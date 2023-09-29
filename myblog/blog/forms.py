from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta :
        model = Article
        fields = ['title','category','desc','image']
        labels = {'title':'Titre','category':'Catégorie', 'desc':'Description'}
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),
                   'category':forms.Select(attrs={'class':'form-control'}),
                   'desc':forms.Textarea(attrs={'class':'form-control','rows':5}),
        }