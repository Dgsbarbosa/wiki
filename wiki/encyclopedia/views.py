from django.shortcuts import render

from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_title(request, title):
    
    entrie = markdown2.markdown(util.get_entry(title))
    
    print(entrie)
    context={"entrie":entrie}
    return render(request, "encyclopedia/title.html",context)