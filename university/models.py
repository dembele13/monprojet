from django.db import models

class Enseignant(models.Model):
    idens = models.AutoField(primary_key=True)
    numens = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    departement = models.CharField(max_length=50)
    grade = models.CharField(max_length=30)
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Cours(models.Model):
    idcours = models.AutoField(primary_key=True)
    code_cours = models.CharField(max_length=20, unique=True)
    intitule = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credit = models.PositiveSmallIntegerField()
    semestre = models.CharField(max_length=20)
    niveau = models.CharField(max_length=30)
    departement = models.CharField(max_length=50)
    prerequis = models.TextField(blank=True)
    enseignant = models.ForeignKey(
        Enseignant,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cours'
    )

    def __str__(self):
        return f"{self.code_cours} - {self.intitule}"

class Etudiant(models.Model):
    idetu = models.AutoField(primary_key=True)
    num_carte = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=15, blank=True)
    filiere = models.CharField(max_length=50)
    annee_entree = models.PositiveSmallIntegerField()
    date_naissance = models.DateField()
    cours = models.ManyToManyField(Cours, related_name='etudiants')

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.num_carte})"

# Create your models here.
