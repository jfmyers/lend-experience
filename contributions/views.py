# Summary: Views for viewing, adding, editing contributions and contributions' comments.
import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from contributions.forms import CommentForm, PostForm
from contributions.models import Comments, Posts
from tags.models import Tags
from userProfile.models import Points, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import time

class AddContributionView(generic.TemplateView):
    # View for creating/adding a new contribution(aka experience post).
    template_name = 'contributions/add_contribution.html'

class EditContributionView(generic.DetailView):
    # View for editing an existing contribution(aka experience post).
    model = Posts
    context_object_name = "post"
    template_name = 'contributions/edit_contribution.html'

class MultiContributionView(generic.ListView):
    # View for multiple contributions(the default home page).
    template_name = 'contributions/multi_contributions.html'
    context_object_name = 'contributions'
    queryset = Posts.objects.prefetch_related('user','tags').filter(type = "experience").order_by('-rating')[:10]
    
    def get_context_data(self, **kwargs):
        context = super(MultiContributionView, self).get_context_data(**kwargs)
        context["points"] = Points.objects.prefetch_related('user').order_by('-total')[:5]
        if self.request.user.is_authenticated():
            context["authenticated"] = True
        else:
            context["authenticated"] = False
        return context

class SingleContributionView(generic.DetailView):
    # View for a single contribution(aka experience post).
    context_object_name = 'post'
    template_name = 'contributions/single_contribution.html'
    
    def get_object(self,**kwargs):
        return Posts.objects.get(pk=self.kwargs["pk"])
    
    def get_context_data(self, **kwargs):
        context = super(SingleContributionView, self).get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["post_comments"] = Comments.objects.prefetch_related('user').filter(contribution_id = self.kwargs["pk"])
        if self.request.user.is_authenticated():
            context["authenticated"] = True
        else:
            context["authenticated"] = False
        return context
     

class SaveNewPostForm(generic.FormView):
    # Save new contributions(aka experience posts). Return data via json if it's an AJAX request.
    form_class = PostForm

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            # Request must be made via Ajax. If error redirect to home feed.
            return HttpResponseRedirect(reverse('feed:post_list')) 

    def form_valid(self, form):
        if self.request.is_ajax():       
            tag_name = self.request.POST["tag"]
            # Is this a brand new tag or did a user select a tag that already exists in the database?
            tag_type = self.request.POST["tag_type"]
            
            # If it's a new tag, save it.
            if tag_type == "new":
                tag = Tags(name=tag_name)
                tag.handle = tag.clean_handle(tag_name)
                tag.save()
            else:
                tag = Tags.objects.get(name=tag_name)
            
            # Save the post and format the title to make it url safe.
            title = form.cleaned_data["title"]
            user_id = self.request.user.id
            date_created = int(time.time())            
            post = Posts(title=title,description=form.cleaned_data["description"],formatted_description=form.cleaned_data["formatted_description"],user_id=user_id, type="experience", date_created = date_created)
            post.save()
            title_url = post.clean_title(title)
            post.url = title_url
            post.save()
            post.tags.add(tag)
            
            # Return data.
            data = {
                'post_pk': post.id,
                'post_url': post.url
            }
            return self.render_to_json_response(data)
        else:
            # Request must be made via Ajax. If error redirect to home feed.
            return HttpResponseRedirect(reverse('feed:post_list'))  

class SaveExistingPostForm(generic.FormView):
    # Save edits made to an existing contribution(aka experience post). Return json if post is made via AJAX.
    form_class = PostForm

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            # Request must be made via Ajax. If error redirect to home feed.
            return HttpResponseRedirect(reverse('feed:post_list')) 

    def form_valid(self, form):
        if self.request.is_ajax():
            # Verify a pk has been sent for the Post to be edited
            if "post_id" in self.request.POST:
                pk = self.request.POST["post_id"]
                # Verify the creator of this experience is the one that is editing it
                post = Posts.objects.get(pk=pk)
                if post.user.id == self.request.user.id:  
                    # Determine what field to update 
                    title = form.cleaned_data["title"]
                    description = form.cleaned_data["description"]
                    formatted_description = form.cleaned_data["formatted_description"]
                    
                    if title == post.title:
                        # Title has not been altered, update the descriptions
                        post.formatted_description = formatted_description
                        post.description = description
                        post.save(update_fields=['description','formatted_description'])
                    else:
                        url = post.clean_title(title)
                        post.url = url
                        post.title = title
                        post.save(update_fields=['title','url'])
                    
                    # Return data
                    data = {
                        'message': "Successfully updated this experience",
                        'status': 200,
                        'post_url': post.url
                    }
                    return self.render_to_json_response(data)
                    
                else:
                    return HttpResponse("Access forbidden.", status=403)
                
            else:
                return HttpResponse("Primary Key for post not provided.", status=400)
        else:
            # Request must be made via Ajax. If error redirect to home feed.
            return HttpResponseRedirect(reverse('feed:post_list'))  

def CommentPost(request):
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(pk=request.user.id)
            contribution_id = form.cleaned_data["contribution_id"]
            text = form.cleaned_data["text"]
            date_created = int(time.time())
            newComment = Comments(contribution_id =contribution_id, user=profile, text=text, date_created=date_created)
            newComment.save()
            
            post = Posts.objects.get(pk=contribution_id)
            post.comments.add(newComment)
            
            if request.is_ajax():
                return render(request, 'contributions/comment.html', {'comment': newComment})
            else:
                return HttpResponseRedirect(reverse('contributions:detail', kwargs={'title':profile.fname, 'pk':contribution_id}))

        else:
            if request.is_ajax():
                return HttpResponse("Unable to save.")


    return HttpResponseRedirect( reverse('contributions:post_list') )

def CommentRemove(request):
    if request.POST:
        comment_id = request.POST["comment_id"]
        user_id = request.user.id;
        try:
            comment = Comments.objects.get(pk = comment_id)
            # Make sure person deleting is the commentor
            if comment.user.id == user_id:
                post = Posts.objects.get(pk = comment.contribution_id)
                post.comments.remove(comment)
                comment.delete()
                if request.is_ajax():
                    return HttpResponse("Success. Comment removed.")
                else:
                    return HttpResponseRedirect(reverse('contributions:detail', kwargs={'title':post.url, 'pk':comment.contribution_id}))
            else:
                if request.is_ajax():
                    return HttpResponse("Comment remove failed. Unauthorized access attempt.", status=403)
                else:
                    return HttpResponseRedirect(reverse('feed:post_list'))

        except:
            return HttpResponseRedirect(reverse('feed:post_list'))
            
    return HttpResponseRedirect( reverse('contributions:post_list') )