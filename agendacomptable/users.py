from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db.models import Count
from .models import *

def user_list(request):
    """Liste tous les utilisateurs."""
    users = User.objects.all()  # Récupérer tous les utilisateurs

    # Gérer les actions du formulaire
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')

        if action == 'add':  # Ajouter un nouvel utilisateur
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            is_admin = request.POST.get('is_admin') == 'true'  # Vérifier si c'est un administrateur

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.warning(request, "Le nom d'utilisateur existe déjà.")
                elif User.objects.filter(email=email).exists():
                    messages.warning(request, "L'email existe déjà.")
                else:
                    user = User.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password1
                    )
                    if is_admin:
                        user.is_staff = True  # Rendre l'utilisateur administrateur
                        user.is_superuser = True  # Rendre l'utilisateur super administrateur
                    user.save()  # Enregistrer l'utilisateur
                    messages.success(request, "L'utilisateur a été ajouté avec succès.")
                    return redirect('user-list')
            else:
                messages.warning(request, "Les mots de passe ne correspondent pas.")
        
        elif action == 'delete':
            user = get_object_or_404(User, id=user_id)  # Récupérer l'utilisateur à supprimer
            if user.is_superuser and User.objects.filter(is_superuser=True).count() <= 1:
                messages.warning(request, "Vous ne pouvez pas supprimer le seul administrateur.")
            else:
                user.delete()  # Supprimer l'utilisateur
                messages.success(request, "L'utilisateur a été supprimé avec succès.")
        
        elif action == 'archive':
            user = get_object_or_404(User, id=user_id)  # Récupérer l'utilisateur à archiver
            user.is_active = False  # Archiver l'utilisateur
            user.save()
            messages.success(request, "L'utilisateur a été archivé avec succès.")
        
        elif action == 'activate':
            user = get_object_or_404(User, id=user_id)  # Récupérer l'utilisateur à activer
            user.is_active = True  # Activer l'utilisateur
            user.save()
            messages.success(request, "L'utilisateur a été activé avec succès.")

        elif action == 'edit':
            user = get_object_or_404(User, id=user_id)  # Récupérer l'utilisateur à modifier
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            if request.POST['password']:
                user.set_password(request.POST['password'])  # Changer le mot de passe si fourni
            user.save()  # Enregistrer les modifications
            messages.success(request, "Les informations de l'utilisateur ont été mises à jour avec succès.")

    return render(request, 'accounting/user_list.html', {'users': users})
