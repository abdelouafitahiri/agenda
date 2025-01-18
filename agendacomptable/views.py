from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from itertools import groupby
from django.utils.timezone import make_aware
from datetime import date, timedelta
from .models import *
import calendar


@login_required
def dashboard(request):        
    # Calcul des statistiques clés
    pass

    context = {
        'total_locations': '',
        'total_items': '',
        'total_media': '',
        'locations': '',
        'months': '',
        'project_data': '',
        'item_data': '',
        'messages': '',
    }

    return render(request, 'accounting/dashboard.html', context)


def societe_list(request):
    """
    Affiche et met à jour les paramètres de la société.
    Si une instance de Société existe déjà, elle est mise à jour avec les nouvelles informations saisies.
    Sinon, une nouvelle instance de Société est créée.
    """

    # Vérifier s'il existe déjà une instance de Société
    societe = Societe.objects.first()

    if request.method == 'POST':
        # Message de succès ou d'information selon qu'un nouvel enregistrement est créé ou qu'un existant est mis à jour
        if not societe:
            # Créer une nouvelle instance de Société si aucune n'existe
            societe = Societe(user_create=request.user)
            messages.success(request, "Nouvelle société créée avec succès.")

        # Mettre à jour les champs de la Société avec les données du formulaire
        societe.libelle = request.POST.get('libelle')
        societe.date_creation = request.POST.get('date_creation')
        societe.activite = request.POST.get('activite')
        societe.activite_ar = request.POST.get('activite_ar')
        societe.adresse = request.POST.get('adresse')
        societe.adresse_ar = request.POST.get('adresse_ar')
        societe.ville = request.POST.get('ville')
        societe.ville_ar = request.POST.get('ville_ar')
        societe.mail = request.POST.get('mail')
        societe.gerant = request.POST.get('gerant')
        societe.gerant_ar = request.POST.get('gerant_ar')
        societe.rib = request.POST.get('rib')
        societe.if_field = request.POST.get('if_field')
        societe.ice = request.POST.get('ice')
        societe.rc = request.POST.get('rc')
        societe.cnss = request.POST.get('cnss')
        societe.user_edit = request.user  # Enregistrer l'utilisateur effectuant la modification

        # Si un nouveau logo est téléversé, le remplacer
        if request.FILES.get('logo'):
            societe.logo = request.FILES['logo']

        # Enregistrer les modifications dans la base de données
        societe.save()
        messages.success(request, "Les paramètres de la société ont été mis à jour avec succès.")
        return redirect('societe_list')  # Redirection vers la même page après sauvegarde

    # Rendre le template avec l'instance de Société (existant ou nouvellement créé)
    return render(request, 'accounting/societe_list.html', {'societe': societe})

@login_required
def formejuridique_list(request):
    """Affiche toutes les formes juridiques avec possibilité de filtrage par état d'archivage et recherche."""
    filter_status = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')

    if filter_status == 'archived':
        formesjuridiques = FormeJuridique.objects.filter(is_archived=True)
    elif filter_status == 'active':
        formesjuridiques = FormeJuridique.objects.filter(is_archived=False)
    else:
        formesjuridiques = FormeJuridique.objects.all()

    # Apply search filter
    if search_query:
        formesjuridiques = formesjuridiques.filter(
            Q(libelle__icontains=search_query) |
            Q(alias__icontains=search_query)
        )

    # Order by creation date in descending order
    formesjuridiques = formesjuridiques.order_by('-date_create')

    return render(request, 'accounting/formejuridique_list.html', {
        'formesjuridiques': formesjuridiques,
        'filter_status': filter_status,
        'search_query': search_query,
    })

@login_required
def formejuridique_create(request):
    """Ajoute une nouvelle forme juridique."""
    if request.method == 'POST':
        formejuridique = FormeJuridique(
            libelle=request.POST.get('libelle'),
            alias=request.POST.get('alias'),
            user_create=request.user
        )
        formejuridique.save()
        messages.success(request, "La forme juridique a été ajoutée avec succès.")
        return redirect('formejuridique_list')
    else:
        messages.error(request, "Erreur lors de l'ajout de la forme juridique.")
        return redirect('formejuridique_list')

@login_required
def formejuridique_edit(request, pk):
    """Modifie une forme juridique existante."""
    formejuridique = get_object_or_404(FormeJuridique, pk=pk)
    if request.method == 'POST':
        formejuridique.libelle = request.POST.get('libelle')
        formejuridique.alias = request.POST.get('alias')
        formejuridique.user_edit = request.user
        formejuridique.save()
        messages.success(request, "La forme juridique a été mise à jour avec succès.")
        return redirect('formejuridique_list')
    else:
        messages.error(request, "Erreur lors de la mise à jour de la forme juridique.")
        return redirect('formejuridique_list')

@login_required
def formejuridique_archive(request, pk):
    """Archive ou réactive une forme juridique."""
    formejuridique = get_object_or_404(FormeJuridique, pk=pk)
    formejuridique.is_archived = not formejuridique.is_archived
    formejuridique.save()
    if formejuridique.is_archived:
        messages.success(request, "La forme juridique a été archivée avec succès.")
    else:
        messages.success(request, "La forme juridique a été réactivée avec succès.")
    return redirect('formejuridique_list')

@login_required
def formejuridique_delete(request, pk):
    """Supprime une forme juridique."""
    formejuridique = get_object_or_404(FormeJuridique, pk=pk)
    if request.method == 'POST':
        formejuridique.delete()
        messages.success(request, "La forme juridique a été supprimée avec succès.")
    else:
        messages.error(request, "Erreur lors de la suppression de la forme juridique.")
    return redirect('formejuridique_list')


@login_required
def exercice_list(request):
    """Affiche tous les exercices avec possibilité de filtrage par état d'archivage et recherche."""
    filter_status = request.GET.get('filter', 'all')  # Obtient le filtre actuel (tous, actifs ou archivés)
    search_query = request.GET.get('search', '')  # Obtient la requête de recherche

    # Filtre les exercices en fonction de l'état d'archivage
    if filter_status == 'archived':
        exercices = Exercice.objects.filter(is_archived=True)
    elif filter_status == 'active':
        exercices = Exercice.objects.filter(is_archived=False)
    else:
        exercices = Exercice.objects.all()
    
    # Applique le filtre de recherche si une requête est fournie
    if search_query:
        exercices = exercices.filter(
            Q(libelle__icontains=search_query)
        )

    # Trier par date de création décroissante pour afficher les plus récents en premier
    exercices = exercices.order_by('-date_create')

    return render(request, 'accounting/exercice_list.html', {
        'exercices': exercices,
        'filter_status': filter_status,
        'search_query': search_query,
    })

@login_required
def exercice_create(request):
    """Ajoute un nouvel exercice."""
    if request.method == 'POST':
        try:
            exercice = Exercice(
                libelle=request.POST.get('libelle'),
                user_create=request.user
            )
            exercice.save()
            messages.success(request, "L'exercice a été ajouté avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout de l'exercice : {e}")
        return redirect('exercice_list')
    else:
        messages.error(request, "Méthode de requête invalide pour l'ajout de l'exercice.")
        return redirect('exercice_list')

@login_required
def exercice_edit(request, pk):
    """Modifie un exercice existant."""
    exercice = get_object_or_404(Exercice, pk=pk)
    if request.method == 'POST':
        try:
            exercice.libelle = request.POST.get('libelle')
            exercice.user_edit = request.user
            exercice.save()
            messages.success(request, "L'exercice a été mis à jour avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de la mise à jour de l'exercice : {e}")
        return redirect('exercice_list')
    else:
        messages.error(request, "Méthode de requête invalide pour la mise à jour de l'exercice.")
        return redirect('exercice_list')

@login_required
def exercice_archive(request, pk):
    """Archive ou réactive un exercice."""
    exercice = get_object_or_404(Exercice, pk=pk)
    exercice.is_archived = not exercice.is_archived  # Toggle archived state
    exercice.save()
    if exercice.is_archived:
        messages.success(request, "L'exercice a été archivé avec succès.")
    else:
        messages.success(request, "L'exercice a été réactivé avec succès.")
    return redirect('exercice_list')

@login_required
def exercice_delete(request, pk):
    """Supprime un exercice."""
    exercice = get_object_or_404(Exercice, pk=pk)
    if request.method == 'POST':
        exercice.delete()
        messages.success(request, "L'exercice a été supprimé avec succès.")
    else:
        messages.error(request, "Erreur lors de la suppression de l'exercice.")
    return redirect('exercice_list')

@login_required
def typereg_list(request):
    """Affiche tous les types de régimes avec possibilité de filtrage par état et recherche."""
    filter_status = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')

    if filter_status == 'archived':
        typeregs = TypeReg.objects.filter(is_archived=True)
    elif filter_status == 'active':
        typeregs = TypeReg.objects.filter(is_archived=False)
    else:
        typeregs = TypeReg.objects.all()

    # Apply search filter
    if search_query:
        typeregs = typeregs.filter(Q(libelle__icontains=search_query))

    # Order by creation date in descending order
    typeregs = typeregs.order_by('-date_create')

    return render(request, 'accounting/typereg_list.html', {
        'typeregs': typeregs,
        'filter_status': filter_status,
        'search_query': search_query,
    })

@login_required
def typereg_create(request):
    """Ajoute un nouveau type de régime."""
    if request.method == 'POST':
        typereg = TypeReg(
            libelle=request.POST.get('libelle'),
            user_create=request.user
        )
        typereg.save()
        messages.success(request, "Le type de régime a été ajouté avec succès.")
        return redirect('typereg_list')
    else:
        messages.error(request, "Erreur lors de l'ajout du type de régime.")
        return redirect('typereg_list')

@login_required
def typereg_edit(request, pk):
    """Modifie un type de régime existant."""
    typereg = get_object_or_404(TypeReg, pk=pk)
    if request.method == 'POST':
        typereg.libelle = request.POST.get('libelle')
        typereg.user_edit = request.user
        typereg.save()
        messages.success(request, "Le type de régime a été mis à jour avec succès.")
        return redirect('typereg_list')
    else:
        messages.error(request, "Erreur lors de la mise à jour du type de régime.")
        return redirect('typereg_list')

@login_required
def typereg_archive(request, pk):
    """Archive ou réactive un type de régime."""
    typereg = get_object_or_404(TypeReg, pk=pk)
    typereg.is_archived = not typereg.is_archived  # Toggle archiving
    typereg.save()
    if typereg.is_archived:
        messages.success(request, "Le type de régime a été archivé avec succès.")
    else:
        messages.success(request, "Le type de régime a été réactivé avec succès.")
    return redirect('typereg_list')

@login_required
def typereg_delete(request, pk):
    """Supprime un type de régime."""
    typereg = get_object_or_404(TypeReg, pk=pk)
    if request.method == 'POST':
        typereg.delete()
        messages.success(request, "Le type de régime a été supprimé avec succès.")
    else:
        messages.error(request, "Erreur lors de la suppression du type de régime.")
    return redirect('typereg_list')


@login_required
def regime_list(request):
    """Affiche tous les régimes avec possibilité de filtrage par état et recherche."""
    filter_status = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')

    # Filtrer les régimes par état (archivé ou non) et trier par date de création décroissante
    if filter_status == 'archived':
        regimes = Regime.objects.filter(is_archived=True)
    elif filter_status == 'active':
        regimes = Regime.objects.filter(is_archived=False)
    else:
        regimes = Regime.objects.all()

    # Appliquer la recherche
    if search_query:
        regimes = regimes.filter(Q(libelle__icontains=search_query))

    # Trier par date de création décroissante pour afficher les plus récents en premier
    regimes = regimes.order_by('-date_create')

    return render(request, 'accounting/regime_list.html', {
        'regimes': regimes,
        'filter_status': filter_status,
        'search_query': search_query,
    })

@login_required
def regime_create(request):
    """Ajoute un nouveau régime."""
    if request.method == 'POST':
        regime = Regime(
            libelle=request.POST.get('libelle'),
            user_create=request.user
        )
        regime.save()
        messages.success(request, "Le régime a été ajouté avec succès.")
        return redirect('regime_list')
    else:
        messages.error(request, "Erreur lors de l'ajout du régime.")
        return redirect('regime_list')

@login_required
def regime_edit(request, pk):
    """Modifie un régime existant."""
    regime = get_object_or_404(Regime, pk=pk)
    if request.method == 'POST':
        regime.libelle = request.POST.get('libelle')
        regime.user_edit = request.user
        regime.save()
        messages.success(request, "Le régime a été mis à jour avec succès.")
        return redirect('regime_list')
    else:
        messages.error(request, "Erreur lors de la mise à jour du régime.")
        return redirect('regime_list')

@login_required
def regime_archive(request, pk):
    """Archive ou réactive un régime."""
    regime = get_object_or_404(Regime, pk=pk)
    regime.is_archived = not regime.is_archived  # Toggle l'état archivé
    regime.save()
    if regime.is_archived:
        messages.success(request, "Le régime a été archivé avec succès.")
    else:
        messages.success(request, "Le régime a été réactivé avec succès.")
    return redirect('regime_list')

@login_required
def regime_delete(request, pk):
    """Supprime un régime."""
    regime = get_object_or_404(Regime, pk=pk)
    if request.method == 'POST':
        regime.delete()
        messages.success(request, "Le régime a été supprimé avec succès.")
    else:
        messages.error(request, "Erreur lors de la suppression du régime.")
    return redirect('regime_list')


@login_required
def qualite_list(request):
    """Affiche toutes les qualités avec possibilité de filtrage par état d'archivage et recherche."""
    filter_status = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')

    # Filtrage selon l'état d'archivage et tri par date de création décroissante
    if filter_status == 'archived':
        qualites = Qualite.objects.filter(is_archived=True)
    elif filter_status == 'active':
        qualites = Qualite.objects.filter(is_archived=False)
    else:
        qualites = Qualite.objects.all()

    # Recherche
    if search_query:
        qualites = qualites.filter(Q(libelle__icontains=search_query))

    # Trier par date de création décroissante pour afficher les plus récents en premier
    qualites = qualites.order_by('-date_create')

    return render(request, 'accounting/qualite_list.html', {
        'qualites': qualites,
        'filter_status': filter_status,
        'search_query': search_query,
    })

@login_required
def qualite_create(request):
    """Ajoute une nouvelle qualité."""
    if request.method == 'POST':
        qualite = Qualite(
            libelle=request.POST.get('libelle'),
            user_create=request.user
        )
        qualite.save()
        messages.success(request, "La qualité a été ajoutée avec succès.")
        return redirect('qualite_list')
    else:
        messages.error(request, "Erreur lors de l'ajout de la qualité.")
        return redirect('qualite_list')

@login_required
def qualite_edit(request, pk):
    """Modifie une qualité existante."""
    qualite = get_object_or_404(Qualite, pk=pk)
    if request.method == 'POST':
        qualite.libelle = request.POST.get('libelle')
        qualite.user_edit = request.user
        qualite.save()
        messages.success(request, "La qualité a été mise à jour avec succès.")
        return redirect('qualite_list')
    else:
        messages.error(request, "Erreur lors de la mise à jour de la qualité.")
        return redirect('qualite_list')

@login_required
def qualite_archive(request, pk):
    """Archive ou réactive une qualité."""
    qualite = get_object_or_404(Qualite, pk=pk)
    qualite.is_archived = not qualite.is_archived  # Bascule l'état d'archivage
    qualite.save()
    if qualite.is_archived:
        messages.success(request, "La qualité a été archivée avec succès.")
    else:
        messages.success(request, "La qualité a été réactivée avec succès.")
    return redirect('qualite_list')

@login_required
def qualite_delete(request, pk):
    """Supprime une qualité."""
    qualite = get_object_or_404(Qualite, pk=pk)
    if request.method == 'POST':
        qualite.delete()
        messages.success(request, "La qualité a été supprimée avec succès.")
    else:
        messages.error(request, "Erreur lors de la suppression de la qualité.")
    return redirect('qualite_list')


@login_required
def service_list(request):
    """Affiche tous les services avec possibilité de filtrage par état et recherche."""
    filter_status = request.GET.get('filter', 'all')  # Obtient le statut de filtre (tous, actifs, archivés)
    search_query = request.GET.get('search', '')  # Obtient la requête de recherche

    critere_paiement_choices = CriteresPaiement.objects.all()

    # Filtrage des services selon le statut
    if filter_status == 'archived':
        services = Service.objects.filter(etat='F')
    elif filter_status == 'active':
        services = Service.objects.filter(etat='T')
    else:
        services = Service.objects.all()

    # Filtrage selon la requête de recherche
    if search_query:
        services = services.filter(libelle__icontains=search_query)

    # Trier par date de création décroissante pour afficher les plus récents en premier
    services = services.order_by('-date_create')

    return render(request, 'accounting/service_list.html', {
        'services': services,
        'filter_status': filter_status,
        'search_query': search_query,
        'critere_paiement_choices': critere_paiement_choices
    })


@login_required
def service_create(request):
    """Ajoute un nouveau service."""
    if request.method == 'POST':
        try:
            # Get the selected Critere de Paiement
            critere_paiement_id = request.POST.get('critere_paiement')
            critere_paiement = CriteresPaiement.objects.get(id=critere_paiement_id)

            # Create a new Service instance with Critere de Paiement
            service = Service(
                libelle=request.POST.get('libelle'),
                prix=request.POST.get('prix'),
                etat='T',
                criteres_paiement=critere_paiement,
                user_create=request.user  # Set the user creating the entry
            )
            service.save()
            messages.success(request, "Le service a été ajouté avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout du service : {e}")
        return redirect('service_list')


@login_required
def service_edit(request, pk):
    """Modifie un service existant."""
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        try:
            # Update fields from the form data
            service.libelle = request.POST.get('libelle')
            service.prix = request.POST.get('prix')
            service.user_edit = request.user  # Register the user modifying the service
            
            # Update Critere de Paiement
            critere_paiement_id = request.POST.get('critere_paiement')
            if critere_paiement_id:
                service.criteres_paiement = CriteresPaiement.objects.get(id=critere_paiement_id)
            
            service.save()
            messages.success(request, "Le service a été mis à jour avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de la mise à jour du service : {e}")
        return redirect('service_list')



@login_required
def service_archive(request, pk):
    """Archive ou réactive un service."""
    service = get_object_or_404(Service, pk=pk)
    try:
        service.etat = 'F' if service.etat == 'T' else 'T'  # Change l'état (archive ou réactive)
        service.save()
        if service.etat == 'F':
            messages.success(request, "Le service a été archivé avec succès.")
        else:
            messages.success(request, "Le service a été réactivé avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors de l'archivage/réactivation du service : {e}")
    return redirect('service_list')

@login_required
def service_delete(request, pk):
    """Supprime un service."""
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        try:
            service.delete()
            messages.success(request, "Le service a été supprimé avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression du service : {e}")
    else:
        messages.error(request, "Méthode de requête invalide pour la suppression du service.")
    return redirect('service_list')


@login_required
def comptable_list(request):
    """Affiche tous les enregistrements avec possibilité de filtrage par état d'archivage et recherche."""
    filter_status = request.GET.get('filter', 'all')  # Obtient le filtre actuel (tous, actifs ou archivés)
    search_query = request.GET.get('search', '')  # Obtient la requête de recherche

    # Filtre les enregistrements en fonction de l'état d'archivage et de la recherche
    if filter_status == 'archived':
        comptables = Comptable.objects.filter(is_archived=True)
    elif filter_status == 'active':
        comptables = Comptable.objects.filter(is_archived=False)
    else:
        comptables = Comptable.objects.all()
    
    # Applique le filtre de recherche si une requête est fournie
    if search_query:
        comptables = comptables.filter(
            Q(lib_08__icontains=search_query) |
            Q(contact_08__icontains=search_query)
        )

    # Trier par date de création décroissante pour afficher les plus récents en premier
    comptables = comptables.order_by('-date_create_08')

    return render(request, 'accounting/comptable_list.html', {
        'comptables': comptables,
        'filter_status': filter_status,
        'search_query': search_query,
    })


@login_required
def comptable_create(request):
    """Ajoute un nouveau comptable."""
    if request.method == 'POST':
        # Crée un nouvel enregistrement avec les données fournies
        comptable = Comptable(
            lib_08=request.POST.get('lib_08'),
            adr_08=request.POST.get('adr_08'),
            mail_08=request.POST.get('mail_08'),
            tel_08=request.POST.get('tel_08'),
            contact_08=request.POST.get('contact_08')
        )
        comptable.save()  # Enregistre le nouvel enregistrement dans la base de données
        messages.success(request, "Le comptable a été ajouté avec succès.")
        return redirect('comptable_list')
    else:
        messages.error(request, "Erreur lors de l'ajout du comptable.")
        return redirect('comptable_list')

@login_required
def comptable_edit(request, pk):
    """Modifie un enregistrement existant."""
    comptable = get_object_or_404(Comptable, pk=pk)  # Récupère l'enregistrement ou affiche une erreur 404 s'il n'existe pas
    if request.method == 'POST':
        # Met à jour les champs en fonction des données du formulaire
        comptable.lib_08 = request.POST.get('lib_08')
        comptable.adr_08 = request.POST.get('adr_08')
        comptable.mail_08 = request.POST.get('mail_08')
        comptable.tel_08 = request.POST.get('tel_08')
        comptable.contact_08 = request.POST.get('contact_08')
        comptable.save()  # Sauvegarde les modifications
        messages.success(request, "L'enregistrement a été mis à jour avec succès.")
        return redirect('comptable_list')
    else:
        messages.error(request, "Erreur lors de la mise à jour du comptable.")
        return redirect('comptable_list')

@login_required
def comptable_archive(request, pk):
    """Archive ou réactive un enregistrement."""
    comptable = get_object_or_404(Comptable, pk=pk)  # Récupère l'enregistrement ou affiche une erreur 404 s'il n'existe pas
    comptable.is_archived = not comptable.is_archived  # Inverse l'état d'archivage
    comptable.save()  # Sauvegarde l'état modifié
    if comptable.is_archived:
        messages.success(request, "L'enregistrement a été archivé avec succès.")
    else:
        messages.success(request, "L'enregistrement a été réactivé avec succès.")
    return redirect('comptable_list')

@login_required
def comptable_delete(request, pk):
    """Supprime un enregistrement."""
    comptable = get_object_or_404(Comptable, pk=pk)  # Récupère l'enregistrement ou affiche une erreur 404 s'il n'existe pas
    if request.method == 'POST':
        comptable.delete()  # Supprime l'enregistrement
        messages.success(request, "L'enregistrement a été supprimé avec succès.")
    else:
        messages.error(request, "Erreur lors de la suppression de l'enregistrement.")
    return redirect('comptable_list')

def folder_client(request):
    if request.method == 'POST':
        try:
            # Vérification de l'authentification
            if not request.user.is_authenticated:
                messages.error(request, "Vous devez être connecté pour effectuer cette action.")
                return redirect('login')

            # Gestion des dates avec vérification du format
            def parse_date(date_str):
                if date_str:
                    try:
                        return datetime.strptime(date_str, "%Y-%m-%d").date()
                    except ValueError:
                        raise ValueError(f"La date '{date_str}' doit être au format YYYY-MM-DD.")
                return None

            
            # Enregistrement des données générales
            raison_sociale = request.POST.get('raison_sociale')
            activite = request.POST.get('activite')
            email = request.POST.get('email')
            ville = request.POST.get('ville')
            adresse = request.POST.get('adresse')
            forme_juridique = request.POST.get('forme_juridique')
            identifiant_fiscal = request.POST.get('identifiant_fiscal')
            registre_commerce = request.POST.get('registre_commerce')
            cnss = request.POST.get('cnss')
            ice = request.POST.get('ice')
            date_creation = request.POST.get('date_creation')
            domiciliation = request.POST.get('domiciliation') == 'on'
            tenue_comptabilite = request.POST.get('tenue_comptabilite') == 'on'
            cabinet_comptable = request.POST.get('cabinet_comptable')
            date_reception_dossier = request.POST.get('date_reception_dossier')

            # Création du dossier client
            customer_file = CustomerFile.objects.create(
                raison_sociale=raison_sociale,
                activite=activite,
                email=email,
                ville=ville,
                adresse=adresse,
                forme_juridique_id=forme_juridique,
                identifiant_fiscal=identifiant_fiscal,
                registre_commerce=registre_commerce,
                cnss=cnss,
                ice=ice,
                date_creation=parse_date(date_creation),
                domiciliation=domiciliation,
                tenue_comptabilite=tenue_comptabilite,
                cabinet_comptable_id=cabinet_comptable,
                date_reception_dossier=parse_date(date_reception_dossier),
                date_create = models.DateTimeField(auto_now_add=True, editable=False),
                user_create=request.user
            )

            # Enregistrement des contacts associés
            noms_complets = request.POST.getlist('nom_complet[]')
            emails = request.POST.getlist('email[]')
            telephones = request.POST.getlist('telephone[]')
            
            # Enregistrement des contacts associés
            for nom, email_contact, telephone in zip(noms_complets, emails, telephones):
                if nom or email_contact or telephone:
                    try:
                        if not Contact.objects.filter(nom_complet=nom, email=email_contact, telephone=telephone).exists():
                            Contact.objects.create(
                                nom_complet=nom,
                                email=email_contact,
                                telephone=telephone,
                                customer_files=customer_file,
                                user_create=request.user
                            )
                        else:
                            print(f"Duplicate contact found: {nom}")
                    except Exception as e:
                        print(f"Error while saving contact {nom}: {e}")

            # Enregistrement des régimes fiscaux associés
            service_types = request.POST.getlist('service_type[]')
            service_options = request.POST.getlist('service_option[]')
            tva_periods = request.POST.getlist('tva_period[]')

            for service_type, service_option, tva_period in zip(service_types, service_options, tva_periods):
                if service_type:  # Vérifier qu'il y a un type de service
                    # If service type is 'TVA', we allow tva_period to be set
                    if service_type == 'TVA' and not tva_period:
                        # Raise an error if 'TVA' type is selected but tva_period is missing
                        raise ValidationError("Le champ 'Période (TVA)' est requis pour le type TVA.")
                    
                    # Create the FiscalRegime object
                    FiscalRegime.objects.create(
                        type=service_type,
                        option=service_option,
                        tva_period=tva_period if service_type == 'TVA' else None,  # Ensure tva_period is set only for TVA
                        customer_file=customer_file
                    )


            messages.success(request, "Le dossier client a été créé avec succès !")

            for nom, email, telephone in zip(noms_complets, emails, telephones):
                nom = nom.strip() if nom and isinstance(nom, str) else None
                email = email.strip() if email and isinstance(email, str) else None
                telephone = telephone.strip() if telephone and isinstance(telephone, str) else None
                contact = Contact.objects.create(
                    customer_file=customer_file,  # Ensure `customer_file` is defined and passed
                    nom_complet=nom,
                    email=email,
                    telephone=telephone,
                    user_create=request.user  # Set the user who is creating the contact
                )

            # Enregistrement des services si "Tenue Comptabilité" est activé
            if tenue_comptabilite:
                services_ids = request.POST.getlist('service_id[]')
                services_prix = request.POST.getlist('service_prix[]')
                services_date_debut = request.POST.getlist('service_date_debut[]')
                services_date_fin = request.POST.getlist('service_date_fin[]')

                for i in range(len(services_ids)):
                    try:
                        service = Service.objects.get(id=services_ids[i])
                        CustomerService.objects.create(
                            customer_file=customer_file,
                            service=service,
                            prix=services_prix[i],
                            date_debut=parse_date(services_date_debut[i]),
                            date_fin=parse_date(services_date_fin[i]),
                        )
                    except Service.DoesNotExist:
                        print(f"Service ID {services_ids[i]} introuvable. Ignoré.")

            # Enregistrement de la service "Domiciliation" si activé
            if domiciliation:
                domiciliation_service, _ = Service.objects.get_or_create(
                    libelle="Domiciliation",
                    defaults={"prix": 0.0}
                )
                domiciliation_prix = request.POST.get('domiciliation_prix', domiciliation_service.prix)
                domiciliation_date_debut = request.POST.get('domiciliation_date_debut', date_creation)
                domiciliation_date_fin = request.POST.get('domiciliation_date_fin') or None

                CustomerService.objects.create(
                    customer_file=customer_file,
                    service=domiciliation_service,
                    prix=domiciliation_prix,
                    date_debut=parse_date(domiciliation_date_debut),
                    date_fin=parse_date(domiciliation_date_fin),
                )

            # Enregistrement des documents électroniques
            files = request.FILES.getlist('document_file[]')
            for file in files:
                EDocument.objects.create(
                    customer_file=customer_file,
                    file=file,
                )
            if files:
                messages.success(request, f"{len(files)} document(s) électronique(s) ont été téléchargé(s) avec succès !")

            # Enregistrement des associés
            noms = request.POST.getlist('associe_nom[]')
            prenoms = request.POST.getlist('associe_prenom[]')
            datns = request.POST.getlist('associe_datn[]')
            cines = request.POST.getlist('associe_cine[]')
            adresses = request.POST.getlist('associe_adresse[]')
            parts = request.POST.getlist('associe_parts[]')
            montants = request.POST.getlist('associe_montant[]')
            
            for index in range(len(noms)):
                if noms[index] and prenoms[index]:
                    Associe.objects.create(
                        customer_file=customer_file,
                        nom=noms[index],
                        prenom=prenoms[index],
                        datn=parse_date(datns[index]) if index < len(datns) and datns[index] else None,
                        cine=cines[index] if index < len(cines) else "",
                        adresse=adresses[index] if index < len(adresses) else "",
                        parts=int(parts[index]) if index < len(parts) and parts[index] else 0,
                        montant=float(montants[index]) if index < len(montants) and montants[index] else 0.0,
                        user_create=request.user,
                    )
            messages.success(request, f"{len(noms)} associé(s) ont été enregistré(s) avec succès !")


            # Gestion des contrats
            type_contrat = request.POST.get('type_contrat')
            if type_contrat == 'personne_physique':
                loyer_mensuel_contrat_physique = request.POST.get('loyer_mensuel_contrat_physique')
                loyer_mensuel_plateforme_physique = request.POST.get('loyer_mensuel_plateforme_physique')
                date_debut_physique = parse_date(request.POST.get('date_debut_physique'))
                date_fin_physique = parse_date(request.POST.get('date_fin_physique'))
                date_naissance_physique = parse_date(request.POST.get('date_naissance_physique'))
                date_contrat_physique = parse_date(request.POST.get('date_contrat_physique'))

                ContratPersonnePhysique.objects.create(
                    customer_file=customer_file,
                    nom_prenom=request.POST.get('nom_prenom'),
                    loyer_mensuel_contrat=loyer_mensuel_contrat_physique,
                    loyer_mensuel_plateforme=loyer_mensuel_plateforme_physique,
                    date_debut=date_debut_physique,
                    date_fin=date_fin_physique,
                    date_naissance=date_naissance_physique,
                    adresse=request.POST.get('adresse_physique'),
                    date_contrat=date_contrat_physique,
                    user_create=request.user,
                    date_create = models.DateTimeField(auto_now_add=True, editable=False),
                )
                messages.success(request, "Le contrat pour une personne physique a été enregistré avec succès !")

            elif type_contrat == 'personne_morale':
                loyer_mensuel_contrat_morale = request.POST.get('loyer_mensuel_contrat_morale')
                loyer_mensuel_plateforme_morale = request.POST.get('loyer_mensuel_plateforme_morale')
                date_debut_morale = parse_date(request.POST.get('date_debut'))
                date_fin_morale = parse_date(request.POST.get('date_fin'))
                date_contrat_morale = parse_date(request.POST.get('date_contrat'))
                date_naissance_representant = parse_date(request.POST.get('date_naissance_representant'))
                nom_soc = request.POST.get('nom_soc')
                ContratPersonneMorale.objects.create(
                    customer_file=customer_file,
                    nom_soc = nom_soc,
                    registre_commerce=request.POST.get('registre_commerce'),
                    nom_representant=request.POST.get('nom_representant'),
                    cin_representant=request.POST.get('cin_representant'),
                    date_naissance_representant=date_naissance_representant,
                    loyer_mensuel_contrat=loyer_mensuel_contrat_morale,
                    loyer_mensuel_plateforme=loyer_mensuel_plateforme_morale,
                    date_debut=date_debut_morale,
                    date_fin=date_fin_morale,
                    date_contrat=date_contrat_morale,
                    user_create=request.user,
                    date_create = models.DateTimeField(auto_now_add=True, editable=False),
                )
                messages.success(request, "Le contrat pour une personne morale a été enregistré avec succès !")

        except Exception as e:
            messages.error(request, f"Une erreur s'est produite lors du traitement : {str(e)}")
            return redirect('folder_client')
        return redirect('customer_file_list')

    # Données pour afficher le formulaire
    services = Service.objects.filter(is_archived=False)
    regimes = Regime.objects.all()
    formes_juridiques = FormeJuridique.objects.all()
    comptables = Comptable.objects.all()
    qualites = Qualite.objects.all()

    return render(request, "accounting/folder_client.html", {
        "services": services,
        "regimes": regimes,
        "formes_juridiques": formes_juridiques,
        "comptables": comptables,
        "qualites": qualites,
    })

def customer_file_list(request):
    """Affiche tous les enregistrements avec possibilité de filtrage par état d'archivage et recherche."""
    filter_status = request.GET.get('filter', 'all')  # Obtient le filtre actuel (tous, actifs ou archivés)
    search_query = request.GET.get('search', '')  # Obtient la requête de recherche

    # Filtre les enregistrements en fonction de l'état d'archivage et de la recherche
    if filter_status == 'archived':
        customer_files = CustomerFile.objects.filter(is_archived=True)
    elif filter_status == 'active':
        customer_files = CustomerFile.objects.filter(is_archived=False)
    else:
        customer_files = CustomerFile.objects.all()
    
    # Applique le filtre de recherche si une requête est fournie
    if search_query:
        customer_files = customer_files.filter(
            Q(raison_sociale__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Trier par date de création décroissante pour afficher les plus récents en premier
    entreprises = customer_files.order_by('-date_create')

    return render(request, 'accounting/customer_file_list.html', {'entreprises': entreprises})

def edit_customer_file(request, pk):
    try:
        customer_file = CustomerFile.objects.prefetch_related('services__service', 'edocuments', 'associes').get(pk=pk)
    except CustomerFile.DoesNotExist:
        messages.error(request, "Le dossier client demandé n'existe pas.")
        return redirect('customer_file_list')
    
    if request.method == 'POST':
        try:
            # Mise à jour des données générales
            customer_file.raison_sociale = request.POST.get('raison_sociale')
            customer_file.activite = request.POST.get('activite')
            customer_file.email = request.POST.get('email')
            customer_file.ville = request.POST.get('ville')
            customer_file.adresse = request.POST.get('adresse')
            customer_file.personne_1 = request.POST.get('personne_1')
            customer_file.personne_2 = request.POST.get('personne_2')
            customer_file.telephone = request.POST.get('telephone')
            customer_file.regime_tva_id = request.POST.get('regime_tva')
            customer_file.forme_juridique_id = request.POST.get('forme_juridique')
            customer_file.identifiant_fiscal = request.POST.get('identifiant_fiscal')
            customer_file.registre_commerce = request.POST.get('registre_commerce')
            customer_file.cnss = request.POST.get('cnss')
            customer_file.ice = request.POST.get('ice')
            customer_file.date_creation = request.POST.get('date_creation')
            customer_file.domiciliation = request.POST.get('domiciliation') == 'on'
            customer_file.tenue_comptabilite = request.POST.get('tenue_comptabilite') == 'on'
            customer_file.cabinet_comptable_id = request.POST.get('cabinet_comptable')
            customer_file.date_reception_dossier = request.POST.get('date_reception_dossier')
            customer_file.save()

            messages.success(request, "Les données générales du dossier client ont été mises à jour avec succès.")

            # Mise à jour ou suppression du service "Domiciliation"
            if customer_file.tenue_comptabilite or customer_file.domiciliation:
                existing_service_ids = request.POST.getlist('service_id[]')
                CustomerService.objects.filter(customer_file=customer_file).exclude(service_id__in=existing_service_ids).delete()

                for index, service_id in enumerate(existing_service_ids):
                    if not service_id.isdigit():
                        continue  # Ignore invalid IDs

                    prix = request.POST.getlist('service_prix[]')[index]
                    date_debut = request.POST.getlist('service_date_debut[]')[index]
                    date_fin = request.POST.getlist('service_date_fin[]')[index]

                    CustomerService.objects.update_or_create(
                        customer_file=customer_file,
                        service_id=int(service_id),
                        defaults={
                            'prix': prix,
                            'date_debut': date_debut,
                            'date_fin': date_fin,
                        }
                    )
            messages.success(request, "Les services ont été mis à jour avec succès.")


            # Mise à jour des autres services
            if customer_file.tenue_comptabilite:
                existing_service_ids = set(request.POST.getlist('service_id[]'))
                CustomerService.objects.filter(customer_file=customer_file).exclude(service_id__in=existing_service_ids).delete()

                for index, service_id in enumerate(existing_service_ids):
                    prix = request.POST.getlist('service_prix[]')[index]
                    date_debut = request.POST.getlist('service_date_debut[]')[index]
                    date_fin = request.POST.getlist('service_date_fin[]')[index]

                    CustomerService.objects.update_or_create(
                        customer_file=customer_file,
                        service_id=service_id,
                        defaults={
                            'prix': prix,
                            'date_debut': date_debut,
                            'date_fin': date_fin,
                        }
                    )
                messages.success(request, "Les services ont été mis à jour avec succès.")

            # Mise à jour des documents électroniques
            removed_document_ids = request.POST.getlist('removed_document_ids[]')
            if removed_document_ids:
                EDocument.objects.filter(id__in=removed_document_ids).delete()
                messages.success(request, f"{len(removed_document_ids)} document(s) ont été supprimé(s).")

            new_files = request.FILES.getlist('document_file[]')
            for file in new_files:
                EDocument.objects.create(customer_file=customer_file, file=file)
            if new_files:
                messages.success(request, f"{len(new_files)} nouveau(x) document(s) électronique(s) ont été ajouté(s).")

            # Mise à jour des associés
            noms = request.POST.getlist('associe_nom[]')
            prenoms = request.POST.getlist('associe_prenom[]')
            datns = request.POST.getlist('associe_datn[]')
            cines = request.POST.getlist('associe_cine[]')
            adresses = request.POST.getlist('associe_adresse[]')
            parts = request.POST.getlist('associe_parts[]')
            montants = request.POST.getlist('associe_montant[]')

            Associe.objects.filter(customer_file=customer_file).delete()

            for index in range(len(noms)):
                if noms[index] and prenoms[index]:
                    Associe.objects.create(
                        customer_file=customer_file,
                        nom=noms[index],
                        prenom=prenoms[index],
                        datn=datns[index] if index < len(datns) and datns[index] else None,
                        cine=cines[index] if index < len(cines) else "",
                        adresse=adresses[index] if index < len(adresses) else "",
                        parts=int(parts[index]) if index < len(parts) and parts[index] else 0,
                        montant=float(montants[index]) if index < len(montants) and montants[index] else 0.0,
                        user_create=request.user,
                    )
            messages.success(request, f"{len(noms)} associé(s) ont été mis à jour avec succès.")

        except Exception as e:
            messages.error(request, f"Une erreur s'est produite lors de la mise à jour : {str(e)}")
            return redirect('edit_customer_file', pk=pk)

        return redirect('edit_customer_file', pk=pk)
    
    services = Service.objects.filter(is_archived=False)
    regimes = Regime.objects.all()
    formes_juridiques = FormeJuridique.objects.all()
    comptables = Comptable.objects.all()
    qualites = Qualite.objects.all()
    documents = customer_file.edocuments.all()
    associes = customer_file.associes.all()

    return render(request, 'accounting/customer_file_edit.html', {
        'customer_file': customer_file,
        'services': services,
        'regimes': regimes,
        'formes_juridiques': formes_juridiques,
        'comptables': comptables,
        'qualites': qualites,
        'documents': documents,
        'associes': associes,
    })

def folder_client_archive(request, pk):
    """Archive ou réactive une forme juridique."""
    folder_client = get_object_or_404(CustomerFile, pk=pk)
    folder_client.is_archived = not folder_client.is_archived
    folder_client.save()
    if folder_client.is_archived:
        messages.success(request, "L'entreprise a été archivée avec succès.")
    else:
        messages.success(request, "L'entreprise a été réactivée avec succès.")
    return redirect('customer_file_list')

def gestion_mois(request):
    if request.method == "POST":
        month_id = request.POST.get("toggle_month")
        try:
            month = Month.objects.get(id=month_id)
            month.is_active = not month.is_active
            month.save()
            messages.success(request, f"Le mois {month.get_month_display()} {month.year} a été {'activé' if month.is_active else 'désactivé'}.")
        except Month.DoesNotExist:
            messages.error(request, "Le mois sélectionné n'existe pas.")

        # Redirection après traitement du formulaire
        return redirect("gestion_mois")

    months = Month.objects.all().order_by("year", "month")
    return render(request, "accounting/gestion_mois.html", {"months": months})

def generate_payments_for_month(month, year):
    try:
        selected_month = Month.objects.get(month=month, year=year)
        if not selected_month.is_active:
            return 0
    except Month.DoesNotExist:
        return 0

    # الحصول على بداية ونهاية الشهر
    _, last_day = calendar.monthrange(year, month)
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)

    # جلب جميع العملاء
    customers = CustomerFile.objects.all()
    payments_created = 0

    for customer in customers:
        # جلب الخدمات المرتبطة بالعميل
        services = CustomerService.objects.filter(
            customer_file=customer,
            date_debut__lte=end_date,
            date_fin__gte=start_date,
        )

        for service in services:
            # تأكد من أن `service` هو كائن من نوع CustomerService
            if not isinstance(service, CustomerService):
                continue  # تجاوز في حالة وجود خطأ

            payment, created = Payment.objects.get_or_create(
                customer_file=customer,
                service=service,  # يجب أن يكون `service` من نوع `CustomerService`
                month=month,
                year=year,
                defaults={"is_paid": False, "date_payment": None, "note": ""},
            )
            if created:
                payments_created += 1

    # تحديث حالة الشهر إذا تم إنشاء المدفوعات
    if payments_created > 0:
        selected_month.is_active = False
        selected_month.save()

    return payments_created

from django.http import JsonResponse

def preparation_mois(request):
    if request.method == "POST":
        if "prepare_month" in request.POST:
            month = int(request.POST.get("month"))
            year = int(request.POST.get("year"))

            try:
                selected_month = Month.objects.get(month=month, year=year)
                if not selected_month.is_active:
                    messages.error(request, f"Le mois {selected_month} n'est pas activé pour la préparation.")
                    return redirect("preparation_mois")

                payments_created = generate_payments_for_month(month, year)
                if payments_created > 0:
                    messages.success(request, f"Les paiements pour {selected_month} ont été préparés avec succès.")
                else:
                    messages.warning(request, f"Aucune nouvelle donnée à préparer pour {selected_month}.")

            except Month.DoesNotExist:
                messages.error(request, "Le mois sélectionné n'existe pas dans la base de données.")
                return redirect("preparation_mois")

        elif "payment_action" in request.POST:
            action = request.POST.get("payment_action")
            try:
                action_type, payment_id = action.split("-")
                payment = Payment.objects.get(id=payment_id)

                if action_type == "pay":
                    payment.is_paid = True
                    payment.date_payment = date.today()
                    payment.save()
                    messages.success(request, f"Le paiement pour {payment.service.service.libelle} a été confirmé.")
                elif action_type == "unpay":
                    payment.is_paid = False
                    payment.date_payment = None
                    payment.save()
                    messages.success(request, f"Le paiement pour {payment.service.service.libelle} a été annulé.")
            except (Payment.DoesNotExist, ValueError):
                messages.error(request, "Action invalide ou ID de paiement introuvable.")

    # Initialize payments as an empty list to avoid UnboundLocalError
    payments = []
    months = Month.objects.all().order_by("year", "month")
    exercices = Exercice.objects.filter(is_archived=False).order_by("libelle")
    current_year = date.today().year
    grouped_payments = {}
    selected_month = None
    total_paid = 0

    if request.method == "POST" and "prepare_month" in request.POST:
        selected_month = Month.objects.filter(month=month, year=year).first()
        if selected_month:
            payments = Payment.objects.filter(month=month, year=year).select_related('service__service', 'customer_file')
            for customer, group in groupby(
                sorted(payments, key=lambda p: p.customer_file.raison_sociale),
                key=lambda p: p.customer_file,
            ):
                grouped_payments[customer] = list(group)

            # Precompute the total of partial payments for each payment
            for payment in payments:
                total_partial = sum(partial.amount for partial in payment.service.partial_payments.all())
                payment.total_partial = total_partial

    return render(request, "accounting/preparation_mois.html", {
        "months": months,
        "exercices": exercices,
        "current_year": current_year,
        "grouped_payments": grouped_payments,
        "selected_month": selected_month,
        'total_paid': total_paid,  # Total paid for the selected month
        'payments': payments,  # Pass payments with total_partial included
    })

def partial_payment(request):
    if request.method == "POST":
        payment_id = request.POST.get("payment_id")
        amount = request.POST.get("amount")
        date_str = request.POST.get("date")
        
        # تحقق من وجود الدفع
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)

        # تحقق من صحة المبلغ
        try:
            amount = float(amount)
            if amount <= 0:
                return JsonResponse({"error": "Amount must be greater than 0"}, status=400)
        except ValueError:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        # تحقق من صحة التاريخ
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            date_obj = make_aware(datetime.combine(date_obj, datetime.min.time()))
        except ValueError:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        # استخدام الخدمة المرتبطة بالدفع (الذي يحتوي على customer_service)
        customer_service = payment.service  # استخدام service بدلاً من customer_service
        
        # إنشاء الدفع الجزئي
        partial_payment = PartialPayment(customer_service=customer_service, amount=amount, date_payment=date_obj)
        partial_payment.save()

        # تحديث حالة الدفع
        customer_service.update_payment_status()

        # إرجاع الاستجابة
        return JsonResponse({
            "amount": amount,
            "date": date_str,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

@require_POST
def delete_partial_payment(request, partial_id):
    try:
        partial_payment = PartialPayment.objects.get(id=partial_id)
        amount = partial_payment.amount
        customer_service = partial_payment.customer_service
        partial_payment.delete()

        # تحديث حالة الدفع بعد الحذف
        customer_service.update_payment_status()

        return JsonResponse({"success": True, "amount": amount})
    except PartialPayment.DoesNotExist:
        return JsonResponse({"success": False, "error": "Partial payment not found"})

@require_POST
def edit_partial_payment(request, partial_id):
    try:
        partial_payment = PartialPayment.objects.get(id=partial_id)
        old_amount = partial_payment.amount

        # تحقق من صحة المبلغ
        try:
            amount = float(request.POST.get("amount"))
            if amount <= 0:
                return JsonResponse({"success": False, "error": "Amount must be greater than 0"})
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid amount"})

        # تحقق من صحة التاريخ
        try:
            date_str = request.POST.get("date")
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            date_obj = make_aware(datetime.combine(date_obj, datetime.min.time()))
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid date format"})

        # تحديث القيم
        partial_payment.amount = amount
        partial_payment.date_payment = date_obj
        partial_payment.save()

        # تحديث حالة الدفع
        customer_service = partial_payment.customer_service
        customer_service.update_payment_status()

        return JsonResponse({
            "success": True,
            "amount": partial_payment.amount,
            "date": partial_payment.date_payment.strftime("%d/%m/%Y"),  # تنسيق التاريخ
            "old_amount": old_amount,
        })
    except PartialPayment.DoesNotExist:
        return JsonResponse({"success": False, "error": "Partial payment not found"})


def ajouter_contrat(request, contrat_id=None):
    """
    View لإضافة أو تعديل عقد.
    """
    # التحقق من حالة التعديل
    if contrat_id:
        try:
            contrat = get_object_or_404(ContratPersonnePhysique, id_contrat=contrat_id)
            print("Contrat موجود:", contrat)
        except Exception as e:
            print("خطأ في الحصول على العقد:", e)
            contrat = None
    else:
        contrat = None

    if request.method == "POST":
        # الحصول على البيانات من النموذج
        nom_prenom = request.POST.get("nom_prenom")
        loyer_mensuel_contrat = request.POST.get("loyer_mensuel_contrat")
        loyer_mensuel_plateforme = request.POST.get("loyer_mensuel_plateforme")
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")
        date_naissance = request.POST.get("date_naissance")
        lieu_naissance = request.POST.get("lieu_naissance")
        nom_pere = request.POST.get("nom_pere")
        nom_mere = request.POST.get("nom_mere")
        adresse = request.POST.get("adresse")
        date_contrat = request.POST.get("date_contrat")

        if contrat:  # حالة تعديل
            contrat.nom_prenom = nom_prenom
            contrat.loyer_mensuel_contrat = loyer_mensuel_contrat
            contrat.loyer_mensuel_plateforme = loyer_mensuel_plateforme
            contrat.date_debut = date_debut
            contrat.date_fin = date_fin
            contrat.date_naissance = date_naissance
            contrat.adresse = adresse
            contrat.date_contrat = date_contrat
            contrat.save()
            print("تم تعديل العقد:", contrat)
        else:  # حالة إنشاء جديد
            contrat = ContratPersonnePhysique.objects.create(
                nom_prenom=nom_prenom,
                loyer_mensuel_contrat=loyer_mensuel_contrat,
                loyer_mensuel_plateforme=loyer_mensuel_plateforme,
                date_debut=date_debut,
                date_fin=date_fin,
                date_naissance=date_naissance,
                nom_pere=nom_pere,
                nom_mere=nom_mere,
                adresse=adresse,
                date_contrat=date_contrat,
            )
        return redirect("liste_contrats")

    return render(request, "accounting/ajouter_contrat.html", {"contrat": contrat})

def liste_contrats(request):
    """
    View لعرض قائمة العقود.
    """
    contrats = ContratPersonnePhysique.objects.all()
    return render(request, "accounting/liste_contrats.html", {"contrats": contrats})
