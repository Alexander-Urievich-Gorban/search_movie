
from .models import *
from django import forms



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude = ['create_at', 'movie', 'profile']
        fields = ("text",)
        widgets = {
            'text': forms.Textarea(attrs={'id': 'contactcomment'})
        }


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""

    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)
