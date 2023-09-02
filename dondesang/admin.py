from django.contrib import admin

from .models import *

class AdminPays(admin.ModelAdmin):
    list_display=('nom','code')
    
#class AdminCollects(admin.ModelAdmin):
    #list_display=('date')
    
class AdminDonneur(admin.ModelAdmin):
    list_display=('numero_cnib','nom','prenom','date_de_naissance','lieu_de_naissance','sexe','profession','ville','email','tel',)
    
    
admin.site.register(Pays, AdminPays)
admin.site.register(Region)
admin.site.register(Ville)
admin.site.register(Collects, 
                    #AdminCollects
                    )
admin.site.register(Zone)
admin.site.register(Type)
admin.site.register(Donneur, AdminDonneur)
admin.site.register(Entretien)
admin.site.register(Predon)
admin.site.register(Preleve)