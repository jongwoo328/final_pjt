from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Review, MAX_RANK


class ReviewForm(forms.ModelForm):
    rank = forms.IntegerField(
        label=None,
        widget = forms.NumberInput(
            attrs={
                'id': 'rank',
                'min': 1,
                'max': MAX_RANK,
            },
        ),
        validators=[MinValueValidator(1), MaxValueValidator(MAX_RANK)],
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