from django import forms

from .i18n import t
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': t('contact.name'),
            'email': t('contact.email_ph'),
            'subject': t('contact.subject'),
            'message': t('contact.message'),
        }
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = placeholders.get(name, '')
            field.widget.attrs['required'] = True
            field.label = ''

    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }
