from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': _('Come ti chiami?'),
                   'class': 'w-100'}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': _('La tua mail?'),
                   'class': 'w-100'}
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': _('Cosa vuoi dirci?'),
                   'rows': 4}
        )
    )
