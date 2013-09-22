# Summary: Get Posts realted to a given career area and also categorize posts into different career areas.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from contributions.models import Posts
from careers.models import Area
from careers.algorithms import CalculateCareer

class Career(generic.ListView):
    template_name = 'careers/career.html'
    context_object_name = 'post_list'
    paginate_by = 10
    
    def get_queryset(self, **kwargs):
        career = self.kwargs["careerCategory"]
        if career == "ArtDesignFashion":
            queryset = Posts.objects.prefetch_related('user','tags').filter(ArtDesignFashion=1)
        elif career == "Business":
            queryset = Posts.objects.prefetch_related('user','tags').filter(Business=1)
        elif career == "Education":
            queryset = Posts.objects.prefetch_related('user','tags').filter(Education=1)
        elif career == "Energy":
            queryset = Posts.objects.prefetch_related('user','tags').filter(Energy=1)
        elif career == "Engineering":
            queryset = Posts.objects.prefetch_related('user','tags').filter(Engineering=1)
        elif career == "Entertainment":
            queryset = Posts.objects.prefetch_related('user','tags').filter(Entertainment=1)
        elif career == "GovernmentAndLaw":
            queryset = Posts.objects.prefetch_related('user','tags').filter(GovernmentAndLaw=1)
        elif career == "HealthAndMedicine":
            queryset = Posts.objects.prefetch_related('user','tags').filter(HealthAndMedicine=1)
        elif career == "NonProfits":
            queryset = Posts.objects.prefetch_related('user','tags').filter(NonProfits=1)
        elif career == "Technology":
            queryset = Posts.objects.prefetch_related('user','tags').filter(Technology=1)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(Career, self).get_context_data(**kwargs)
        context["career"] =  Area.objects.get(url = self.kwargs["careerCategory"])
        if self.request.user.is_authenticated():
            context["authenticated"] = True
        else:
            context["authenticated"] = False
        
        return context

class Categorize(generic.View):
    def post(self, request, *args, **kwargs):
        post_pk = self.request.POST["post_pk"]
        post = Posts.objects.get(pk=post_pk)
        # Reset career relations for this post.
        post.ArtDesignFashion = 0
        post.Business = 0
        post.Education = 0
        post.Energy = 0
        post.Engineering = 0
        post.Entertainment = 0
        post.GovernmentAndLaw = 0
        post.HealthAndMedicine = 0
        post.NonProfits = 0
        post.Technology = 0
        post.save()
        # Calculate career relations of this post.    
        calculate = CalculateCareer(post)
        
        return HttpResponse("Success.")
        
    def get(self, request, *args, **kwargs):
        return HttpResponse("HTTP GET method not allowed. HTTP POST method only.")
    
        