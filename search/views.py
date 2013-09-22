# Summary: Views for returning search results.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from search.searchAlgorithm.initialize_search import search

class SearchAllView(generic.View):  
    def post(self, request, *args, **kwargs):
        searchStr = request.POST["search"]
        if searchStr != "":
            searchResults = search(searchStr)
            returnDict = {}
            returnDict["value"] = searchStr
            return render(request, 'search/searchResult.html', {'results': searchResults, 'search': returnDict})
        else:
            return HttpResponse(400)
            
    def get(self, request, *args, **kwargs):
        return HttpResponse(400)