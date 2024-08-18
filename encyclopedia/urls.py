from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.get_title, name="get_title"),
    path("search",views.search,name="search"),
    path("create",views.create,name="create"),
    path("random_entry",views.random_entry, name="random_entry"),
    path("edit/<str:entry_name>",views.edit,name="edit")
    
]
