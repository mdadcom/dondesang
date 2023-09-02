from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .form import *
from .models import *
from django.views import View
from django.template.loader import render_to_string
from django.core.paginator import(Paginator, EmptyPage, PageNotAnInteger)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from reportlab.pdfgen import canvas
import json
from weasyprint import HTML
from weasyprint import HTML, CSS

def home(request):
    
    pays = Pays.objects.all()
    region=Region.objects.all()
    ville=Ville.objects.all()
    context={
        'pays':pays,
        'region':region,
        'ville':ville,
    }
    return render(request, 'index.html', context)
def home2(request):
    
    pays = Pays.objects.all()
    region=Region.objects.all()
    ville=Ville.objects.all()
    context={
        'pays':pays,
        'region':region,
        'ville':ville,
    }
    return render(request, 'index2.html', context)

def region(request, pays_pk):
    pays=Pays.objects.get(pk=pays_pk)
    #form=RegionForm()

    return render(request, 'region.html',{'pays':pays})

def ville(request, region_pk):
    region=Region.objects.get(pk=region_pk)
    
    return render(request, 'ville.html',{'region':region})

def add_pays(request):
    
    if request.method == 'POST':
        nom=request.POST.get('nom')
        code=request.POST.get('code')
        newpays = Pays.objects.create(nom=nom,code=code)
   
    return redirect("home2")
def ad_pays(request):
    if request.method == 'POST':
        nom=request.POST.get('nom')
        code=request.POST.get('code')
        newpays = Pays.objects.create(nom=nom,code=code)
   
    return render(request, 'don/ad_pays.html')

def affregion(request):
    pays_list=Pays.objects.all()
    return render(request, 'don/ad_region.html',{'pays_list':pays_list})

def ad_region(request):
    
    if request.method=="POST":
        pays_id=request.POST.get('pays')
        pays=Pays.objects.get(id=pays_id)
        nom=request.POST.get('nom')
        region=Region.objects.create(pays=pays,nom=nom)
        
        return redirect('affregion')
    
    
def ad_ville(request):
    region_list=Region.objects.all()
    if request.method=="POST":
        region_pk=request.POST.get('region')
        nom=request.POST.get('nom')
        region= get_object_or_404(Region, pk=region_pk)
        ville=Ville.objects.create(region=region,nom=nom)
        
    return render(request, 'don/ad_ville.html',{'region_list':region_list})

def affcong(request):
    pays = Pays.objects.all()
    region=Region.objects.all()
    ville=Ville.objects.all()
    context={
        'pays':pays,
        'region':region,
        'ville':ville,
    }
    return render(request, 'don/affcong.html',context)
    
def add_region(request, pays_pk):
    
    if request.method=="POST":
        pays=Pays.objects.get(pk=pays_pk)
        nom=request.POST.get('nom')
        region=Region.objects.create(pays=pays,nom=nom)
        return redirect("region", pays_pk=pays_pk)
    
#def add_region(request):

#    if request.method=="POST":
#        forms=RegionForm(request.POST)
#        if forms.is_valid():
#            forms.save()
#        return redirect("ville")
#    else:
#        forms=RegionForm()
        
#        return redirect('ville')

#def add_ville(request):
#    if request.method=="POST":
#        form=VilleForm(request.POST)
#        if form.is_valid():
#            form.save()
#        return redirect("home")
#    else:
#        form=VilleForm()
        
#        return redirect('home')
    
def add_ville(request, region_pk):
    if request.method=="POST":
        region=Region.objects.get(pk=region_pk)
        nom=request.POST.get('nom')
        ville=Ville.objects.create(region=region,nom=nom)
        return redirect("home2")
    else:
        
        
        return render(request, 'ville.html',{'region':region})
    
def edit(request, pays_pk):
    form=PaysForm()
    pays= Pays.objects.get(pk=pays_pk)
    return render(request, 'edit.html',{'pays':pays, 'form':form})

def update_pays(request, pays_pk):
    pays= Pays.objects.get(pk=pays_pk)
    form=PaysForm(request.POST, instance=pays)
    if form.is_valid():
        form.save()
    return redirect('home')

def delete_pays(request, pays_pk):
    pays= Pays.objects.get(pk=pays_pk)
    pays.delete()
    return redirect('home')

def edite(request, region_pk):
    region= get_object_or_404(Region, pk=region_pk)
    form=RegionForm(request.POST or None, instance=region)
    return render(request, 'edite.html',{'region':region, 'form':form})

def update_region(request, region_pk):
    region= get_object_or_404(Region, pk=region_pk)
    form=RegionForm(request.POST or None, instance=region)
    if form.is_valid():
        form.save()
    return redirect('home')

def delete_region(request, region_pk):
    region= Region.objects.get(pk=region_pk)
    region.delete()
    return redirect('home')

def edites(request, ville_pk):
    ville= get_object_or_404(Ville, pk=ville_pk)
    form=VilleForm(request.POST or None, instance=ville)
    return render(request, 'edites.html',{'ville':ville, 'form':form})

def update_ville(request, ville_pk):
    ville= Ville.objects.get(pk=ville_pk)
    form=VilleForm(request.POST, instance=ville)
    if form.is_valid():
        form.save()
    return redirect('home')

def delete_ville(request, ville_pk):
    ville= Ville.objects.get(pk=ville_pk)
    ville.delete()
    return redirect('home')


def affzone(request):
    ville=Ville.objects.all()
    context={
            'ville':ville,
        }
    return render(request,'don/zone.html',context)

def zone(request):
    
    if request.method == 'POST':
        name= request.POST.get('name')
        ville_pk=request.POST.get('ville')
        ville=Ville.objects.get(pk=ville_pk)
        addzone=Zone.objects.create(name=name,ville=ville)
     
        
    return redirect('affzone')

def collect(request, ville_pk):
    ville=get_object_or_404(Ville, pk=ville_pk)
    collects_lis=ville.collects_set.filter(ferme=False)
    context={
        'ville':ville,
        'collects_lis':collects_lis,
    }
    return render(request, 'don/collect.html',context)

def affcol(request):
    collects_ferme=Collects.objects.filter(ferme=True)
    context={
        'collects_ferme':collects_ferme,
    }
    return render(request, 'don/affcol.html',context)

def affcollect(request):
    collects_lis=Collects.objects.filter(ferme=False)
    zone=Zone.objects.all()
    context={
        'collects_lis':collects_lis,
        'zone':zone
    }
    return render(request, 'don/collects.html',context)

def collects(request):
    
    if request.method=="POST":
        zone_pk=request.POST.get('zone')
        zone=Zone.objects.get(pk=zone_pk)
        date=request.POST.get('date')
        newcollect=Collects.objects.create(date=date,zone=zone)
        
    
    return redirect('affcollect')

#def add_collect(request, ville_pk):
    #if request.method=="POST":
       
     #   date=request.POST.get('date')
    #    newcollect=Collects.objects.create(date=date)
   # return redirect('collect', ville_pk=ville_pk)

def editcol(request, collects_pk):
    collects=get_object_or_404(Collects, pk=collects_pk)
    form=CollectsForm(request.POST or None, instance=collects)
    return render(request, 'don/editi.html',{'collects':collects, 'form':form})

def update_collects(request, collects_pk):
    collects= get_object_or_404(Collects, pk=collects_pk)
    form=CollectsForm(request.POST, instance=collects)
    if form.is_valid():
        form.save()
    return redirect('home')

def delete_collects(request, collects_pk):
    collects= Collects.objects.get(pk=collects_pk)
    collects.delete()
    return redirect('home')

def ferme_col(request, collects_id):
    collects =Collects.objects.get(id=collects_id)
    collects.ferme = True
    collects.save()
    
    return redirect('affcol')
    
#def donneur (request, collects_pk):
    #collects=Collects.objects.get(pk=collects_pk)
    #numero_cnib= request.GET.get("numero_cnib")
    #donneur= Donneur.objects.filter(numero_cnib=numero_cnib).first()
    #form=DonneurForm
    #ville=Ville.objects.all()
    #type=Type.objects.all()
    #context={
    #    'form':form,
    #    'ville':ville,
    #    'type':type,
    #    'collects':collects,
    #    'donneur':donneur,
    #}
    
    #return render(request,'don/donneur.html',context)

def donneurs (request):
    
    ville=Ville.objects.all()
    type=Type.objects.all()
    context={
        'donneurs':donneurs,
        'ville':ville,
        'type':type,
        
    }
    
    return render(request,'don/donneurs.html',context)

def don(request):
    return render(request,'don/don.html')

def prelev(request):
    donneur_lis=Donneur.objects.all()
    context={
        'donneur_lis':donneur_lis,
    }
    return render(request,'don/prelev.html')

def ent(request):
    collects_lis=Collects.objects.filter(ferme=False)
    context={
        'collects_lis':collects_lis,
    }
    return render(request, 'don/collect.html',context)

#def ad_donneur(request):
 #   if request.method=="POST":
  #      numero_cnib = request.POST.get('numero_cnib')
   #     nom = request.POST.get('nom') 
    #    nom_de_jeune = request.POST.get('nom_de_jeune')
     #   prenom = request.POST.get('prenom')
      #  date_de_naissance = request.POST.get('date_de_naissance')
       # age = request.POST.get('age')
        #lieu_de_naissance = request.POST.get('lieu_de_naissance')
        #sexe = request.POST.get('sexe')
        #profession = request.POST.get('profession')
        #ville_pk=request.POST.get('ville')
        #ville=Ville.objects.get(pk=ville_pk)
        #secteur = request.POST.get('secteur')
        #tel = request.POST.get('tel')
        #email = request.POST.get('email')
        #type_pk=request.POST.get('type')
        #type=Type.objects.get(pk=type_pk)
      
        #Donneur.objects.get_or_create(numero_cnib=numero_cnib, nom=nom, nom_de_jeune=nom_de_jeune, prenom=prenom, date_de_naissance=date_de_naissance,age=age,
         #                               lieu_de_naissance=lieu_de_naissance,sexe=sexe, profession=profession, ville=ville, secteur=secteur, tel=tel,
          #                              email=email, type=type)
        
        #data = {
         #   'donneur': {
          #      'pk': donneur.pk,
           #     'numero_cnib': donneur.numero_cnib,
            #    'nom': donneur.nom,
             #   'nom_de_jeune': donneur.nom_de_jeune,
              #  'prenom': donneur.prenom,
               # 'date_de_naissance': donneur.date_de_naissance,
                #'age': donneur.age,
                #'lieu_de_naissance': donneur.lieu_de_naissance,
                #'sexe': donneur.sexe,
                #'profession': donneur.profession,
                #'ville': {'ville':ville.nom,},
                #'secteur': donneur.secteur,
                #'tel': donneur.tel,
                #'email': donneur.email,
                #'type': {'type':type.nom,},
            #},
        #}

        #return JsonResponse(data)
        
    #return redirect("details")
    
def ad_donneur(request):
   if request.method=="POST":
        numero_cnib = request.POST.get('numero_cnib')
        nom = request.POST.get('nom') 
        nom_de_jeune = request.POST.get('nom_de_jeune')
        prenom = request.POST.get('prenom')
        date_de_naissance = request.POST.get('date_de_naissance')
        age = request.POST.get('age')
        lieu_de_naissance = request.POST.get('lieu_de_naissance')
        sexe = request.POST.get('sexe')
        profession = request.POST.get('profession')
        ville_pk=request.POST.get('ville')
        ville=Ville.objects.get(pk=ville_pk)
        secteur = request.POST.get('secteur')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        type_pk=request.POST.get('type')
        type=Type.objects.get(pk=type_pk)
        
        
        donneur, created= Donneur.objects.get_or_create(numero_cnib=numero_cnib, nom=nom, nom_de_jeune=nom_de_jeune, prenom=prenom, date_de_naissance=date_de_naissance,age=age,
                                        lieu_de_naissance=lieu_de_naissance,sexe=sexe, profession=profession, ville=ville, secteur=secteur, tel=tel,
                                        email=email, type=type)
        
        donneur.save()
        
        request.session['donneur_id'] = donneur.id
       
        data={'donneur':{
            'pk': donneur.pk,
            'numero_cnib': donneur.numero_cnib,
            'nom': donneur.nom,
            'nom_de_jeune': donneur.nom_de_jeune,
            'prenom': donneur.prenom,
            'date_de_naissance': donneur.date_de_naissance,
            'age': donneur.age,
            'lieu_de_naissance': donneur.lieu_de_naissance,
            'sexe': donneur.sexe,
            'profession': donneur.profession,
            'ville': {'ville':ville.nom,},
            'secteur': donneur.secteur,
            'tel': donneur.tel,
            'email': donneur.email,
            'type': {'type':type.nom,},
            
        }
                }
        
        return redirect('entretien')
        #return JsonResponse(data)

def add_donneur(request, collects_pk):
    collects = Collects.objects.get(pk=collects_pk)
    ville=Ville.objects.all()
    type=Type.objects.all()
    numero_cnib= request.GET.get("numero_cnib")
    query= Donneur.objects.filter(numero_cnib=numero_cnib).first()
    if request.method=="POST":
        collects_zone = [x.zone for x in Collects.objects.all()]
        collects_ids=[Collects.objects.get(pk=collects_pk)]
        numero_cnib = request.POST.get('numero_cnib')
        nom = request.POST.get('nom') 
        nom_de_jeune = request.POST.get('nom_de_jeune')
        prenom = request.POST.get('prenom')
        date_de_naissance = request.POST.get('date_de_naissance')
        age = request.POST.get('age')
        lieu_de_naissance = request.POST.get('lieu_de_naissance')
        sexe = request.POST.get('sexe')
        profession = request.POST.get('profession')
        ville_pk=request.POST.get('ville')
        ville=Ville.objects.get(pk=ville_pk)
        secteur = request.POST.get('secteur')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        type_pk=request.POST.get('type')
        type=Type.objects.get(pk=type_pk)
        donneur= Donneur.objects.filter(numero_cnib=numero_cnib)
        donneur, created= Donneur.objects.get_or_create(numero_cnib=numero_cnib, nom=nom, nom_de_jeune=nom_de_jeune, prenom=prenom, date_de_naissance=date_de_naissance,age=age,
                                        lieu_de_naissance=lieu_de_naissance,sexe=sexe, profession=profession, ville=ville, secteur=secteur, tel=tel,
                                        email=email, type=type)
    
        
        donneur.collects.add(Collects.objects.get(pk=collects_pk))
        donneur.save()
        request.session['donneur_id'] = donneur.id
    
        data = {
            'collects': {
                'pk': collects.pk,
                
                
                'date':collects.date,
            },
            'donneur': None
        }

        if donneur:
            data['donneur'] = {
                'pk': donneur.pk,
                'numero_cnib': donneur.numero_cnib,
                'nom': donneur.nom,
                'nom_de_jeune': donneur.nom_de_jeune,
                'prenom': donneur.prenom,
                'date_de_naissance': donneur.date_de_naissance,
                'age': donneur.age,
                'lieu_de_naissance': donneur.lieu_de_naissance,
                'sexe': donneur.sexe,
                'profession': donneur.profession,
                'ville': {'ville':ville.nom,},
                'secteur': donneur.secteur,
                'tel': donneur.tel,
                'email': donneur.email,
                'type': {'type':type.nom,},
                
            }
            
        return redirect('entretien')
            
    return render(request, "don/donneur.html",{
                    'collects':collects,
                    'ville':ville,
                    'type':type,
                    
                    #'msg':'Déja Enregistre',
                    'query':query,
                    
                })
        #return redirect('detail', collects_pk=collects_pk,)
        #return redirect("detail", collects_pk=collects_pk)
       
#@csrf_exempt
#def add_donneur(request, collects_pk):
#    collects = Collects.objects.get(pk=collects_pk)
#    data = {}
#    if request.method == 'POST':
#        form = DonneurForm(request.POST)
#        if form.is_valid():
#            numero_cnib = form.cleaned_data['numero_cnib']
#            nom = form.cleaned_data['nom']
#            nom_de_jeune = form.cleaned_data['nom_de_jeune']
#            prenom = form.cleaned_data['prenom']
#            date_de_naissance = form.cleaned_data['date_de_naissance']
#            age = form.cleaned_data['age']
#            lieu_de_naissance = form.cleaned_data['lieu_de_naissance']
#            sexe = form.cleaned_data['sexe']
#            profession = form.cleaned_data['profession']
#            ville = form.cleaned_data['ville']
#            secteur = form.cleaned_data['secteur']
#            tel = form.cleaned_data['tel']
#            email = form.cleaned_data['email']
#            type = form.cleaned_data['type']

#            donneur, created = Donneur.objects.get_or_create(
#                numero_cnib=numero_cnib,
#                nom=nom,
#                nom_de_jeune=nom_de_jeune,
#                prenom=prenom,
#                date_de_naissance=date_de_naissance,
#                age=age,
#                lieu_de_naissance=lieu_de_naissance,
#                sexe=sexe,
#                profession=profession,
#                ville=ville,
#                secteur=secteur,
#                tel=tel,
#                email=email,
#                type=type,
#            )

#            donneur.collects.add(collects)
#            donneur.save()

#            data = {
#                'collects': {
#                    'pk': collects.pk,
#                    'name': collects.name,
#                    'ville': {'nom': ville.nom},
#                    'date': collects.date,
#                },
#                'donneur': {
#                    'pk': donneur.pk,
#                    'numero_cnib': donneur.numero_cnib,
#                    'nom': donneur.nom,
#                    'nom_de_jeune': donneur.nom_de_jeune,
#                    'prenom': donneur.prenom,
#                    'date_de_naissance': donneur.date_de_naissance,
#                    'age': donneur.age,
#                    'lieu_de_naissance': donneur.lieu_de_naissance,
#                    'sexe': donneur.sexe,
#                    'profession': donneur.profession,
#                    'ville': donneur.ville,
#                    'secteur': donneur.secteur,
#                    'tel': donneur.tel,
#                    'email': donneur.email,
#                    'type': donneur.type,
#                },
#            }
    
#            return JsonResponse(data)
#        else:
#            data = {'error': form.errors}
#    return JsonResponse(data)

#def donneur_details(request, numero_cnib):
 #   donneur = get_object_or_404(Donneur, numero_cnib=numero_cnib)
 #   data = {
 #       'numero_cnib': donneur.numero_cnib,
 #       'nom': donneur.nom,
 #       'nom_de_jeune': donneur.nom_de_jeune,
 #       'prenom': donneur.prenom,
 #       'date_de_naissance': donneur.date_de_naissance.strftime('%Y-%m-%d'),
 #       'age': donneur.age,
 #       'lieu_de_naissance': donneur.lieu_de_naissance,
 #       'sexe': donneur.sexe,
 #       'profession': donneur.profession,
 #       'ville': donneur.ville,
 #       'secteur': donneur.secteur,
 #       'tel': donneur.tel,
 #       'email': donneur.email,
 #       'type': donneur.type,
  #  }
  #  return JsonResponse(data)


    
def detail(request, collects_pk):
    collects=get_object_or_404(Collects, pk=collects_pk)
    donneur=collects.donneur_set.all()
    collects_lis=Collects.objects.all()
    p= Paginator(collects.donneur_set.all(), 2)
    page = request.GET.get('page')
    donne= p.get_page(page)
    request.session['collects_id'] = collects.id
    return render(request, 'don/detail.html',{'donneur':donneur, 'collects':collects,'collects_lis':collects_lis, 'donne':donne})

def details(request):
    
    donneur=Donneur.objects.all()
   
    return render(request, 'don/details.html',{'donneur':donneur,})

def editdo (request, donneur_pk):
    donneur=Donneur.objects.get(pk=donneur_pk)
    entretien=Entretien.objects.get(pk=donneur_pk)
    form=DonneurForm(request.POST or None, instance=donneur)
    form1=EntretienForm(request.POST or None, instance=entretien)
    ville=Ville.objects.all()
    type=Type.objects.all()
    return render(request, 'don/editdo.html',{'donneur':donneur, 'entretien':entretien,'form':form, 
                                              'form1':form1, 
                                              'ville':ville, 'type':type})

def update_donneur(request, donneur_pk):
    donneur=get_object_or_404(Donneur, pk=donneur_pk)
    entretien=get_object_or_404(Entretien, pk=donneur_pk)
    form=DonneurForm(request.POST or None, instance=donneur)
    form1=EntretienForm(request.POST or None, instance=entretien)
    if form.is_valid():
        form.save()
        if form1.is_valid():
            form1.save() 
    return redirect("home")

def delete_donneur(request, donneur_pk):
    donneur=Donneur.objects.get(pk=donneur_pk)
    donneur.delete()
    return redirect("home")


class LoadDonneurView(View):
    def get(self, request):
        numero_cnib = request.GET.get('numero_cnib', None)
        donneur = get_object_or_404(Donneur, numero_cnib=numero_cnib)

        data = {
            'nom': donneur.nom,
            'nom_de_jeune': donneur.nom_de_jeune,
            'prenom': donneur.prenom,
            'date_de_naissance': donneur.date_de_naissance.strftime('%Y-%m-%d') if donneur.date_de_naissance else '',
            'age': donneur.age,
            'lieu_de_naissance': donneur.lieu_de_naissance,
            'sexe': donneur.sexe,
            'profession': donneur.profession,
            
            'secteur': donneur.secteur,
            'tel': donneur.tel,
            'email': donneur.email,
            
        }
        
        return JsonResponse({'donneur': data})
    
#def load_donneur(request):
 #   numero_cnib = request.GET.get("numero_cnib")
  #  donneur = Donneur.objects.filter(numero_cnib=numero_cnib).first()
   # data = {}
    #if donneur:
    
     #   data['numero_cnib'] = donneur.numero_cnib
      #  data['nom'] = donneur.nom
       # data['nom_de_jeune'] = donneur.nom_de_jeune
        #data['prenom'] = donneur.prenom
        #data['date_de_naissance'] = donneur.date_de_naissance
        #data['age'] = donneur.age
        #data['lieu_de_naissance'] = donneur.lieu_de_naissance
        #data['sexe'] = donneur.sexe
        #data['profession'] = donneur.profession
        
        #data['secteur'] = donneur.secteur
        #data['tel'] = donneur.tel
        #data['email'] = donneur.email
       
        #data['donneur'] = True
       
    #else:
     #   data['donneur'] = False
    

    #return JsonResponse(data)
    
def entretien(request):
    donneur_id = request.session.get('donneur_id')
    donneur = Donneur.objects.get(id=donneur_id)
    if request.method == 'POST':
        donneur_nom = [x.nom for x in Donneur.objects.all()]
        donneur_ids=[Donneur.objects.get(pk=donneur_id)]
        date_du_jour= request.POST.get('date_du_jour')
        numero= request.POST.get('numero')
        collecte= request.POST.get('collecte')
        premier= request.POST.get('premier')
        si_premier= request.POST.get('si_premier')
        en_couple= request.POST.get('en_couple')
        en_couple_oui=request.POST.get('en_couple_oui')
        en_couple_non=request.POST.get('en_couple_non')
        sante=request.POST.get('sante')
        affections=request.POST.getlist('affections')
        transfusion=request.POST.get('transfusion')
        drogue=request.POST.get('drogue')
        tatou=request.POST.get('tatou')
        infection=request.POST.get('infection')
        exposition= request.POST.get('exposition')
        relations=request.POST.get('relations')
        chirgi=request.POST.get('chirgi')
        n_partenaire= request.POST.get('n_partenaire')
        enceinte= request.POST.get('enceinte')
        acupuncture= request.POST.get('acupuncture')
        sut_plaies= request.POST.get('sut_plaies')
        partenaire_s=request.POST.get('partenaire_s')
        vaccin = request.POST.get('vaccin')
        auvaccin = request.POST.get('auvaccin')
        s_dentaire=request.POST.get('s_dentaire')
        fievre=request.POST.get('fievre')
        plaies_ou=request.POST.get('plaies_ou')
        medicament=request.POST.get('medicament')
        aumedicament=request.POST.get('aumedicament')
        medicament_p=request.POST.get('medicament_p')
        date_de_p= request.POST.get('date_de_p')
        motif_p_medicament= request.POST.get('motif_p_medicament')
        enfant=request.POST.get('enfant')
        enceint_actu=request.POST.get('enceint_actu')
        en_regle=request.POST.get('en_regle')
        resultat_p=request.POST.get('resultat_p')
        si_resultat=request.POST.get('si_resultat')
        le_resultat=request.POST.get('le_resultat')
        poid=request.POST.get('poid')
        taux_hd=request.POST.get('taux_hd')
        ta=request.POST.get('ta')
        consentement=request.POST.getlist('consentement')
        apte=request.POST.get('apte')
        code_ci=request.POST.get('code_ci')
        identification=request.POST.get('identification')
        entretien, created = Entretien.objects.get_or_create(date_du_jour=date_du_jour,numero=numero,collecte=collecte,premier=premier, si_premier=si_premier,
                                             en_couple=en_couple,en_couple_oui=en_couple_oui,en_couple_non=en_couple_non, sante=sante, 
                                             affections=affections,transfusion=transfusion, drogue=drogue, tatou=tatou, infection=infection, exposition=exposition,
                                             relations=relations, chirgi=chirgi, n_partenaire=n_partenaire, enceinte=enceinte, acupuncture=acupuncture,
                                             sut_plaies=sut_plaies, partenaire_s=partenaire_s, vaccin=vaccin, auvaccin=auvaccin, s_dentaire=s_dentaire, fievre=fievre, plaies_ou=plaies_ou,
                                             medicament=medicament, aumedicament=aumedicament,medicament_p=medicament_p, date_de_p=date_de_p, motif_p_medicament=motif_p_medicament, enfant=enfant, 
                                             enceint_actu=enceint_actu, en_regle=en_regle, resultat_p=resultat_p,si_resultat=si_resultat,le_resultat=le_resultat, 
                                             poid=poid, taux_hd=taux_hd, ta=ta, consentement=consentement,apte=apte,code_ci=code_ci,identification=identification)
        entretien.donneur.add(Donneur.objects.get(pk=donneur_id))
        entretien.save()
        if not created:
            message = 'Vous avez déjà donné votre sang dans ce lieu de collecte.'
            return HttpResponse(message)
        request.session['entretien_id'] = entretien.id
        request.session['apte'] = apte
        return redirect('predon')
    
    else:
        
        return render(request, 'don/entretien.html', {'donneur':donneur,})



def predon(request):
    
    entretien_id = request.session.get('entretien_id')
    entretien = Entretien.objects.get(id=entretien_id)
    apte = request.session.get('apte')
    if request.method == 'POST':
        entretien_numero = [x.numero for x in Entretien.objects.all()]
        entretien_ids=[Entretien.objects.get(pk=entretien_id)]
        apte=request.POST.get('apte')
        q_preleve= request.POST.get('q_preleve')
        preparation= request.POST.get('preparation')
        inapte= request.POST.get('inapte')
        code_ci= request.POST.get('code_ci')
        identification= request.POST.get('identification')
        predon= Predon.objects.create(apte=apte, q_preleve=q_preleve, preparation=preparation, 
                                      inapte=inapte, code_ci=code_ci, identification=identification)
        predon.entretien.add(Entretien.objects.get(pk=entretien_id))
        predon.save()
        request.session['predon_id'] = predon.id
        return redirect('preleve')
    else:
        context={
            'entretien':entretien,
            'apte':apte,
            }
        return render(request,'don/predon.html',context )
    
def preleve(request):
    predon_id = request.session.get('predon_id')
    predon = Predon.objects.get(id=predon_id)
    if request.method == 'POST':
        predon_apte = [x.apte for x in Predon.objects.all()]
        predon_ids=[Predon.objects.get(pk=predon_id)]
        heur_p=request.POST.get('heur_p')
        dure_p=request.POST.get('dure_p')
        quantite_p=request.POST.get('quantite_p')
        poche= request.POST.get('poche')
        observation= request.POST.get('observation')
        identif_p= request.POST.get('identif_p')
        preleve=Preleve.objects.create(heur_p=heur_p, dure_p=dure_p, 
                                       quantite_p=quantite_p, poche=poche, 
                                       observation=observation, identif_p=identif_p)
        preleve.predon.add(Predon.objects.get(pk=predon_id))
        preleve.save()
        return redirect('details')
    else:
        return render(request,'don/preleve.html',{'predon':predon})

def extraire_pdf(request, donneur_pk):
    donneur = get_object_or_404(Donneur, id=donneur_pk)
    entretiens = Entretien.objects.filter(donneur=donneur).order_by('-id').first()
    
    # Générer le contenu HTML pour le PDF
    html_content = render_to_string('don/extraire_pdf_page2.html', {'entretiens': entretiens})
    #html_content = render_to_string('don/extraire_pdf.html', {'donneur': donneur})
    
    # Ajouter une page break pour la deuxième page
    #html_content += '<div style="page-break-after: always;"></div>'
    
    # Générer le contenu HTML pour la deuxième page
    #html_content += render_to_string('don/extraire_pdf_page2.html', {'entretiens': entretiens})
    
    css = CSS(string='@page { size: A4; margin: 2mm; }')
    
    # Créer le PDF à partir du contenu HTML
    pdf_file = HTML(string=html_content).write_pdf(stylesheets=[css])
    
    # Renvoyer le PDF en tant que réponse HTTP
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="donneur_{}.pdf"'.format(donneur_pk)
    return response
