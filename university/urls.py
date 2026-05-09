from django.urls import path
from . import views

app_name = 'university'

urlpatterns = [
    # Enseignant
    path('enseignants/', views.EnseignantListView.as_view(), name='enseignant_list'),
    path('enseignants/ajouter/', views.EnseignantCreateView.as_view(), name='enseignant_create'),
    path('enseignants/<int:pk>/modifier/', views.EnseignantUpdateView.as_view(), name='enseignant_update'),
    path('enseignants/<int:pk>/supprimer/', views.EnseignantDeleteView.as_view(), name='enseignant_delete'),

    # Cours
    path('cours/', views.CoursListView.as_view(), name='cour_list'),
    path('cours/ajouter/', views.CoursCreateView.as_view(), name='cours_create'),
    path('cours/<int:pk>/modifier/', views.CoursUpdateView.as_view(), name='cours_update'),
    path('cours/<int:pk>/supprimer/', views.CoursDeleteView.as_view(), name='cours_delete'),

    # Etudiant
    path('etudiants/', views.EtudiantListView.as_view(), name='etudiant_list'),
    path('etudiants/ajouter/', views.EtudiantCreateView.as_view(), name='etudiant_create'),
    path('etudiants/<int:pk>/modifier/', views.EtudiantUpdateView.as_view(), name='etudiant_update'),
    path('etudiants/<int:pk>/supprimer/', views.EtudiantDeleteView.as_view(), name='etudiant_delete'),
    
    path('dashboard/', views.dashboard_page, name='dashboard'),  
    path('api/dashboard-data/', views.dashboard_data, name='dashboard-data'),
]