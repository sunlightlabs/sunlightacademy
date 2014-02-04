from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationForm

from training.models import Feedback, IS_A_CHOICES

attrs_dict = {'class': 'required'}


class ProfileForm(forms.Form):

    phone = forms.CharField(required=False, max_length=24)
    organization = forms.CharField(required=False, max_length=128)
    is_a = forms.ChoiceField(required=False, choices=IS_A_CHOICES)
    interests = forms.CharField(required=False, widget=forms.Textarea)
    notify = forms.BooleanField(required=False, initial=True)


class UniqueEmailRegistrationForm(RegistrationForm, ProfileForm):
    """ Basic registration form that requires unique email addresses.

        Also overrides passwords to retain value on error.
    """

    first_name = forms.CharField(max_length=64, required=False)
    last_name = forms.CharField(max_length=64, required=False)

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=True),
        label="Password")

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=True),
        label="Confirm Password")

    def clean(self):

        cleaned_data = super(UniqueEmailRegistrationForm, self).clean()

        if 'email' in cleaned_data:
            email = cleaned_data['email']
            if User.objects.filter(email=email).exists():
                self._errors['email'] = self.error_class(["Email address has already been used"])
                del cleaned_data['email']

        return cleaned_data


class SettingsForm(ProfileForm):
    """ Form used on account settings page.
    """

    username = forms.CharField(max_length=32)
    first_name = forms.CharField(max_length=64, required=False)
    last_name = forms.CharField(max_length=64, required=False)
    email = forms.EmailField()
    new_password = forms.CharField(required=False, widget=forms.PasswordInput)


class AccountSetupForm(ProfileForm):
    """ Form used during social authentication to set account preferences.
    """

    username = forms.CharField(max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()

    def clean(self):

        cleaned_data = super(AccountSetupForm, self).clean()

        if 'username' in cleaned_data:
            username = cleaned_data['username']
            if User.objects.filter(username=username).exists():
                self._errors['username'] = self.error_class(["Username is already taken"])
                del cleaned_data['username']

        if 'email' in cleaned_data:
            email = cleaned_data['email']
            if User.objects.filter(email=email).exists():
                self._errors['email'] = self.error_class(["Email address has already been used"])
                del cleaned_data['email']

        return cleaned_data


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('timestamp',)
