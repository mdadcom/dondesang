
import uuid
import random
import string
import datetime
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField

class Pays(models.Model):
    nom= models.CharField(max_length=100)
    code= models.IntegerField(unique=True)
    date_created= models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'dondesang'
        verbose_name_plural=('Pays')
    
    def __str__(self):
        return self.nom
    
class Region(models.Model):
    pays=models.ForeignKey(Pays,on_delete=models.CASCADE,null=True,blank=True)
    nom=models.CharField(max_length=100)
    date_created= models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'dondesang'
        verbose_name =('Region')
        verbose_name_plural=('Regions')
    
    def __str__(self):
        return self.nom
    
class Ville (models.Model):
    region=models.ForeignKey(Region,on_delete=models.CASCADE,null=True,blank=True)
    nom=models.CharField(max_length=100)
    date_created= models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'dondesang'
        verbose_name =('Ville')
        verbose_name_plural=('Villes')
    
    def __str__(self):
        return self.nom
    
class Zone(models.Model):
    
    name=models.CharField(max_length=100)
    ville=models.ForeignKey(Ville, on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'dondesang'
    def __str__(self):
        return self.name
    
class Collects(models.Model):
    code = models.CharField(max_length=100, unique=True, editable=False)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True,blank=True)
    ferme= models.BooleanField(default=False)
    date_created= models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'dondesang'
        verbose_name =('Collect')
        verbose_name_plural=('Collects')
        
    def generate_code(self):
        date_part = datetime.datetime.now().strftime("%d%m%Y")
        last_collect = Collects.objects.order_by('-id').first()
        if last_collect:
            last_code = int(last_collect.code[-1])
            new_code = last_code + 1
        else:
            new_code = 1
        code = f"{str(self.zone)[:2]}{date_part}{str(new_code).zfill(4)}"
        return code
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

        
    def __str__(self):
            return str(self.zone)

class Type(models.Model):
    nom = models.CharField(max_length=60,null=True,blank=True)

    class Meta:
        app_label = 'dondesang'
    
        
    def __str__(self):
            return str(self.nom)

class Donneur(models.Model):
    class Sexe(models.TextChoices):
        MALE = 'H', 'HOMME'
        FEMELLE = 'F', 'FEMME'
    code = models.CharField(max_length=100, unique=True, editable=False)
    collects=models.ManyToManyField(Collects, blank=True)
    numero_cnib=models.CharField(max_length=60,unique=True)
    nom = models.CharField(max_length=60,null=True,blank=True)
    nom_de_jeune = models.CharField(max_length=60,null=True,blank=True)
    prenom = models.CharField(max_length=60,null=True,blank=True)
    date_de_naissance = models.DateTimeField(null=True,blank=True)
    age=models.CharField(max_length=4,null=True,blank=True)
    lieu_de_naissance = models.CharField(max_length=60,null=True,blank=True)
    sexe =models.CharField(max_length=10, choices=Sexe.choices, null=True, blank=True)
    profession = models.CharField(max_length=60,null=True,blank=True)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    secteur = models.CharField(max_length=80, null=True, blank=True)
    tel = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=80,blank=True)
    type=models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    date_created= models.DateTimeField(auto_now=True)
    
    class Meta:
            app_label = 'dondesang'
            verbose_name =('Donneur')
            verbose_name_plural=('Donneurs')
            db_table='donneur'
            ordering = ['-date_created']
            
    def generate_code(self):
        date_part = datetime.datetime.now().strftime("%d%m%Y")
        last_collect = Collects.objects.order_by('-id').first()
        if last_collect:
            last_code = int(last_collect.code[-1])
            new_code = last_code + 1
        else:
            new_code = 1
        code = f"{self.prenom[:1]}{self.nom[:1]}{date_part}{str(new_code).zfill(2)}"
        return code
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)
    
        
    def __str__(self):
            return str(self.nom)
        
class Entretien(models.Model):
    
    Aff_choices = (
                ('Infarctus','Infarctus'),('Rhumatisme Articulaire','Rhumatisme Articulaire'),
                 ('Diabète sous insuline','Diabète sous insuline'),('Angine de poitrine','Angine de poitrine'),
                 ('Asthme instable(crise-de 6 mois)','Asthme instable(crise-de 6 mois)'),('Dermatose','Dermatose'),
                 ('Troubles cardiaques','Troubles cardiaques'),('Maladie du foie','Maladie du foie'),
                 ('Cancer','Cancer'),('HTA instable','HTA instable'),('Tuberculose','Tuberculose'),
                 ('Autre maladie chronique grave','Autre maladie chronique grave'),('Epilepsie','Epilepsie'),('Drépanocytose(ss,sc,cc,)','Drépanocytose(ss,sc,cc,)'),
                 ('Maladie Neurologique','Maladie Neurologique'),('Trouble de la coagulation sanguine','Trouble de la coagulation sanguine'),
                 ('Aucune','Aucune'),)
    Vaccin= (('Fièvre jaune','Fièvre jaune'),('Rougeole','Rougeole'),('Varicelle','Varicelle'),
             ('Rubéole','Rubéole'),('Typhoïde','Typhoïde'),)
    Medicament_p= (('Antibiotique dans les 07 jours','Antibiotique dans les 07 jours'),
             ('Anti-inflammatoire/Corticoïde dans les 03 jours','Anti-inflammatoire/Corticoïde dans les 03 jours'),
             ('Antipaludéen dans les 14 jour','Antipaludéen dans les 14 jour'),)
    Consentement= (('j_ai bien été informé','j_ai bien été informé'),('je confirme que','je confirme que'),
             ('je consens à donner de mon sang','je consens à donner de mon sang'),('j_accepte que mon sang','j_accepte que mon sang'),
             ('j_ai été informé que','j_ai été informé que'),('Aucune','Aucune'))
    Apte= (('APTE','APTE'),('INAPTE TEMPORAIRE','INAPTE TEMPORAIRE'),('INAPTE DEFINITIVE','INAPTE DEFINITIVE'),)
    
    class Collecte(models.TextChoices):
        FIXE = 'Fixe','Fixe'
        MOBILE = 'Mobile','Mobile'
    class Premier(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Couple(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Oui(models.TextChoices):
        MONOGAMIE='Monogamie','Monogamie'
        POLYGAMIE='Polygamie','Polygamie'
    class Non(models.TextChoices):
        CELIBATAIRE='Celiba','Celiba'
        DIVORCE='Divorce','Divorce'
        VEUF='Veuf','Veuf'
    class Sante(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Transfusion(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Drogue(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Tatou(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Infection(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Exposition(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Relations(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Chirgi(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Enceinte(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Acupuncture(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Sut_plaies(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Partenaire_s(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class S_dentaire(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Fievre(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Plaies_ou(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Medicament(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Enfant(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Enceint_actu(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class En_regle(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Resultat_p(models.TextChoices):
        OUI= 'Oui','Oui'
        NON= 'Non','Non'
    class Resultat(models.TextChoices):
        POSITIF= 'Positifs','Positifs'
        NEGATIF= 'Negatifs','Negatifs'
    
    donneur= models.ManyToManyField(Donneur,blank=True)
    date_du_jour=models.DateTimeField(null=True,blank=True)
    numero= models.IntegerField()
    collecte= models.CharField(max_length=10, choices=Collecte.choices, null=True, blank=True)
    premier= models.CharField(max_length=10, choices=Premier.choices, null=True, blank=True)
    si_premier= models.CharField(max_length=120, null=True, blank=True)
    en_couple= models.CharField(max_length=10, choices=Couple.choices, null=True, blank=True)
    en_couple_oui= models.CharField(max_length=10, choices=Oui.choices, null=True, blank=True)
    en_couple_non= models.CharField(max_length=10, choices=Non.choices, null=True, blank=True)
    sante= models.CharField(max_length=10, choices=Sante.choices, null=True, blank=True)
    affections= MultiSelectField(max_length=250, max_choices=17, choices=Aff_choices, default='Aucune')
    transfusion= models.CharField(max_length=10, choices=Transfusion.choices, null=True, blank=True)
    drogue= models.CharField(max_length=10, choices=Drogue.choices, null=True, blank=True)
    tatou= models.CharField(max_length=10, choices=Tatou.choices, null=True, blank=True)
    infection= models.CharField(max_length=10, choices=Infection.choices, null=True, blank=True)
    exposition= models.CharField(max_length=10, choices=Exposition.choices, null=True, blank=True)
    relations= models.CharField(max_length=10, choices=Relations.choices, null=True, blank=True)
    chirgi= models.CharField(max_length=10, choices=Chirgi.choices, null=True, blank=True)
    n_partenaire= models.IntegerField(null=True, blank=True)
    enceinte= models.CharField(max_length=10, choices=Enceinte.choices, null=True, blank=True)
    acupuncture= models.CharField(max_length=10, choices=Acupuncture.choices, null=True, blank=True)
    sut_plaies= models.CharField(max_length=10, choices=Sut_plaies.choices, null=True, blank=True)
    partenaire_s= models.CharField(max_length=10, choices=Partenaire_s.choices, null=True, blank=True)
    vaccin= models.CharField(max_length=100, choices=Vaccin, null=True, blank=True)
    auvaccin= models.CharField(max_length=50, null=True, blank=True)
    s_dentaire= models.CharField(max_length=10, choices=S_dentaire.choices, null=True, blank=True)
    fievre= models.CharField(max_length=10, choices=Fievre.choices, null=True, blank=True)
    plaies_ou= models.CharField(max_length=10, choices=Plaies_ou.choices, null=True, blank=True)
    medicament= models.CharField(max_length=10, choices=Medicament.choices, null=True, blank=True)
    aumedicament= models.CharField(max_length=50,  null=True, blank=True)
    medicament_p= models.CharField(max_length=100, choices= Medicament_p, null=True, blank=True)
    date_de_p = models.CharField(max_length=50, null=True, blank=True)
    motif_p_medicament=models.CharField(max_length=100, null=True, blank=True)
    enfant= models.CharField(max_length=10, choices=Enfant.choices, null=True, blank=True)
    enceint_actu= models.CharField(max_length=10, choices=Enceint_actu.choices, null=True, blank=True)
    en_regle= models.CharField(max_length=10, choices=En_regle.choices, null=True, blank=True)
    resultat_p= models.CharField(max_length=10, choices=Resultat_p.choices, null=True, blank=True)
    si_resultat= models.CharField(max_length=100, choices=Resultat.choices, null=True, blank=True)
    le_resultat= models.CharField(max_length=50, null=True, blank=True)
    poid= models.IntegerField( null=True, blank=True)
    taux_hd= models.IntegerField(null=True, blank=True)
    ta= models.IntegerField(null=True, blank=True)
    consentement= MultiSelectField(max_length=250, max_choices=17, choices=Consentement, default='Aucune')
    apte=models.CharField(max_length=100, choices=Apte, null=True, blank=True)
    code_ci=models.CharField(max_length=50, null=True, blank=True)
    identification=models.CharField(max_length=30, null=True, blank=True)
    date_created= models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dondesang'
    
    def __str__(sef):
        return str(sef.numero)
    
        if self.date_de_p is None:
            self.date_de_p = None
        super().save(*args, **kwargs)
    

class Predon(models.Model):
    class Preparation(models.TextChoices):
        AVEC = 'AvecCPS','Avec CPS'
        SANS = 'Sans CPS','Sans CPS'
    
    class Inapte(models.TextChoices):
        TEMPORAIRE= 'ITemporaire','ITemporaire'
        DEFINITIF= 'IDefinitif','IDefinitif'    
        
    entretien=models.ManyToManyField(Entretien)
    apte=models.CharField(max_length=30, null=True, blank=True)
    q_preleve=models.IntegerField()
    preparation=models.CharField(max_length=30, choices= Preparation.choices, null=True, blank=True)
    inapte=models.CharField(max_length=30, choices= Inapte.choices, null=True, blank=True,)
    code_ci= models.CharField(max_length=30, null=True, blank=True)
    identification=models.CharField(max_length=30, null=True, blank=True)
    date_created= models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dondesang'
    
    def __str__(sef):
        return str(sef.apte)
    def save(self, *args, **kwargs):
        if self.apte == '':
            self.apte = 'INAPTE'  # Valeur par défaut si aucun champ d'aptitude n'est spécifié
        super().save(*args, **kwargs)
    
    
class Preleve(models.Model):
    Poche=(('Simple','Simple'),('Double','Double'),
           ('Triple','Triple'),('Quadruple','Quadruple'))
    Observation=(('RAS','RAS'),('Problème de veine','Problème de veine'),
                 ('Malaise','Malaise'))
    
    predon=models.ManyToManyField(Predon)
    heur_p= models.TimeField()
    dure_p = models.TimeField()
    quantite_p= models.IntegerField()
    poche= models.CharField(max_length=100, choices=Poche, null=True, blank=True)
    observation= models.CharField(max_length=100, choices=Observation, null=True, blank=True)
    autre=models.CharField(max_length=100, null=True, blank=True)
    identif_p= models.CharField(max_length=100,)
    date_created= models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dondesang'
    
    def __str__(sef):
        return str(sef.identif_p)