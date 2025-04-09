from django import forms
from .models import Board

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'pdf_file']
        widgets = {
            'pdf_file': forms.FileInput(attrs={'accept': '.pdf'})
        }