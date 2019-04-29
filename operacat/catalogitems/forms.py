
from django import forms
from .models import CatalogItemComment

class CommentForm(forms.ModelForm):
    """auto-generated form for comment posting on catalog item pages
    """
    class Meta:
        model = CatalogItemComment
        fields = ['subject', 'comment_message']

