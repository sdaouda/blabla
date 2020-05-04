"""blablaCar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from blablaCar import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='/acceuil/', permanent=True)),
    #url(r'^$', views.product_list, name='product_list'),
    url(r'^acceuil/', views.listDestination, name='listDest',),
    url('accounts/', include('django.contrib.auth.urls')),
    #url('login/' ,auth_views.PasswordChangeView.as_view(template_name='login.html'),),
    url(r'^result$', views.DestDispo, name='Dest_search_list'),
    url(r'^trajet/(?P<pk>\d+)/update/', views.TrajetUpdate.as_view(), name='traj_update'),
    #url(r'^(?P<id>\d+)/delete/$', views.trajet_delete_view, name='delete1'),
    url(r'^(?P<pk>\d+)/deletevehicule/$', views.VehiculeDelete.as_view(), name='delete2'),
    url(r'^(?P<pk>\d+)/deleteTrajet/$', views.TrajetDelete.as_view(), name='delete1'),
    url(r'^(?P<id>\d+)/$', views.DestinationDetails, name='dest_detail'),
    url(r'^maj_vehicule/(?P<pk>\d+)/update/', login_required(views.VehiculeUpdate.as_view()), name='maj_vehicule'),
    url(r'^resume/$', login_required(views.ClientReservation), name='clientResv'),
    url(r'^listdestrajets/$' , views.listTrajets ,name = 'listdestrajets'),
    url(r'^listvehicule/$' , views.listVehicule ,name = 'listvehicule'),
    url(r'^contact/$' , views.Contact ,name = 'nouscontacter'),
    url(r'^policy/$' , views.CookiesPolicy ,name = 'cookiespolicy'),
    url(r'^condition/$' , views.ConditionUtilisation ,name = 'condUtil'),
    #url(r'^logindata/$' , views.loginUser ,name = 'logindata'),
    url(r'^registration/$' , views.registration ,name = 'register'),
    url(r'^agent/$' , views.CreerTrajet ,name = 'creertrajet'),
    #url(r'^vehicule/$' ,views.VehiculeCreate.as_view(),name = 'vehicule'),
    url(r'^vehicule/$' , login_required(views.VehiculeCreate.as_view()),name = 'vehicule'),
    url(r'^vehiculefinder/$' , views.TrouverVehi ,name = 'vehiculefinder'),
    url(r'^resultat_voiture/$' , views.DisplayVehi ,name = 'resultat_voiture'),
    url(r'^list_reservation/$' , views.listReservation ,name = 'list_reservation'),
    url(r'^apropos/$' , views.aproposdenous ,name = 'apropos'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)