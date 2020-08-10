from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """ Форма для атворизации пользователя """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistration(forms.ModelForm):
    """ Форма для самостоятельной регистрации пользователей на сайте.

        Django предоставляет класс UserCreationForm, который расположен
        в модуле django.contrib.auth.forms. Он очень похож на класс формы,
        созданный нами.
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']
