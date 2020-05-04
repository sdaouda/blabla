'''
Created on 14 Noo 2019

@author: esoulam
'''
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Vehicule, Trajet, Reservation, LieuDapart, LieuArrivee,NousContactez
from blablaCar.forms import ReservationForm,TrajetForm,DateForm,VehiculeForm,SignUpForm,LoginForm
from django.db.models import Count
from django.urls import reverse_lazy
#from django.http import HttpResponseRedirect
#from bootstrap_datepicker_plus import DateTimePickerInput
from django.views import generic
from datetime import datetime
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from tempus_dominus.widgets import DateTimePicker
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from blablaCar.mixins import GroupRequiredMixin


def is_in_groups(user,group):
    return user.groups.filter(name = group).exists()

@login_required
def CreerTrajet(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('/')
            return redirect('/')
        else:
            var = request.POST.get('heure_depart')
            er = form.errors
            return render(request,'output.html',{'var':var,'er':er})
    else:
        form = DateForm()
        return render(request,'creerTrajet.html',{'form':form,})

class TrajetUpdate(UpdateView):
    model = Trajet
    fields = ['vehicule','depart','heure_depart','arrivee',
                'heure_arrivee','tarif','available','commentaire']            
    template_name_suffix = '_update_form'
    def get_form(self):
         form = super().get_form()
         form.fields['heure_depart'].widget = DateTimePicker(
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
            )
         form.fields['heure_arrivee'].widget = DateTimePicker(
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
            )
         return form

@login_required
#@group_required('Staff')
def vehiculeCreate(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = VehiculeForm()
            return render(request,'outputVehicule.html',{'form':form,})
    else:
        form = VehiculeForm()
        return render(request,'outputVehicule.html',{'form':form,})

def TrouverVehi(request):
    voiture = Vehicule.objects.all()
    return render(request,'trajetFinder.html',{'voiture':voiture,})

def DisplayVehi(request):
    voiture = Vehicule.objects.all()
    #listtra = Trajet.objects.all()
    if request.method == "GET":
        source = request.GET.get('dep')
        voiture_queryset = voiture.filter(Q(numero_vehicule__icontains=source))
        trajet_voiture= Trajet.objects.filter(vehicule_id=voiture_queryset[0].id)
    return render(request,'OneVehicule.html',{'voiture_queryset':voiture_queryset[0],'trajet_voiture':trajet_voiture,})

class VehiculeCreate(CreateView):
    model = Vehicule
    fields = ['nom_conducteur','numero_conducteur1','numero_conducteur2','numero_vehicule',
                'marque','image_vehicule',]
    success_url = '/listvehicule/'

class VehiculeUpdate(UpdateView):
    model = Vehicule
    fields = ['nom_conducteur','numero_conducteur1','numero_conducteur2','numero_vehicule',
                'marque','image_vehicule',]            
    #template_name_suffix = '_update_form'
    template_name = 'vehicule_update_form.html'
    success_url = '/listvehicule/'

class VehiculeDelete(GroupRequiredMixin, DeleteView):
    group_required = [u'Administrateur', u'Staff']
    model = Vehicule
    success_url = reverse_lazy('listvehicule')


# class VehiculeDelete(PermissionRequiredMixin, DeleteView):
#     model = Vehicule
#     #template_name = 'mysite/del_company.html'
#     permission_required = ('blablaCar.can_delete_vehicule', )
#     success_url = reverse_lazy('listvehicule')

class TrajetDelete(GroupRequiredMixin, DeleteView):
    group_required = [u'Administrateur', u'Staff']
    model = Trajet
    #template_name = 'mysite/del_company.html'
    success_url = reverse_lazy('listdestrajets')


def DestinationDetails(request, id):
    place = []
    trajetId = get_object_or_404(Trajet, id=id)
    for i in range(trajetId.vehicule.nbPlace):
        place.append(i+1)
    return render(request,'Destdetail.html',{'trajetId': trajetId,'place':place})


def listDestination(request):
    #listDestination = Trajet.objects.all()
    dlist = []
    #listDestination = get_object_or_404(Trajet, available=True)
    listDestination = Trajet.objects.filter(available=True)
    for dest in listDestination:
        dlist.append(dest.arrivee)
        dh = dest.heure_depart
        dh = int(dh.strftime("%Y%m%d%H%M%S"))
        d_now = datetime.now()
        d_now = int(d_now.strftime("%Y%m%d%H%M%S"))
        if dh <= d_now:
            dest.available=False
            dest.save()
        else:
            dest.available=True
            dest.save()
    dlist = list(dict.fromkeys(dlist))
    #listDestination1 = Trajet.objects.all().annotate(Count('arrivee__localite',distinct=True))
    return render(request,'mainpage.html',{'listDestination':listDestination,'dlist':dlist,})

def listTrajets(request):
    #listDestination = Trajet.objects.all()
    listT = Trajet.objects.filter(available=True)
    # for var in listT:
    #     if var.heure_depart != datetime.now():
    #         var.available = False
    #         var.save()
    # listT = Trajet.objects.filter(available=False)
    
    return render(request,'AllTrajets.html',{'listT':listT,})

def listTrajets_voiture(request, id=None):
    trajet_voiture= Trajet.objects.filter(voiture_id=id)
    return render(request,'AllTrajets.html',{'trajet_voiture':trajet_voiture,})

def listVehicule(request):
    listdesVehicule = Vehicule.objects.all()
    listdestrajets = Trajet.objects.all()
    return render(request,'AllVehicule.html',{'listdesVehicule':listdesVehicule,'listdestrajets':listdestrajets})

def DestDispo(request):
    all_trajects_queryset_list = Trajet.objects.filter(available=True)
    destinationChoisie = request.GET.get('destination')
    if destinationChoisie != 'all':
        #localitequartier = destinationChoisie.split('-')
        dest_trajects_queryset_list = all_trajects_queryset_list.filter(Q(arrivee__localite__icontains=destinationChoisie))
        for dst in dest_trajects_queryset_list:
            if dst.vehicule.nbPlace==0:
                dst.available=False
                dst.save()
        return render(request,'listPerDest.html',
            {'dest_trajects_queryset_list':dest_trajects_queryset_list,
            'destinationChoisie':destinationChoisie},)
    else:
        for dst in all_trajects_queryset_list:
            if dst.vehicule.nbPlace==0:
                dst.available=False
                dst.save()
        return render(request,'listPerDest.html',
            {'all_trajects_queryset_list':all_trajects_queryset_list,
            'destinationChoisie':destinationChoisie,})

def Test(request):
    traID = request.GET.get('idField')
    trajetData = get_object_or_404(Trajet, id=traID)
    
    form = ReservationForm()
    return render(request,'prestation.html',{'form':form,})

@login_required(redirect_field_name='list_reservation')
def ClientReservation(request):
    traID = request.GET.get('idField')
    traID = int(traID)
    #trajetData = Trajet.objects.get(pk=traID)
    trajetData = get_object_or_404(Trajet, pk=traID)
    typ = trajetData.vehicule.id
    #CarData = Vehicule.objects.get(pk=typ)
    CarData = get_object_or_404(Vehicule, pk=typ)
    plcInit = CarData.nbPlace
    plcPrise = request.GET.get('nbPlace_Reservee')
    plcPrise = int(plcPrise)
    
    if plcInit != 0:
        plcRestante = plcInit - plcPrise
        CarData.nbPlace = plcRestante
        if plcRestante == 0:
            trajetData.available = False
            trajetData.save()
        else:
            CarData.save()
    else:
        trajetData.available = False
        trajetData.save()
        
    #trajetData = Trajet.objects.get(id=traID)
    
    if request.method == "GET":
        form = ReservationForm(request.GET)
        dep = form.is_valid()
        if form.is_valid():
            form.save(commit=True)
            #return redirect('listDest')
            return render(request, 'prestation.html', {'trajetData':trajetData,'CarData':CarData,
                'plcPrise':plcPrise,})
        # return render(request, 'cookValidation.html',)
    else:
        traID = 'DAOUDA IS FINE'
        return render(request, 'contact.html')
#@permission_required('blablaCar.NousContactez.can_add_nous_contactez', login_url='/listvehicule/')
def Contact(request):
    nous = NousContactez.objects.all()
    return render(request,'contact.html',{'nous':nous,})

def CookiesPolicy(request):
    return render(request,'cookValidation.html',{})

def ConditionUtilisation(request):
    return render(request,'conditionUtil.html',{})

def multiple_forms(request):
    if request.method == 'POST':
        contact_form = SignUpForm(request.POST)
        login_form = LoginForm(request.POST)
        if contact_form.is_valid() or login_form.is_valid():
          if request.POST.get('submit') == 'sign_in':
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
              user = authenticate(username=username, password=password)
              if user:
                login(request,user)
                #return redirect('/')
              else:
                return render(request, 'signupLogin.html', {'login_form': login_form})
          if request.POST.get('submit') == 'sign_up':
            contact_form.save()
            username = contact_form.cleaned_data.get('username')
            raw_password = contact_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
          else:
            return render(request, 'signupLogin.html', {'contact_form': contact_form})
        else:
          contact_form = SignUpForm()
          login_form = LoginForm()
    else:
        contact_form = SignUpForm()
        login_form = LoginForm()

    return render(request, 'signupLogin.html', {
        'contact_form': contact_form,
        'login_form': login_form,
    })

def loginUser(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
              user = authenticate(username=username, password=password)
              if user:
                login(request,user)
                #return redirect('/')
              else:
                login_form = LoginForm()
        else:
            login_form = LoginForm()
    else:
        login_form = LoginForm()
        return render(request, 'LoginForm.html', {'login_form': login_form})

def registration(request):
    if request.method == 'POST':
        contact_form = SignUpForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
        username = contact_form.cleaned_data.get('username')
        raw_password = contact_form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        group = Group.objects.get(name='Client')
        user.groups.add(group)
        login(request, user)
        if user.groups.filter(name = 'Client').exists():
            return redirect('/')
        else:
            contact_form = SignUpForm()
            return render(request, 'registrationForm.html', {'contact_form': contact_form})
    else:
        contact_form = SignUpForm()
        return render(request, 'registrationForm.html', {'contact_form': contact_form})

def listReservation(request):
    resrv = Reservation.objects.all().order_by('-created')
    return render(request,'listResev.html',{'resrv':resrv,})

def aproposdenous(request):
    return render(request,'apropos.html',{})
