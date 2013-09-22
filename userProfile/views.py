# Summary: View user's stories(profile), edit your own story(profile) and upload a profile picture to AWS S3.
import random
import os
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from userProfile.forms import DocumentForm
from userProfile.models import Document, Profile, Points
from handleImageUpload import image_upload
from contributions.models import Posts

class Story(generic.DetailView):
    template_name = 'userProfile/story.html'
    context_object_name = 'profile'
    
    def get_object(self, **kwargs):
        # Determine if the user is accessing their own profile or another user's profile.
        if "pk" not in self.kwargs:
            self.user_id = self.request.user.id
            self.my_profile = True
            return get_object_or_404(Profile, pk=self.request.user.id) 
        else:
            self.user_id = self.kwargs["pk"]
            self.my_profile = False
            return get_object_or_404(Profile, pk=self.kwargs["pk"]) 
        
    def get_context_data(self, **kwargs):
        context = super(Story, self).get_context_data(**kwargs)
        user_id = self.user_id
        context["myProfile"] = self.my_profile     
        context["points"] = Points.objects.get(user_id = self.user_id)
        context["posts"] = Posts.objects.filter(user_id = self.user_id).prefetch_related('tags')
        # Determine if the request is coming from an authenticated user or a guest.
        if self.request.user.is_authenticated():
            context["authenticated"] = True
        else:
            context["authenticated"] = False
        return context
  
class EditStory(generic.DetailView):
    template_name = 'userProfile/edit.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super(EditStory, self).get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

class ImageUpload(generic.FormView):
    form_class = DocumentForm
    
    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('myUserProfile:edit')) 

    def form_valid(self, form):
        if self.request.method == 'POST':
            # Upload the file using the Document form.
            # Image is temporarily saved to the '/temp' directory in this project.
            newdoc = Document(file = self.request.FILES['file'])
            newdoc.save()
            
            # Create a FileName for AWS S3
            temp_file_name = str(newdoc.file)
            file_extension = os.path.splitext(temp_file_name)[1]
            userFirst_name = self.request.user.first_name
            userLast_name = self.request.user.last_name
            user_id = self.request.user.id
            s3_file_name = str(userFirst_name)+"_"+str(userLast_name)+"_"+str(user_id)+"_"+str(random.randint(1,200))+str(random.randint(1,300))+str(file_extension.lower())
            
            # Upload the File to S3 and Save the New File Name to User's Profile.
            image_upload(temp_file_name, s3_file_name, user_id)
            
            return HttpResponseRedirect(reverse('myUserProfile:edit'))
        else:
            # Upload request must be made via POST.
            return HttpResponseRedirect(reverse('myUserProfile:edit'))
            
class Update(generic.View):  
    def post(self, request, *args, **kwargs):
        value = self.request.POST["updateValue"]
        target = self.request.POST["target"]
        user_id = self.request.user.id;
        user = User.objects.get(pk=user_id)
        profile = Profile.objects.get(pk=user_id)
        
        if target == "fname":
            if value != profile.fname:
                profile.fname = value
                profile.save(update_fields=['fname'])
                user.first_name = value
                user.save(update_fields=['first_name'])
                return HttpResponse("Successly Updated Your First Name to " + str(value) + ".")
            else:
                return HttpResponse(400)

        elif target == "lname":
            if value != profile.lname:
                profile.lname = value
                profile.save(update_fields=['lname'])
                user.last_name = value
                user.save(update_fields=['last_name'])
                return HttpResponse("Successly Updated Your Last Name to " + str(value) + ".")
            else:
                return HttpResponse(400)
        
        elif target == "company":
            if value != profile.company:
                profile.company = value
                profile.save(update_fields=['company'])
                return HttpResponse("Successly Updated Your Company to " + str(value) + ".")
            else:
                return HttpResponse(400)
        
        elif target == "title":
            if value != profile.title:
                profile.title = value
                profile.save(update_fields=['title'])
                return HttpResponse("Successly Updated Your Title to " + str(value) + ".")
            else:
                return HttpResponse(400)
            
        elif target == "city":
            if value != profile.city:
                profile.city = value
                profile.save(update_fields=['city'])
                return HttpResponse("Successly Updated Your City to " + str(value) + ".")
            else:
                return HttpResponse(400)
            
        elif target == "state":
            if value != profile.state:
                profile.state = value
                profile.save(update_fields=['state'])
                return HttpResponse("Successly Updated Your State to " + str(value) + ".")
            else:
                return HttpResponse(400)
            
        elif target == "email":
            if value != user.email:
                user.email = value
                user.username = value
                user.save(update_fields=['username','email'])
                return HttpResponse("Successly Updated Your Email Login to " + str(value) + ".")
            else:
                return HttpResponse(400)
            
    def get(self, request, *args, **kwargs):
        return HttpResponse("Error")