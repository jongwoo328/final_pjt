from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    rank = forms.IntegerField(
        label=None,
        widget = forms.NumberInput(
            attrs={
                'id': 'rank',
            },
        )
    )
    content = forms.CharField(
        label="댓글",
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'id': 'content',
                'placeholder': '이 영화에 대해 평가해주세요!',
            },
        )
    )
    class Meta:
        model = Review
        fields = ('rank', 'content', )
