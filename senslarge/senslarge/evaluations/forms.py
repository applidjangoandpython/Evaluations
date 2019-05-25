from django import forms
from .models import Formulaire, Choice, Categorie
from django.contrib.auth.models import User


class ChoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        my_formulaire = kwargs.pop('my_formulaire')
        reponse = super().__init__(*args, **kwargs)
        self.fields['categorie'].queryset = Categorie.objects.filter(
            formulaire=my_formulaire
        )
        return reponse

    class Meta:
        model = Choice
        fields = ['choice_text', 'categorie', 'valorisation']


class ChoiceFormEdit(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        formulaire = kwargs.pop('formulaire')

        super().__init__(*args, **kwargs)

        self.fields['categorie'].queryset = Categorie.objects.filter(
            formulaire=formulaire
        )

    class Meta:
        model = Choice
        fields = ['choice_text', 'categorie', 'valorisation']


class UserForm(forms.ModelForm):
    formulaires = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=Formulaire.objects.all(),
        label='Formulaires associés',
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'formulaires',
        ]

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(
                "Cette adresse mail est déjà utilisée par un autre utilisateur"
            )
        return data


class UserChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.my_formulaire = kwargs.pop('my_formulaire')
        reponse = super().__init__(*args, **kwargs)
        return reponse

    def clean(self):
        cleaned_data = super().clean()
        if self.my_formulaire.nb_points != sum(cleaned_data.values()):
            raise forms.ValidationError(
                "La somme totale des points doit être égale à {}.".format(
                    self.my_formulaire.nb_points
                )
            )
        return cleaned_data
