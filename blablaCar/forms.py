'''
Created on 14 Noo 2019

@author: esoulam
'''
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from .models import Trajet,Reservation,Vehicule,Profile
#from bootstrap_datepicker_plus import DatePickerInput
#from .widgets import BootstrapDateTimePickerInput
from tempus_dominus.widgets import DateTimePicker
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# class DateForm(forms.Form):
#     vehicule = forms.ModelChoiceField()
#     depart = forms.ModelChoiceField()
#     heure_depart = forms.DateTimeField()
#     arrivee = forms.ModelChoiceField()
#     heure_arrivee = forms.DateTimeField()
#     tarif = forms.CharField()
#     available = forms.BooleanField()
#     commentaire = forms.CharField(widget=forms.Textarea())

class DateForm(ModelForm):
    class Meta:
        model = Trajet
        fields = ['vehicule','depart','heure_depart','arrivee',
        'heure_arrivee','tarif','available','commentaire',]
        widgets = {
            'heure_depart': DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
        'heure_arrivee': DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),      
        }

# class DateForm1(ModelForm):
#     class Meta:
#         model = Trajet
#         fields = ['vehicule','depart','heure_depart','arrivee',
#         'heure_arrivee','tarif','available','commentaire']
#         widgets = {
#             'heure_depart': DatePickerInput(), # default date-format %m/%d/%Y will be used
#             'heure_arrivee': DatePickerInput(format='%Y-%m-%d'), # specify date-frmat
#         }


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['idTrajet','num_vehicule','lieu_depart','lieu_arrivee','heure_depart','heure_arrivee',
        'pseudo_client','non_client','contact_client','contact_client1', 'nbPlace_Reservee']

class VehiculeForm(ModelForm):
    class Meta:
        model = Vehicule
        fields = ['nom_conducteur','numero_conducteur1','numero_conducteur2',
        'numero_vehicule','nbPlace','marque','image_vehicule']

class TrajetForm(ModelForm):
    class Meta:
        model = Trajet
        fields = ['vehicule','depart','heure_depart','arrivee',
        'heure_arrivee','tarif','available','commentaire']


class MyForm(forms.Form):
    datetime_field = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

class LoginForm(forms.Form):
    username = forms.CharField(label='pseudo')
    password = forms.CharField(label='Mot de passe',widget = forms.PasswordInput)

    # def clean(self):
    #     cleaned_data = super(LoginForm, self).clean()
    #     username = cleaned_data.get("username")
    #     #password = cleaned_data.get("password")
    #     if username:
    #         result = User.objects.filter(username=username)
    #         if len(result) != 1:
    #             raise forms.ValidationError("Adresse de courriel ou mot de passe erone(e).")
    #         #if password != 'sesame' or email != 'sdaouda@gmail.com':
            
    #     return cleaned_data

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='',label='Nom')
    last_name = forms.CharField(max_length=30, required=False, help_text='',label='Prénom')
    email = forms.EmailField(max_length=254, help_text='')
    telephone = forms.CharField(help_text='Numero de phone')

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','telephone', 'password1', 'password2', )