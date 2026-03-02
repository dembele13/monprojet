from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Enseignant, Cours, Etudiant
from .forms import EnseignantForm, CoursForm, EtudiantForm
from django.conf import settings
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import logging
from django.http import JsonResponse
from django.shortcuts import render 


# ------------------------------------------------------------------
# Enseignant
# ------------------------------------------------------------------
class EnseignantListView(ListView):
    model = Enseignant
    template_name = 'university/enseignant_list.html'
    context_object_name = 'enseignants'

class EnseignantCreateView(CreateView):
    model = Enseignant
    form_class = EnseignantForm
    template_name = 'university/enseignants_form.html'
    success_url = reverse_lazy('university:enseignant_list')

class EnseignantUpdateView(UpdateView):
    model = Enseignant
    form_class = EnseignantForm
    template_name = 'university/enseignants_form.html'
    success_url = reverse_lazy('university:enseignant_list')

class EnseignantDeleteView(DeleteView):
    model = Enseignant
    template_name = 'university/enseignant_confirm_delete.html'
    success_url = reverse_lazy('university:enseignant_list')

# ------------------------------------------------------------------
# Cours
# ------------------------------------------------------------------
class CoursListView(ListView):
    model = Cours
    template_name = 'university/cour_list.html'
    context_object_name = 'cours'

class CoursCreateView(CreateView):
    model = Cours
    form_class = CoursForm
    template_name = 'university/cours_form.html'
    success_url = reverse_lazy('university:cour_list')

class CoursUpdateView(UpdateView):
    model = Cours
    form_class = CoursForm
    template_name = 'university/cours_form.html'
    success_url = reverse_lazy('university:cour_list')

class CoursDeleteView(DeleteView):
    model = Cours
    template_name = 'university/cours_confirm_delete.html'
    success_url = reverse_lazy('university:cour_list')

# ------------------------------------------------------------------
# Etudiant
# ------------------------------------------------------------------
class EtudiantListView(ListView):
    model = Etudiant
    template_name = 'university/etudiant_list.html'
    context_object_name = 'etudiants'

class EtudiantCreateView(CreateView):
    model = Etudiant
    form_class = EtudiantForm
    template_name = 'university/etudiants_form.html'
    success_url = reverse_lazy('university:etudiant_list')

class EtudiantUpdateView(UpdateView):
    model = Etudiant
    form_class = EtudiantForm
    template_name = 'university/etudiants_form.html'
    success_url = reverse_lazy('university:etudiant_list')

class EtudiantDeleteView(DeleteView):
    model = Etudiant
    template_name = 'university/etudiant_confirm_delete.html'
    success_url = reverse_lazy('university:etudiant_list')

# dans views.py


def dashboard_data(request):
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]
    total_cours = db['cours'].count_documents({})
    total_enseignants = db['enseignants'].count_documents({})
    total_etudiants = db['etudiants'].count_documents({})
    return JsonResponse({
        'total_cours': total_cours,
        'total_enseignants': total_enseignants,
        'total_etudiants': total_etudiants,
    })
   # views.py


def dashboard_page(request):
    return render(request, 'university/dashboard.html')