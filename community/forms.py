from django import forms

from .models import Article, Comment, Board


class ArticleForm(forms.ModelForm):
    board = forms.ModelChoiceField(queryset=Board.objects.all())
    class Meta:
        model = Article
        fields = ('title', 'content', )
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="댓글",
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'id': 'content',
                'placeholder': '댓글',
            },
        )
    )
    class Meta:
        model = Comment
        fields = ('content', )