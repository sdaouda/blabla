'''
Created on 14 Noo 2019

@author: esoulam
'''
# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone

class LieuDapart(models.Model):
    localite = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return "%s" % (self.localite)

class LieuArrivee(models.Model):
    localite = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return "%s" % (self.localite)


class Vehicule(models.Model):
    nom_conducteur = models.CharField(max_length=30,blank=True)
    numero_conducteur1 = models.CharField(max_length=15)
    numero_conducteur2 = models.CharField(max_length=15,blank=True)
    numero_vehicule = models.CharField(max_length=7, db_index=True)
    nbPlace = models.IntegerField(default=0)
    marque_choice = (
        ('TOYOTA', 'TOYOTA'),
        ('MERCEDEZ-BENZ', 'MERCEDEZ-BENZ'),
        ('HUNDAI', 'HUNDAI'),
        ('HONDA', 'HONDA'),
        ('RENAULT', 'RENAULT'),
        ('PEUGEAUT', 'PEUGEAUT'),
        ('AUTRE', 'AUTRE'),
    )
    marque = models.CharField(max_length=15, choices=marque_choice, blank=True, default='toy', help_text='Si Autre svp specifier une image')
    image_vehicule = models.ImageField(upload_to='blablaCar/images/', blank=True)

    def get_absolute_url(self):
        return reverse('maj_vehicule', args=[self.id])
    def get_absolute_url1(self):
        return reverse('delete2', args=[self.id])
    def get_absolute_url2(self):
        return reverse('delete2', args=[self.id])

    def __str__(self):
        return self.numero_vehicule

    class Meta:
        permissions = (("can_change_img_vehicule", "Can change img vehicule"),)

class Trajet(models.Model):
    vehicule = models.ForeignKey(Vehicule ,on_delete=models.CASCADE,blank=True, null=True)
    trajet_creation_date = models.DateField(auto_now_add=True)
    depart = models.ForeignKey(LieuDapart,on_delete=models.CASCADE,blank=True, null=True)
    heure_depart = models.DateTimeField(blank=True, null=True)
    arrivee = models.ForeignKey(LieuArrivee,on_delete=models.CASCADE,blank=True, null=True)
    heure_arrivee = models.DateTimeField(blank=True, null=True)
    tarif = models.CharField(max_length=8)
    available = models.BooleanField(default=True)
    commentaire = models.TextField(blank=True,help_text='Decrire les eventuels detours')

    def __str__(self):
        return "%s-%s" % (self.depart,self.arrivee)

    def get_absolute_url(self):
        return reverse('dest_detail', args=[self.id])
    def get_absolute_url1(self):
        return reverse('traj_update', args=[self.id])
    def get_absolute_url2(self):
        return reverse('delete1', args=[self.id])

class Reservation(models.Model):
    idTrajet = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lieu_depart = models.CharField(max_length=30,blank=True, null=True)
    lieu_arrivee = models.CharField(max_length=30,blank=True, null=True)
    heure_depart = models.CharField(max_length=30,blank=True, null=True)
    heure_arrivee = models.CharField(max_length=30,blank=True, null=True)
    pseudo_client = models.CharField(max_length=30,blank=True, null=True)
    non_client = models.CharField(max_length=30,blank=True, null=True)
    contact_client = models.CharField(max_length=15)
    contact_client1 = models.CharField(max_length=15,blank=True, null=True)
    nbPlace_Reservee = models.IntegerField(default=1)
    
    def __str__(self):
        return "%s--(%s)" % (self.non_client,self.contact_client1)

class NousContactez(models.Model):
    nom = models.CharField(max_length=30,blank=True, null=True)
    addresse = models.CharField(max_length=30,blank=True, null=True)
    tel = models.CharField(max_length=35,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fax = models.CharField(max_length=16,blank=True, null=True)
    commentaire = models.TextField(blank=True,help_text='Autres commentaires')
    def __str__(self):
        return self.nom