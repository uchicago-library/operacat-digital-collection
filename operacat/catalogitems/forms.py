
from django import forms
from .models import CatalogItemComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = CatalogItemComment
        fields = ['subject', 'comment_message']

