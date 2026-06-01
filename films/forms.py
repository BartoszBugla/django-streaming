from django import forms
from .models import Comment, Rating, Category


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Napisz komentarz...',
                'class': 'w-full bg-zinc-800 text-white rounded-lg p-3 border border-zinc-700 focus:border-red-500 focus:outline-none',
            })
        }
        labels = {
            'content': '',
        }


class RatingForm(forms.Form):
    score = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'w-20 bg-zinc-800 text-white rounded-lg p-2 border border-zinc-700 text-center focus:border-red-500 focus:outline-none',
            'min': 1,
            'max': 10,
            'placeholder': '1-10',
        })
    )


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Szukaj filmu...',
            'class': 'bg-zinc-800 text-white rounded-lg px-4 py-2 border border-zinc-700 focus:border-red-500 focus:outline-none w-full',
        })
    )
    genre = forms.CharField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'bg-zinc-800 text-white rounded-lg px-4 py-2 border border-zinc-700 focus:border-red-500 focus:outline-none w-full md:w-48',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].widget.choices = [('', 'Wszystkie gatunki')] + [
            (category.name, category.name) for category in Category.objects.all()
        ]


