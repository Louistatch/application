from django.urls import path
from . import views
urlpatterns = [
    path('' ,views.home, name="home"),
    path('Investir/' ,views.Investir, name="Investir"),
    path('index/' ,views.index, name="index"),
    path('opportunite/', views.opportunite, name="opportunite"),
    path('Temoignage/' ,views.Temoignage, name="Temoignage"),
    path('elearning/' ,views.elearning, name="elearning"),
    path('search/' ,views.search, name="search"),
]