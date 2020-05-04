'''
Created on 14 Noo 2019

@author: esoulam
'''
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Vehicule, Trajet, Reservation, LieuDapart, LieuArrivee, NousContactez

admin.site.register(Vehicule)
admin.site.register(Trajet)
admin.site.register(Reservation)
admin.site.register(LieuDapart)
admin.site.register(LieuArrivee)
admin.site.register(NousContactez)