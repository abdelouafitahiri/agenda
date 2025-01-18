from django.conf import settings
from django.urls import path
from . import views, users

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),

    path('users/', users.user_list, name='user-list'),
    
    path('societe/', views.societe_list, name='societe_list'),

    path('formesjuridiques/', views.formejuridique_list, name='formejuridique_list'),
    path('formesjuridiques/add/', views.formejuridique_create, name='formejuridique_create'),
    path('formesjuridiques/<int:pk>/edit/', views.formejuridique_edit, name='formejuridique_edit'),
    path('formesjuridiques/<int:pk>/archive/', views.formejuridique_archive, name='formejuridique_archive'),
    path('formesjuridiques/<int:pk>/delete/', views.formejuridique_delete, name='formejuridique_delete'),


    path('typeregs/', views.typereg_list, name='typereg_list'),
    path('typeregs/add/', views.typereg_create, name='typereg_create'),
    path('typeregs/<int:pk>/edit/', views.typereg_edit, name='typereg_edit'),
    path('typeregs/<int:pk>/archive/', views.typereg_archive, name='typereg_archive'),
    path('typeregs/<int:pk>/delete/', views.typereg_delete, name='typereg_delete'),

    path('regimes/', views.regime_list, name='regime_list'),
    path('regimes/add/', views.regime_create, name='regime_create'),
    path('regimes/<int:pk>/edit/', views.regime_edit, name='regime_edit'),
    path('regimes/<int:pk>/archive/', views.regime_archive, name='regime_archive'),
    path('regimes/<int:pk>/delete/', views.regime_delete, name='regime_delete'),

    path('qualites/', views.qualite_list, name='qualite_list'),
    path('qualites/add/', views.qualite_create, name='qualite_create'),
    path('qualites/<int:pk>/edit/', views.qualite_edit, name='qualite_edit'),
    path('qualites/<int:pk>/archive/', views.qualite_archive, name='qualite_archive'),
    path('qualites/<int:pk>/delete/', views.qualite_delete, name='qualite_delete'),

    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:pk>/archive/', views.service_archive, name='service_archive'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),

    path('exercices/', views.exercice_list, name='exercice_list'),
    path('exercices/add/', views.exercice_create, name='exercice_create'),
    path('exercices/<int:pk>/edit/', views.exercice_edit, name='exercice_edit'),
    path('exercices/<int:pk>/archive/', views.exercice_archive, name='exercice_archive'),
    path('exercices/<int:pk>/delete/', views.exercice_delete, name='exercice_delete'),

    path('comptables/', views.comptable_list, name='comptable_list'),
    path('comptables/add/', views.comptable_create, name='comptable_create'),
    path('comptables/<int:pk>/archive/', views.comptable_archive, name='comptable_archive'),
    path('comptables/<int:pk>/edit/', views.comptable_edit, name='comptable_edit'),
    path('comptables/<int:pk>/delete/', views.comptable_delete, name='comptable_delete'),


    path('folder_client/', views.folder_client, name='folder_client'),
    path('customer-files/', views.customer_file_list, name='customer_file_list'),
    path('customer-file/edit/<int:pk>/', views.edit_customer_file, name='edit_customer_file'),

    path('customer-files/<int:pk>/archive/', views.folder_client_archive, name='customer_file_list_archive'),

#    path('customer-files/<int:pk>/edit/', views.customer_file_edit, name='customer_file_edit'),

    path('gestion_mois/', views.gestion_mois, name='gestion_mois'),

    path("preparation-mois/", views.preparation_mois, name="preparation_mois"), 
    path('partial-payment/', views.partial_payment, name='partial_payment'),
    path('delete-partial-payment/<int:partial_id>/', views.delete_partial_payment, name='delete_partial_payment'),
    path('edit-partial-payment/<int:partial_id>/', views.edit_partial_payment, name='edit_partial_payment'),


    path("contracts/", views.liste_contrats, name="liste_contrats"),
    path("personne-physique/", views.ajouter_contrat, name="ajouter_contrat"),

    #path("renouveler/<int:id_contrat>/", views.renouveler_contrat, name="renouveler_contrat"),

]