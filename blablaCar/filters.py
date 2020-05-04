'''
Created on 14 Noo 2019

@author: esoulam
'''
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from .models import Category, Product, Commodite, Vendor
import django_filters
from django import forms

class UserFilter(django_filters.FilterSet):
        details = django_filters.ModelMultipleChoiceFilter(queryset=Commodite.objects.all(),
                widget=forms.CheckboxSelectMultiple)
        #year_joined__gt = django_filters.NumberFilter('date_joined', lookup_expr='year__gt')
        #year_joined__lt = django_filters.NumberFilter('date_joined', lookup_expr='year__lt')
        class Meta:
                model = Product
                fields = ['commdt', 'localite', 'category', 'action_type', 'details']
                # fields = {
                #         'username': ['exact', ],
                #         'first_name': ['icontains', ],
                #         'last_name': ['exact', ],
                #         'date_joined': ['year', 'year__gt', 'year__lt', ],
                #         }

class VendorFilter(django_filters.FilterSet):
        
        class Meta:
                model = Vendor
                fields = ['name', 'email', 'phone1', 'phone2', 'phone3', 'address', 'ville', 
                'quartier', 'localization']