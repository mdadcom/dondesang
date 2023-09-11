"""
URL configuration for sang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from dondesang.views import *
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name='home'),
    path('home2', home2,name='home2'),
    path('ad-pays/', ad_pays,name='ad-pays'),
    path('ent/', ent,name='ent'),
    path('prelev/', prelev,name='prelev'),
    path('ad-region/', ad_region,name='ad-region'),
    path('ad-ville/', ad_ville,name='ad-ville'),
    path('affcong/', affcong,name='affcong'),
    path('collects/', collects,name='collects'),
    path('affcol/', affcol,name='affcol'),
    path('donneurs/',donneurs,name='donneurs'),
    path('ad-donneur/',ad_donneur,name='ad-donneur'),
    path('details/',details,name='details'),
    path('region/<int:pays_pk>', region,name='region'),
    path('ville/<int:region_pk>', ville,name='ville'),
    path('add-pays', add_pays,name='add-pays'),
    path('add-region/<int:pays_pk>',add_region,name='add-region'),
    path('add-ville/<int:region_pk>',add_ville,name='add-ville'),
    
    path('edit/<int:pays_pk>',edit,name='edit'),
    path('update-pays/<int:pays_pk>',update_pays,name='update-pays'),
    path('delete-pays/<int:pays_pk>',delete_pays,name='delete-pays'),
    
    path('edite/<int:region_pk>',edite,name='edite'),
    path('update-region/<int:region_pk>',update_region,name='update-region'),
    path('delete-region/<int:region_pk>',delete_region,name='delete-region'),
    
    path('edites/<int:ville_pk>',edites,name='edites'),
    path('update-ville/<int:ville_pk>',update_ville,name='update-ville'),
    path('delete-ville/<int:ville_pk>',delete_ville,name='delete-ville'),
    
    path('affzone',affzone,name='affzone'),
    path('zone',zone,name='zone'),
    
    path('collect/<int:ville_pk>',collect,name='collect'),
    path('affcollect',affcollect,name='affcollect'),
    #path('add-collect/<int:ville_pk>',add_collect,name='add-collect'),
    
    path('editcol/<int:collects_pk>',editcol,name='editcol'),
    path('update-collects/<int:collects_pk>',update_collects,name='update-collects'),
    path('delete-collects/<int:collects_pk>',delete_collects,name='delete-collects'),
    path('ferme/<int:collects_id>',ferme_col,name='ferme'),
    
    #path('donneur/<int:collects_pk>',donneur,name='donneur'),
    path('don',don,name='don'),
    path('add-donneur/<int:collects_pk>',add_donneur,name='add-donneur'),
    #path('api/donneur/<int:numero_cnib>', donneur_details, name='donneur-details'),
    path('detail/<int:collects_pk>',detail,name='detail'),
    
    
    path('editdo/<int:donneur_pk>',editdo,name='editdo'),
    path('update-donneur/<int:donneur_pk>',update_donneur,name='update-donneur'),
    path('delete-donneur/<int:donneur_pk>',delete_donneur,name='delete-donneur'),
    path('load-donneur/',  LoadDonneurView.as_view(),name='load-donneur'),
    
    path('entretien',entretien,name='entretien'),
    path('predon',predon,name='predon'),
    path('preleve',preleve,name='preleve'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('affty',affty,name='affty'),
    path('addty',addty,name='addty'),
]
