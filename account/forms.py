from django import forms


class LoginForm(forms.Form):
    """ Форма для атворизации пользователя """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
