from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import RequestContext, Context
from accounts.forms import UserForm
from userProfile.models import Profile, Points

class SignUp(generic.FormView):
    form_class = UserForm
    template_name = "registration/signup.html"  
    success_url = '/signup/success/'
    
    def form_valid(self, form):
        if self.request.method == 'POST':
            try:
                # Make the user's username the email address they signed up with. Then create a new user.
                form.cleaned_data["username"] = form.cleaned_data["email"]
                user = User.objects.create_user(**form.cleaned_data)
                
                # Create a profile for the new user.
                profile = Profile(id=user.id,fname=form.cleaned_data["first_name"],lname=form.cleaned_data["last_name"],dateJoined=user.date_joined)
                profile.save()
                # Create a Profile Handle that is URL Safe using clean_handle() method of Profile model.
                handle = str(profile.fname[0])+str(profile.lname)
                cleaned_handle = profile.clean_handle(handle)
                # Check to make sure handle is not already taken    
                check = Profile.objects.filter(handle=cleaned_handle)
                if check.count() > 0:
                    cleaned_handle = cleaned_handle+str(profile.id)
                # Save the cleaned handle
                profile.handle = cleaned_handle
                profile.save(update_fields=['handle'])            
                # Give the user points
                points = Points(user=profile, total=25)
                points.save()
                # Send a success welcome email.
                send_mail(
                    'Thanks for signing up ' + str(profile.fname) + '!',
                    get_template('registration/signup_email.html').render(
                        Context({
                            'first_name': str(profile.fname)
                        })
                    ),
                    'hello@lendexperience.com',
                    [user.email],
                    fail_silently = True
                )
                return HttpResponseRedirect(reverse('accounts:signup_success'))
            except:
                # If a the email input by the user is already taken the above will fail. Render the following with errors.
                return render(self.request, 'registration/signup.html', {'form': form,'duplicate':True}) 
            
        else:
            # Redirect to signup page if this is a HTTP Get request.
            return HttpResponseRedirect(reverse('accounts:signup')) 
    
    def form_invalid(self, form):
        # Redirect to signup with form errors if form is invalid.
        return render(self.request, 'registration/signup.html', {'form': form}) 

def signupSuccess(request):
    return render_to_response('registration/signup_success.html',RequestContext(request))  

def signupError(request):
    return render_to_response('registration/signup_error.html',RequestContext(request))  
    
