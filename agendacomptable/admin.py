from django.contrib import admin
from .models import *


@admin.register(Societe)
class SocieteAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'num', 'libelle', 'ice', 'if_field', 'rc', 'ville', 'gerant', 
        'date_creation', 'capital', 'user_create', 'user_edit', 'date_edit'
    )
    
    # Fields to enable search functionality
    search_fields = ('libelle', 'libelle_ar', 'ice', 'if_field', 'rc', 'gerant', 'gerant_ar', 'mail', 'ville', 'ville_ar')
    
    # Fields to filter by in the list view
    list_filter = ('date_creation', 'ville', 'user_create', 'user_edit')
    
    # Fields to be displayed in the form view
    fieldsets = (
        (None, {
            'fields': (
                ('num', 'libelle', 'libelle_ar'),
                ('ice', 'if_field', 'rc'),
                ('activite', 'activite_ar'),
                ('adresse', 'adresse_ar'),
                ('ville', 'ville_ar'),
                ('gerant', 'gerant_ar'),
                ('mail', 'rib', 'cnss'),
                'logo',
                'capital',
                'header',
                'footer',
            ),
        }),
        ('Dates', {
            'fields': (('date_creation', 'date_create', 'date_edit'),),
        }),
        ('Tracking', {
            'fields': (('user_create', 'user_edit'),),
            'classes': ('collapse',),
        }),
    )
    
    # Make certain fields read-only
    readonly_fields = ('date_create', 'date_edit', 'user_create', 'user_edit')
    
    # Automatically set user_create and user_edit fields
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is new
            obj.user_create = request.user
        obj.user_edit = request.user
        super().save_model(request, obj, form, change)

@admin.register(FormeJuridique)
class FormeJuridiqueAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'alias', 'is_archived', 'date_create', 'date_edit')
    list_filter = ('is_archived',)
    search_fields = ('libelle', 'alias')
    list_editable = ('is_archived',)
    fieldsets = (
        (None, {
            'fields': ('libelle', 'alias', 'is_archived')
        }),
        ('System Info', {
            'fields': ('user_create', 'user_edit', 'date_create', 'date_edit')
        }),
    )

@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'default', 'is_archived', 'date_create', 'date_edit')
    list_filter = ('is_archived',)
    search_fields = ('libelle',)
    list_editable = ('is_archived',)
    fieldsets = (
        (None, {
            'fields': ('libelle', 'default', 'is_archived')
        }),
        ('System Info', {
            'fields': ('user_create', 'user_edit', 'date_create', 'date_edit')
        }),
    )

@admin.register(TypeReg)
class TypeRegAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'is_archived', 'date_create', 'date_edit')
    list_filter = ('is_archived',)
    search_fields = ('libelle',)
    list_editable = ('is_archived',)
    fieldsets = (
        (None, {
            'fields': ('libelle', 'is_archived')
        }),
        ('System Info', {
            'fields': ('user_create', 'user_edit', 'date_create', 'date_edit')
        }),
    )

@admin.register(Regime)
class RegimeAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'is_archived', 'date_create', 'date_edit')
    list_filter = ('is_archived',)
    search_fields = ('libelle',)
    list_editable = ('is_archived',)
    fieldsets = (
        (None, {
            'fields': ('libelle', 'is_archived')
        }),
        ('System Info', {
            'fields': ('user_create', 'user_edit', 'date_create', 'date_edit')
        }),
    )

@admin.register(Qualite)
class QualiteAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'is_archived', 'date_create', 'date_edit')
    list_filter = ('is_archived',)
    search_fields = ('libelle',)
    list_editable = ('is_archived',)
    fieldsets = (
        (None, {
            'fields': ('libelle', 'is_archived')
        }),
        ('System Info', {
            'fields': ('user_create', 'user_edit', 'date_create', 'date_edit')
        }),
    )

@admin.register(CriteresPaiement)
class CriteresPaiementAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'description')
    search_fields = ('libelle',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'prix', 'etat', 'criteres_paiement', 'is_archived', 'date_create', 'date_edit')
    list_filter = ('etat', 'criteres_paiement', 'is_archived')
    search_fields = ('libelle',)
    list_editable = ('etat', 'is_archived')
    fieldsets = (
        (None, {
            'fields': ('libelle', 'prix', 'etat', 'criteres_paiement', 'is_archived')
        }),
        ('System Info', {
            'fields': ('user_create', 'user_edit', 'date_create', 'date_edit')
        }),
    )

@admin.register(Comptable)
class ComptableAdmin(admin.ModelAdmin):
    list_display = ('lib_08', 'adr_08', 'mail_08', 'tel_08', 'contact_08', 'default_08', 'is_archived', 'date_create_08', 'date_edit_08')
    list_filter = ('default_08', 'is_archived')
    search_fields = ('lib_08', 'contact_08')
    list_editable = ('default_08', 'is_archived')
    fieldsets = (
        (None, {
            'fields': ('lib_08', 'adr_08', 'mail_08', 'tel_08', 'contact_08', 'default_08', 'is_archived')
        }),
        ('System Info', {
            'fields': ('user_create_08', 'user_edit_08', 'date_create_08', 'date_edit_08')
        }),
    )


class AssocieInline(admin.TabularInline):
    model = Associe
    extra = 1

class CustomerServiceInline(admin.TabularInline):
    model = CustomerService
    extra = 1
    fields = ('service', 'prix', 'date_debut', 'date_fin')
    verbose_name = "Customer Service"
    verbose_name_plural = "Customer Services"

class EDocumentInline(admin.TabularInline):
    model = EDocument
    extra = 1


class ContactInline(admin.TabularInline):
    model = CustomerFile.contacts.through
    extra = 1

@admin.register(CustomerFile)
class CustomerFileAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'regime_tva', 'forme_juridique', 'domiciliation', 'tenue_comptabilite', 'date_creation')
    inlines = [AssocieInline, CustomerServiceInline, EDocumentInline, ContactInline]
    fieldsets = (
            ('Information Générale', {
                'fields': ('raison_sociale', 'activite', 'ville', 'adresse')
            }),
            ('Informations Juridiques', {
                'fields': ('regime_tva', 'forme_juridique', 'date_creation', 'ice', 'identifiant_fiscal', 'cnss', 'registre_commerce')
            }),
            ('Options de Service', {
                'fields': ('domiciliation', 'tenue_comptabilite', 'cabinet_comptable', 'date_reception_dossier')
            }),
        )

    exclude = ('contacts',)
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user_create = request.user
        obj.user_edit = request.user
        super().save_model(request, obj, form, change)





@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'telephone')

@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ("year", "month", "is_active", "date_created", "date_updated")
    list_filter = ("year", "is_active")
    ordering = ("-year", "-month")
    actions = ["activate_months", "deactivate_months"]

    @admin.action(description="Activer les mois sélectionnés")
    def activate_months(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Désactiver les mois sélectionnés")
    def deactivate_months(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_file', 'service', 'month', 'year', 'is_paid', 'date_payment')

@admin.register(ContratPersonnePhysique)
class ContratPersonnePhysiqueAdmin(admin.ModelAdmin):
    list_display = ("nom_prenom", "date_contrat", "loyer_mensuel_contrat", "date_debut", "date_fin")
    search_fields = ("nom_prenom", "date_contrat", "adresse")
    list_filter = ("date_debut", "date_fin")

@admin.register(ContratPersonneMorale)
class ContratPersonneMoraleAdmin(admin.ModelAdmin):
    list_display = ("registre_commerce", "nom_representant", "date_contrat", "loyer_mensuel_contrat", "date_debut", "date_fin")
    search_fields = ("nom_representant", "registre_commerce", "customer_file__raison_sociale")
    list_filter = ("date_contrat", "date_debut", "date_fin")
    readonly_fields = ("cree_le", "mis_a_jour_le")  # Ensure these fields exist in the model


