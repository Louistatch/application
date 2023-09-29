from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def home(request):
    list_articles=Article.objects.all()
    context={"liste_articles":list_articles}
    return render(request, "elearning.html" ,context)

def detail(request,id_article):
    article=Article.objects.get(id=id_article)
    category=article.category
    articles_en_relation=Article.objects.filter(category=category)
    return render( request, 'detail.html',{"article":article,"aer":articles_en_relation})

def Investir(request):
    return render(request, 'Investir.html')


def opportunite(request):
    return render(request, 'opportunite.html')


def Temoignage(request):
    return render(request, 'Temoignage.html')

def index(request):
    return render(request, 'index.html')

def elearning(request):
    if not request.user.is_authenticated:
        return redirect('login_blog')
    list_articles=Article.objects.all()
    context={"liste_articles":list_articles}
    return render(request, "elearning.html" ,context)

def search(request):
    query=request.GET["article"]
    liste_article=Article.objects.filter(title__icontains=query)
    return render(request, 'search.html',{"liste_article":liste_article})



