from django import forms
from .models import Enseignant, Cours, Etudiant

# ------------------------------------------------------------------
# Formulaire pour Enseignant
# ------------------------------------------------------------------
class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = '__all__'  # ou une liste explicite
        labels = {
            'numens': 'Numéro enseignant',
            'nom': 'Nom',
            'prenom': 'Prénom',
            'email': 'Email',
            'departement': 'Département',
            'grade': 'Grade',
            'specialite': 'Spécialité',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'ex: jean.dupont@univ.fr'}),
        }

    def clean_numens(self):
        """Exemple de validation personnalisée"""
        numens = self.cleaned_data['numens']
        if not numens.startswith('ENS'):
            raise forms.ValidationError("Le numéro enseignant doit commencer par 'ENS'")
        return numens


# ------------------------------------------------------------------
# Formulaire pour Etudiant
# ------------------------------------------------------------------
class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = '__all__'
        labels = {
            'num_carte': 'Numéro de carte',
            'nom': 'Nom',
            'prenom': 'Prénom',
            'email': 'Email',
            'tel': 'Téléphone',
            'filiere': 'Filière',
            'annee_entree': 'Année d\'entrée',
            'date_naissance': 'Date de naissance',
            'cours': 'Cours suivis',
        }
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'tel': forms.TextInput(attrs={'placeholder': 'ex: 0123456789'}),
            'cours': forms.SelectMultiple(attrs={'size': 10}),  # Affichage plus pratique
        }

    def clean_annee_entree(self):
        annee = self.cleaned_data['annee_entree']
        from datetime import date
        if annee > date.today().year:
            raise forms.ValidationError("L'année d'entrée ne peut pas être dans le futur")
        return annee


# ------------------------------------------------------------------
# Formulaire pour Cours (avec gestion des relations)
# ------------------------------------------------------------------
class CoursForm(forms.ModelForm):
    # Champ supplémentaire pour gérer la relation ManyToMany avec Etudiant
    etudiants = forms.ModelMultipleChoiceField(
        queryset=Etudiant.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # ou forms.SelectMultiple
        required=False,
        label="Étudiants inscrits"
    )

    class Meta:
        model = Cours
        fields = '__all__'  # inclut la clé étrangère 'enseignant'
        labels = {
            'code_cours': 'Code du cours',
            'intitule': 'Intitulé',
            'description': 'Description',
            'credit': 'Crédits',
            'semestre': 'Semestre',
            'niveau': 'Niveau',
            'departement': 'Département',
            'prerequis': 'Prérequis',
            'enseignant': 'Enseignant responsable',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'prerequis': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser l'affichage du champ enseignant : nom complet
        self.fields['enseignant'].queryset = Enseignant.objects.all()
        self.fields['enseignant'].label_from_instance = lambda obj: f"{obj.nom} {obj.prenom} ({obj.numens})"

        # Si on modifie un cours existant, pré-remplir le champ 'etudiants'
        if self.instance.pk:
            self.fields['etudiants'].initial = self.instance.etudiants.all()

    def save(self, commit=True):
        # Sauvegarde du cours (ForeignKey gérée automatiquement)
        cours = super().save(commit=False)
        if commit:
            cours.save()
        # Gestion de la relation ManyToMany après sauvegarde
        if cours.pk:
            cours.etudiants.set(self.cleaned_data['etudiants'])
        return cours

    def clean_code_cours(self):
        code = self.cleaned_data['code_cours']
        if len(code) < 4:
            raise forms.ValidationError("Le code doit comporter au moins 4 caractères")
        return code.upper()