from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import random
from markdown2 import Markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, title):
    if not (content := util.get_entry(title)):
        content = f"{title} is not avaialble."
    markdowner = Markdown()
    context = {
        "title": title,
        "content": markdowner.convert(content)
    }
    return render(request, "encyclopedia/entry.html", context)

def search(request):
    entry_list = util.list_entries()
    if request.method == "GET":
        query = request.GET.get('q', None)
        for entry in entry_list:
            if query.lower() == entry.lower():
                return entries(request, entry)
        search_results = []
        for entry in entry_list:
            if query.lower() in entry.lower():
                search_results.append(entry)
        if not search_results:
            search_results.append(None)
        context = {
            "results": search_results,
            "query": query
        }
        return render(request, "encyclopedia/search.html", context)
    else:
        return HttpResponseRedirect("/")

def new(request):
    entry_list = util.list_entries()
    if request.method == "POST":
        print("yes")
        for entry in entry_list:
            if request.POST['title'].lower() == entry.lower():
                return render(request, "encyclopedia/error.html", {'error': "Entry already exists."})
        # print(request.POST)
        util.save_entry(request.POST['title'], request.POST['content'])
        return HttpResponseRedirect("/new")
    else:
        return render(request, "encyclopedia/new.html", {})

def edit(request):
    if request.method == 'GET':
        
        context = {
            'title': request.GET['title'],
            'content': util.get_entry(request.GET['title'])
        }
        return render(request, "encyclopedia/edit.html", context)
    elif request.method == 'POST':
        util.save_entry(request.POST['title'], request.POST['content'])
        return entries(request, request.POST['title'])
    else:
        return HttpResponseRedirect("/")

def rand(request):
    
    random_entry = random.choice(util.list_entries())
    return entries(request, random_entry)
    