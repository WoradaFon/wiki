from django.shortcuts import render
from django import forms
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import re
import markdown2

class Newpages(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))

# create your view here.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def newpage(request):
    if request.method == "POST":
        form = Newpages(request.POST)
        if form.is_valid():
            title2 = form.cleaned_data["title"]
            content2 = form.cleaned_data["content"]

            # check the topic
            topics = util.list_entries()
            for topic in topics:
                if topic.lower() == title2.lower():
                    return HttpResponseRedirect(reverse("index"))
            
            # safe the content
            util.save_entry(title2, content2)

            # go to the content
            entries = util.get_entry(title2)
            return render(request, "encyclopedia/entries.html", {
                "entries": markdown2.markdown(entries)
            })
    else:
        new_page = Newpages()
        return render(request, "encyclopedia/newpage.html", {
            "new_page": new_page
        })


def entries(request, name):
    entries = util.get_entry(name)
    return render(request, "encyclopedia/entries.html", {
        "entries": markdown2.markdown(entries),
        "name": name
    })


def search(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("index"))
