from django.shortcuts import render
from django import forms
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.urls import reverse
#from django.contrib.massages.views import SuccessMassageMixin

from . import util
import re
import markdown2
import random


class Newpage(forms.Form):
    title = forms.CharField(label="title", widget=forms.Textarea(attrs={'rows':'1', 'class':'form-control'}))
    content = forms.CharField(label="content", widget=forms.Textarea(attrs={'rows':'10', 'class':'form-control'}))

#class alert(SuccessMassageMixin, CreateView):


# create your view here.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def newpage(request):
    if request.method == "POST":
        form = Newpage(request.POST)
        if form.is_valid():
            content = form.cleaned_data['edit_content']
            title = form.cleaned_data['edit_title']

            topics = util.list_entries()
            for topic in topics:
                if topic.lower() == title.lower():
                    return HttpResponseRedirect(reverse("index"))
            
            # safe the content
            util.save_entry(title, content)

            # go to the content
            entries = util.get_entry(title)
            return render(request, "encyclopedia/entries.html", {
                "entries": markdown2.markdown(entries)
            })
    else:
        return render(request, "encyclopedia/newpage.html", {
            "Newpage": Newpage
        })


def entries(request, name):
    entries = util.get_entry(name)
    return render(request, "encyclopedia/entries.html", {
        "entries": markdown2.markdown(entries),
        "name": name
    })


def search(request):
    if request.method == "POST":
        search = request.POST['q']

        topics = util.list_entries()
        item = []
        for topic in topics:
            if topic.lower() == search.lower():
                entries = util.get_entry(search)
                return render(request, "encyclopedia/entries.html", {
                    "entries": markdown2.markdown(entries)
                    })
            else:
                if search.lower() in topic.lower():
                    item.append(topic)
        
        return render(request, "encyclopedia/search.html", {
            "items" : item
        })


def random_page(request):
    entries = util.list_entries()
    select_entry = random.choice(entries)
    selected = util.get_entry(select_entry)
    return render(request, "encyclopedia/entries.html", {
        "entries": markdown2.markdown(selected),
        "name": selected
    })


def edit(request):
    if request.method == "POST":
        title = request.POST['name']
        content = util.get_entry(title)

        #class Edit(forms.Form):
        #    edit_title = forms.CharField(label="title", initial=title, widget=forms.Textarea(attrs={'rows':'1', 'class':'form-control'}))
        #    edit_content = forms.CharField(label="content", initial=content, widget=forms.Textarea(attrs={'rows':'10', 'class':'form-control'}))
        
        f = Newpage(initial={'title': title, 'content': content})

        return render(request, "encyclopedia/edit.html", {
            "edit": f,
            "name": title
        })

def save_edit(request):
    if request.method == "POST":
        form = Newpage(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            title = form.cleaned_data['title']

            #save the edit
            util.save_entry(title, content)

            #redirect to entry page
            entries = util.get_entry(title)
            return render(request, "encyclopedia/entries.html", {
                "entries": markdown2.markdown(entries)
            })
