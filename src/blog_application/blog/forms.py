from django import forms
from .models import Post, User


class PostForm(forms.ModelForm):

    text = forms.CharField(label='text_unput', widget=forms.Textarea(attrs={'class':'form-control',  "rows": 5, "cols": 20}))
    author = forms.ModelChoiceField(label='author_select', queryset=User.objects.all(), empty_label=None,widget = forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Post
        fields = ['text', 'author']

