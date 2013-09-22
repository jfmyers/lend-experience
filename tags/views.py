# Summary: View posts related to tags, search tags, create tags and delete tags.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from tags.tagSearch import SearchTags, ManageTags
from contributions.models import Posts
from tags.models import Tags

class TagsView(generic.ListView):
    template_name = 'tags/detail.html'
    context_object_name = 'post_list'
    paginate_by = 10
    
    def get_queryset(self, **kwargs):
        # Get the posts that have been assigned this tag.
        pk = self.kwargs["pk"]
        self.tag = Tags.objects.get(pk = pk)
        queryset = Posts.objects.prefetch_related('user','tags').filter(tags = self.tag)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(TagsView, self).get_context_data(**kwargs)
        context["tag"] = self.tag
        if self.request.user.is_authenticated():
            context["authenticated"] = True
        else:
            context["authenticated"] = False
        
        return context

class Search(generic.View):  
    def post(self, request, *args, **kwargs):
        searchStr = request.POST["tag_text"]
        if searchStr != "":
            searchResults = SearchTags(searchStr).search()
            # Determine whether a new post is being created with a single tag or if tags are being added to an existing post.
            if "contribution_id" in request.POST.keys():
                contribution_id = request.POST["contribution_id"]
                searchDict = {}
                searchDict["string"] = searchStr
                searchDict["contribution_id"] = contribution_id
                # If tags are being added to existing posts, return HTML of just the tags.
                return render(request, 'tags/searchResult.html', {'results': searchResults, 'search': searchDict})
            else:
                # If tag is being added with the creation of a new post, send back this html.
                return render(request, 'tags/searchResult_newContribution.html', {'results': searchResults, 'search': searchDict})
        else:
            return HttpResponse(400)
            
    def get(self, request, *args, **kwargs):
        return HttpResponse(400)

@login_required
def SaveTag(request):
    if request.POST:
        type = request.POST["type"]
        tag = request.POST["tag_text"]
        contribution_id = request.POST["contribution_id"]
        post = Posts.objects.get(pk=contribution_id)
        title = post.title.replace(" ", "")
        
        if type is not None and tag is not None and contribution_id is not None:
            if type == "new":
                #Save to tags_tags
                tagLib = Tags(name=tag)
                tagLib.handle = tagLib.clean_handle(tag)
                tagLib.save()
            else:
                tagLib = Tags.objects.get(name = tag)
                
            #save to posts_tags
            post.tags.add(tagLib)
            post.save()
            #add to Redis Tags
            redis = ManageTags(tag)
            redis.add()
            
            if request.is_ajax():
                return render(request, 'tags/tag.html', {'tag': tagLib})
            else:
                return HttpResponseRedirect(reverse('singleCont:detail', kwargs={'pk': contribution_id, 'title': title} ))
        
        else: 
            if request.is_ajax():
                HttpResponse(400)
            else:
                return HttpResponseRedirect(reverse('singleCont:detail', kwargs={'pk': contribution_id, 'title': title} ))

    return HttpResponseRedirect(reverse('contributions:post_list'))

@login_required
def RemoveTag(request):
    if request.POST:
        contribution_id = request.POST["contribution_id"]
        tag_id = request.POST["tag_id"]
        
        try:
            tag = Tags.objects.get(pk=tag_id)
            post = Posts.objects.get(pk=contribution_id)
            
            #remove post_tags
            post.tags.remove(tag)
            
            if request.is_ajax():
                return HttpResponse("Success. Comment removed.")
            else:
                title = post.title.replace(" ", "")
                return HttpResponseRedirect(reverse('singleCont:detail', kwargs={'pk': contribution_id, 'title': title} ))

        except:
            if request.is_ajax():
                return HttpResponse("Error. Tag not Removed.")
            else:
                return HttpResponseRedirect(reverse('contributions:post_list'))
            
            
    return HttpResponseRedirect(reverse('contributions:post_list'))