from django import forms

from .models import Article, Comment, Board


class ArticleForm(forms.ModelForm):
    board = forms.ModelChoiceField(queryset=Board.objects.all())
    class Meta:
        model = Article
        fields = ('title', 'content', )
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )