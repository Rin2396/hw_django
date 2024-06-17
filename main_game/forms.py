"""Forms file."""
from django.contrib.auth import forms, models
from django.forms import Form, ModelChoiceField

from .models import Club


class Registration(forms.UserCreationForm):
    """Form class for registration."""

    class Meta:
        """Meta class for registration."""

        model = models.User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class Join(Form):
    """Form class for join club."""

    club = ModelChoiceField(queryset=Club.objects.all(), label='Выберите клуб')
