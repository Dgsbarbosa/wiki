from django.shortcuts import redirect, render
import random
from . import util
import markdown2

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django import forms

class NewEntryForm(forms.Form):
    
    title = forms.CharField(label="Title")

    description = forms.CharField(widget=forms.Textarea,label="Description")
    
class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_title(request, title):
    
    
    entry_content = util.get_entry(title)

    entrie = ""
    message_error =""
    if entry_content:
        title_line = entry_content.splitlines()[0] if entry_content else ""
        title_only = title_line.lstrip('#').strip()
        entrie = markdown2.markdown(entry_content)
        
    else:
        title_only = "Error"
        message_error = f"The page \n{request.path}\n not found "
        
    context = {"entrie": entrie, "title_only": title_only,"message_error":message_error}    
    
   
    return render(request, "encyclopedia/title.html", context)

def search(request):
    
    query = request.GET.get("q","").strip().lower()

    all_entries = util.list_entries()
    matching_entries = []
    
    
    for entry in all_entries:
        
        if query == entry.lower():
            return redirect("encyclopedia:get_title", title=entry)

        elif query in entry.lower():
            matching_entries.append(entry)

    if matching_entries:
        return render(request, "encyclopedia/search_results.html",{"entries":matching_entries, "query":query})
    
    else:
        return render(request, "encyclopedia/search_results.html",{
            "entries":[],
            "query":query,
            "error_message": "No results found"
        })
        
def create(request):
    
    
    if request.method == "POST":
        
        form = NewEntryForm(request.POST)        
        if form.is_valid():
            
            new_title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            
            list_entries = util.list_entries()

            for entry in list_entries:
                
                if entry.lower() == new_title.lower():
                    
                    error_message = f"{new_title.upper()} Already exists"
                    
                    form = NewEntryForm(initial={'title':new_title, "description":description})
                  
                    
                    context={"form":form,
                             "error_message":error_message}
                    return render(request, "encyclopedia/create.html",context)
            
            formated_description = f"# {new_title.title()}\n\n {description}"
            
            formated_description = formated_description.encode("utf-8")
            
            util.save_entry(new_title.title(),formated_description)    
            
            
            return redirect("encyclopedia:get_title", title=new_title)
    else: 
        form = NewEntryForm()
        context = {
            "form":form,
            
            
        }
        return render(request, "encyclopedia/create.html", context)
    
    
def random_entry(request):
    
    list_entries = util.list_entries()
    
    
  
    return redirect("encyclopedia:get_title", title=random.choice(list_entries))

def edit(request,entry_name):
    
    
    datas_entry = util.get_entry(entry_name.lower())
    
    if request.method == "POST":
        
        form = EditEntryForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data["content"]

            content = content.encode("utf-8")
            util.save_entry(entry_name,content)
        
           
    
        return redirect("encyclopedia:get_title", title=entry_name.lower())
    
    
    
    else:
        form = EditEntryForm(initial={"content":datas_entry})
        context = {"form":form,
                "entry_name": entry_name
                }
        return render(request,'encyclopedia/edit.html',context)