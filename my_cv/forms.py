from django import forms

from .i18n import t
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Hidden trap for bots. People never see or fill it.
    website = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'hp-field',
            'tabindex': '-1',
            'autocomplete': 'off',
            'aria-hidden': 'true',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': t('contact.name'),
            'email': t('contact.email_ph'),
            'subject': t('contact.subject'),
            'message': t('contact.message'),
        }
        for name, field in self.fields.items():
            if name == 'website':
                continue
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
