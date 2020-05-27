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
from datetime import date
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
from django.contrib.auth.models import User, Group, Permission
from blablaCar.mixins import GroupRequiredMixin
from django.db import transaction
#from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.generic import View
import random
from blablaCar.utils import render_to_pdf
from io import BytesIO


def is_in_groups(user,group):
    return user.groups.filter(name = group).exists()

#@login_required(login_url='loginuser')
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
    fields = ['nom_conducteur','numero_conducteur1','numero_conducteur2','numero_vehicule','nbPlace',
    'marque','image_vehicule',]
    success_url = '/listvehicule/'

class VehiculeUpdate(UpdateView):
    model = Vehicule
    fields = ['nom_conducteur','numero_conducteur1','numero_conducteur2','numero_vehicule','nbPlace',
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
    # all_trajects_queryset_list = Trajet.objects.filter(available=True)
    all_trajects_queryset_list = Trajet.objects.all()
    destinationChoisie = request.GET.get('destination')
    if destinationChoisie != 'all':
        #localitequartier = destinationChoisie.split('-')
        dest_trajects_queryset_list = all_trajects_queryset_list.filter(Q
            (arrivee__localite__icontains=destinationChoisie))
        # for dst in dest_trajects_queryset_list:
        #     if dst.vehicule.nbPlace==0:
        #         dst.available=False
        #         dst.save()
        return render(request,'listPerDest.html',
            {'dest_trajects_queryset_list':dest_trajects_queryset_list,
            'destinationChoisie':destinationChoisie},)
    else:
        # for dst in all_trajects_queryset_list:
        #     if dst.vehicule.nbPlace==0:
        #         dst.available=False
        #         dst.save()
        return render(request,'listPerDest.html',
            {'all_trajects_queryset_list':all_trajects_queryset_list,
            'destinationChoisie':destinationChoisie,})

def Test(request):
    traID = request.GET.get('idField')
    trajetData = get_object_or_404(Trajet, id=traID)
    
    form = ReservationForm()
    return render(request,'prestation.html',{'form':form,})

#@login_required(login_url='/loginuser/',redirect_field_name='list_reservation')
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
    invoice = random.randint(1,10000)
    if plcInit != 0:
        plcRestante = plcInit - plcPrise
        CarData.nbPlace = plcRestante
        CarData.save()
    if request.method == "GET":
        nomclient = request.GET.get('non_client')
        contactclient = request.GET.get('contact_client')
        form = ReservationForm(request.GET)
        dep = form.is_valid()
        if form.is_valid():
            form.save(commit=True)
            #return redirect('listDest')
            return render(request, 'receipt.html', {'trajetData':trajetData,'CarData':CarData,
                'plcPrise':plcPrise,'invoice':invoice,'nomclient':nomclient,'contactclient':contactclient})
        else:
            data = print(form.errors)
            return render(request, 'test.html',{'data':dep,})
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
        #login_form = LoginForm(request.POST)
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
        nextpage = request.POST.get('nextp')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.info(request, f"You are now logged in as {username}")
                if nextpage == '/agent/':
                    return redirect('/agent/')
                else:
                    return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = LoginForm()
    return render(request,'login.html',{"form":form,})


def listReservation(request):
    resrv = Reservation.objects.all().order_by('-created')
    return render(request,'listResev.html',{'resrv':resrv,})

def aproposdenous(request):
    return render(request,'apropos.html',{})

def receiptview(request):
    return render(request,'finalreceipt.html',{})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def pdf_view(request):
    # fs = FileSystemStorage()
    # filename = 'passwd1.pdf'
    # if fs.exists(filename):
    #     with fs.open(filename) as pdf:
    #         response = HttpResponse(pdf, content_type='application/pdf')
    #         response['Content-Disposition'] = 'attachment; filename="passwd1.pdf"'
    #         return response
    # else:
    #     return HttpResponseNotFound('The requested pdf was not found in our server.')
    if 'pdf' in request.GET:
        response = HttpResponse(content_type='application/pdf')
        today = date.today()
        filename = 'pdf_demo' + today.strftime('%Y-%m-%d')
        response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(filename)
        buffer = BytesIO()
        report = PdfPrint(buffer, 'A4')
        pdf = report.report(weather_period, 'Weather statistics data')
        response.write(pdf)
        return response
def GeneratePdf(request):
    if request.GET:
        trajID = request.GET.get('idTraj')
        plcPrise = request.GET.get('placeP')
        client = request.GET.get('client')
        invoiceNumber = request.GET.get('invoiceNumber')
        contactclient = request.GET.get('contactclient')
        trajID = int(trajID)
        plcPrise = int(plcPrise)
        invoiceNumber = int(invoiceNumber)
        trajetData = get_object_or_404(Trajet, pk=trajID)
        typ = trajetData.vehicule.id
        CarData = get_object_or_404(Vehicule, pk=typ)
        plcInit = CarData.nbPlace
    else:
        trajID = 'non'
    context = {
        "invoice_id": invoiceNumber,
        "Client": client,
        "Trajet":"%s-%s" % (trajetData.depart,trajetData.arrivee),
        "Depart": trajetData.heure_depart,
        "Arrivee": trajetData.heure_arrivee,
        "Nbplace": plcPrise,
        "Prix": trajetData.tarif,
    }
    pdf = render_to_pdf('pdf/invoice.html', context)
    # return HttpResponse(pdf, content_type='application/pdf')
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %(contactclient)
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         traID = request.GET.get('idTraj')
#         context = {
#             "invoice_id": traID,
#             "customer_name": "John Cooper",
#             "amount": 1399.99,
#             "today": "Today",
#         }
#         pdf = render_to_pdf('pdf/invoice.html', context)
#         # return HttpResponse(pdf, content_type='application/pdf')
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Invoice_%s.pdf" %("12341")
#             content = "inline; filename='%s'" %(filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")