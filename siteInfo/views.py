# Summary: These views are for pages related to company side of Lend Experience (about us, contact, etc..).
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login

class AboutView(generic.TemplateView):
    template_name = 'siteInfo/about.html'
    
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context["authenticated"] = True
        else:
            context["authenticated"] = False
        return context

class ContactView(generic.TemplateView):
    template_name = 'siteInfo/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context["authenticated"] = True
        else:
            context["authenticated"] = False
        return context

class CommunityView(generic.TemplateView):
    template_name = 'siteInfo/community.html'
    
    def get_context_data(self, **kwargs):
        context = super(CommunityView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context["authenticated"] = True
        else:
            context["authenticated"] = False
        return context

class LegalView(generic.TemplateView):
    template_name = 'siteInfo/legal.html'
    
    def get_context_data(self, **kwargs):
        context = super(LegalView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context["authenticated"] = True
        else:
            context["authenticated"] = False
        return context