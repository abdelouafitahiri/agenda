from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import date, datetime


class Societe(models.Model):
    num = models.CharField(max_length=6, null=True, verbose_name="Numéro")
    libelle = models.CharField(max_length=70, null=True, verbose_name="Raison Sociale")
    ice = models.CharField(max_length=24, null=True, verbose_name="ICE")
    if_field = models.CharField(max_length=24, null=True, verbose_name="IF")  # 'if' is a Python keyword, so use 'if_field'
    rc = models.CharField(max_length=24, null=True, verbose_name="RC")
    activite = models.TextField(max_length=250, null=True, verbose_name="Activité")
    adresse = models.CharField(max_length=250, null=True, verbose_name="Adresse")
    date_creation = models.DateField(null=True, verbose_name="Date de Création")
    gerant = models.CharField(max_length=24, null=True, verbose_name="Gérant")
    ville = models.CharField(max_length=24, null=True, verbose_name="Ville")
    cin = models.CharField(max_length=24, null=True, verbose_name="CIN")
    mail = models.EmailField(max_length=70, null=True, verbose_name="Mail")
    rib = models.CharField(max_length=34, null=True, verbose_name="RIB")  # Adding RIB field as requested
    logo = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name="Logo")
    
    # Arabic fields
    libelle_ar = models.CharField(max_length=70, null=True, verbose_name="الاسم التجاري")
    activite_ar = models.TextField(max_length=250, null=True, verbose_name="الخدمات")
    adresse_ar = models.CharField(max_length=250, null=True, verbose_name="العنوان")
    ville_ar = models.CharField(max_length=24, null=True, verbose_name="المدينة")
    gerant_ar = models.CharField(max_length=24, null=True, verbose_name="المسير")

    # Additional fields
    cnss = models.CharField(max_length=24, null=True, verbose_name="CNSS")
    header = models.CharField(max_length=225, null=True, verbose_name="En-tête")
    footer = models.CharField(max_length=225, null=True, verbose_name="Pied de page")
    capital = models.IntegerField(null=True, verbose_name="Capital")
    
    # Tracking fields
    user_create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="societe_createur", verbose_name="Créé par")
    user_edit = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="societe_editeur", verbose_name="Modifié par")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de Création en Système")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Dernière Modification")

    class Meta:
        verbose_name = "Société"
        verbose_name_plural = "Sociétés"

    def __str__(self):
        return self.libelle or "Société"

class FormeJuridique(models.Model):
    libelle = models.CharField(max_length=35, null=True, verbose_name="Libellé")
    alias = models.CharField(max_length=5, null=True, verbose_name="Alias")
    user_create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="forme_createur", verbose_name="Créé par")
    user_edit = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="forme_editeur", verbose_name="Modifié par")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Forme Juridique"
        verbose_name_plural = "Formes Juridiques"

    def __str__(self):
        return self.libelle or "Forme Juridique"

@receiver(post_migrate)
def add_default_formes_juridiques(sender, **kwargs):
    if sender.name == 'agendacomptable':
        formes_juridiques_data = [
            {"libelle": "Société à Responsabilité Limitée", "alias": "SARL"},
            {"libelle": "Société Anonyme", "alias": "SA"},
            {"libelle": "Société en Nom Collectif", "alias": "SNC"},
            {"libelle": "Société en Commandite Simple", "alias": "SCS"},
            {"libelle": "Société en Commandite par Actions", "alias": "SCA"},
            {"libelle": "Entreprise Individuelle", "alias": "EI"},
            {"libelle": "Coopérative", "alias": "Coopérative"},
        ]
        for forme_data in formes_juridiques_data:
            FormeJuridique.objects.get_or_create(libelle=forme_data["libelle"], alias=forme_data["alias"])

class Exercice(models.Model):
    libelle = models.CharField(max_length=4, null=True, verbose_name="Libellé")
    default = models.CharField(max_length=1, null=True, verbose_name="Défaut")
    user_create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="exercice_createur", verbose_name="Créé par")
    user_edit = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="exercice_editeur", verbose_name="Modifié par")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_archived = models.BooleanField(default=False, verbose_name="Archivé")

    class Meta:
        verbose_name = "Exercice"
        verbose_name_plural = "Exercices"

    def __str__(self):
        return self.libelle or "Exercice"
    

@receiver(post_migrate)
def create_exercices(sender, **kwargs):
    current_year = datetime.now().year
    for year in range(2020, current_year + 1):
        if not Exercice.objects.filter(libelle=str(year)).exists():
            Exercice.objects.create(
                libelle=str(year),
                default="1",
                is_archived=False
            )


class TypeReg(models.Model):
    libelle = models.CharField(max_length=15, null=True, verbose_name="Libellé")
    user_create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="typereg_createur", verbose_name="Créé par")
    user_edit = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="typereg_editeur", verbose_name="Modifié par")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Type de Régime"
        verbose_name_plural = "Types de Régimes"

    def __str__(self):
        return self.libelle or "Type de Régime"

class Regime(models.Model):
    libelle = models.CharField(max_length=25, null=True, verbose_name="Libellé")
    user_create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="regime_createur", verbose_name="Créé par")
    user_edit = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="regime_editeur", verbose_name="Modifié par")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Régime"
        verbose_name_plural = "Régimes"

    def __str__(self):
        return self.libelle or "Régime"

@receiver(post_migrate)
def create_regimes(sender, **kwargs):
    regimes = [
        # IR
        "Résultat net réel",
        "Résultat net simplifié",
        "Contribution professionnelle",

        # IS
        "De plein droit",
        "Sur option",
        "Option pour l'imposition forfaitaire",

        # TVA
        "De plein droit",
        "Sur option",
        "Hors champ",
        "Totalement exonéré sans droit à exonéré",
        "Totalement exonéré avec droit à déduction",

    ]
    for regime_name in regimes:
        if not Regime.objects.filter(libelle=regime_name).exists():
            Regime.objects.create(
                libelle=regime_name,
                is_archived=False
            )

class Qualite(models.Model):
    libelle = models.CharField(max_length=25, null=True, verbose_name="Libellé")
    user_create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="qualite_createur", verbose_name="Créé par")
    user_edit = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="qualite_editeur", verbose_name="Modifié par")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_archived = models.BooleanField(default=False, verbose_name="Archivé")  # Champ pour indiquer si l'enregistrement est archivé

    class Meta:
        verbose_name = "Qualité"
        verbose_name_plural = "Qualités"

    def __str__(self):
        return self.libelle or "Qualité"

@receiver(post_migrate)
def create_qualites(sender, **kwargs):
    qualites = [
        "Gérant Associé unique",
        "Gérant Associé",
        "Co-Gérant Associé",
        "Co-Gérant non Associé",
        "Associé",
        "Gérant non Associé"
    ]
    
    for qualite in qualites:
        if not Qualite.objects.filter(libelle=qualite).exists():  # Corrected 'qualiste' to 'qualite'
            Qualite.objects.create(
                libelle=qualite,
                is_archived=False
            )

class CriteresPaiement(models.Model):
    libelle = models.CharField(max_length=50, null=True, verbose_name="Type de Paiement")
    description = models.TextField(null=True, blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Critère de Paiement"
        verbose_name_plural = "Critères de Paiement"

    def __str__(self):
        return self.libelle or "Critère de Paiement"

@receiver(post_migrate)
def add_default_criteres_paiement(sender, **kwargs):
    if sender.name == 'agendacomptable':
        default_criteres = [
            {"libelle": "Mensuel", "description": "Paiement effectué chaque mois"},
            {"libelle": "Trimestriel", "description": "Paiement effectué tous les trois mois"},
            {"libelle": "Semestriel", "description": "Paiement effectué tous les six mois"},
            {"libelle": "Annuel", "description": "Paiement effectué une fois par an"},
        ]
        for critere_data in default_criteres:
            CriteresPaiement.objects.get_or_create(libelle=critere_data["libelle"], defaults=critere_data)

class Service(models.Model):
    libelle = models.CharField(max_length=75, null=True, verbose_name="Libellé")
    prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name="Prix")
    etat = models.CharField(max_length=1, default='T', verbose_name="État")
    criteres_paiement = models.ForeignKey(CriteresPaiement, on_delete=models.SET_NULL, null=True, verbose_name="Critère de Paiement")
    user_create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="service_createur", verbose_name="Créé par")
    user_edit = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="service_editeur", verbose_name="Modifié par")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.libelle or "Service"


@receiver(post_migrate)
def create_services(sender, **kwargs):
    # التأكد من أن البيانات الافتراضية موجودة
    add_default_criteres_paiement(sender, **kwargs)
    
    services_data = [
        ("Domiciliation", 1500.00, "Mensuel"),
        ("Expertise Comptable", 1500.00, "Mensuel"),
        ("Audit", 2000.00, "Mensuel"),
        ("Consulting Fiscalité", 1800.00, "Mensuel"),
        ("Services de Paie", 1200.00, "Mensuel"),
        ("Conseil Juridique", 2500.00, "Mensuel"),
        ("Consulting Stratégique", 2200.00, "Mensuel"),
    ]

    for libelle, prix, critere_libelle in services_data:
        try:
            criteres_paiement = CriteresPaiement.objects.get(libelle=critere_libelle)
        except CriteresPaiement.DoesNotExist:
            print(f"Critère de paiement '{critere_libelle}' introuvable. Service '{libelle}' ignoré.")
            continue

        Service.objects.get_or_create(
            libelle=libelle,
            defaults={
                "prix": prix,
                "etat": 'T',
                "criteres_paiement": criteres_paiement,
                "is_archived": False,
            },
        )

class Comptable(models.Model):
    lib_08 = models.CharField(max_length=25, blank=True, null=True)
    adr_08 = models.CharField(max_length=75, blank=True, null=True)
    mail_08 = models.EmailField(max_length=35, blank=True, null=True)
    tel_08 = models.CharField(max_length=12, blank=True, null=True)
    contact_08 = models.CharField(max_length=25, blank=True, null=True)
    user_create_08 = models.ForeignKey(User, related_name='created_comptables', on_delete=models.SET_NULL, null=True, blank=True)
    user_edit_08 = models.ForeignKey(User, related_name='edited_comptables', on_delete=models.SET_NULL, null=True, blank=True)
    date_create_08 = models.DateTimeField(auto_now_add=True)
    date_edit_08 = models.DateTimeField(auto_now=True)
    default_08 = models.CharField(max_length=1, default='F', blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Comptable'
        verbose_name_plural = 'Comptables'

    def __str__(self):
        return f"{self.lib_08} - {self.contact_08}"



class FiscalRegime(models.Model):
    type = models.CharField(max_length=50, verbose_name="Type de Régime")
    option = models.CharField(max_length=50, verbose_name="Option", null=True, blank=True)
    tva_period = models.CharField(
        max_length=20,
        choices=[('Mensuelle', 'Mensuelle'), ('Trimestrielle', 'Trimestrielle')],
        verbose_name="Période (TVA)",
        null=True,
        blank=True
    )
    customer_file = models.ForeignKey(
        'CustomerFile',
        related_name='fiscal_regimes',
        on_delete=models.CASCADE,
        verbose_name="Fiche Client"
    )

    def __str__(self):
        return f"{self.type} - {self.option or 'N/A'}"

    def clean(self):
        """
        Verify that tva_period is only set when type is 'TVA'.
        """
        if self.type != 'TVA' and self.tva_period:
            raise ValidationError({'tva_period': 'Le champ "Période (TVA)" ne peut être rempli que pour le régime TVA.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Trigger the validation
        super().save(*args, **kwargs)


class CustomerFile(models.Model):
    raison_sociale = models.CharField(max_length=70, verbose_name="Raison Sociale")
    activite = models.CharField(max_length=100, verbose_name="Activité")
    ville = models.CharField(max_length=45, verbose_name="Ville")
    adresse = models.TextField(verbose_name="Adresse")
    email = models.EmailField(max_length=100, verbose_name="E-Mail")
    contacts = models.ManyToManyField('Contact', related_name="customer_files", verbose_name="Contacts", blank=True)
    forme_juridique = models.ForeignKey('FormeJuridique', on_delete=models.SET_NULL, null=True)
    date_creation = models.DateField(null=True)
    ice = models.CharField(max_length=24, verbose_name="ICE", null=True, blank=True)
    identifiant_fiscal = models.CharField(max_length=24, verbose_name="IF", null=True, blank=True)
    cnss = models.CharField(max_length=24, verbose_name="CNSS", null=True, blank=True)
    registre_commerce = models.CharField(max_length=24, verbose_name="RC", null=True, blank=True)
    domiciliation = models.BooleanField(default=False)
    tenue_comptabilite = models.BooleanField(default=False)
    cabinet_comptable = models.ForeignKey('Comptable', on_delete=models.SET_NULL, null=True, blank=True)
    date_reception_dossier = models.DateField(null=True, blank=True)
    user_create = models.ForeignKey(User, related_name="customerfile_created_by", on_delete=models.SET_NULL, null=True)
    user_edit = models.ForeignKey(User, related_name="customerfile_edited_by", on_delete=models.SET_NULL, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.raison_sociale



class Contact(models.Model):
    
    customer_file = models.ForeignKey(
        CustomerFile,
        on_delete=models.CASCADE,
        related_name="customer_contacts"  # Set unique related_name
    )
    nom_complet = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)

    user_create = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="created_contacts"
    )
    user_edit = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="edited_contacts"
    )
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_complet

class PartialPayment(models.Model):
    customer_service = models.ForeignKey('CustomerService', related_name="partial_payments", on_delete=models.CASCADE, verbose_name="Customer Service")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Payment Amount")
    date_payment = models.DateTimeField(auto_now_add=True, verbose_name="Payment Date")
    month = models.DateField(verbose_name="Payment Month")  # حقل جديد لتحديد الشهر

    def __str__(self):
        return f"{self.amount} MAD on {self.date_payment.strftime('%d/%m/%Y')} for {self.customer_service}"

class CustomerService(models.Model):
    customer_file = models.ForeignKey(CustomerFile, related_name="services", on_delete=models.CASCADE, verbose_name="Customer File")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    date_debut = models.DateField(verbose_name="Start Date")
    date_fin = models.DateField(verbose_name="End Date")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Last Modified")

    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total Paid")
    is_fully_paid = models.BooleanField(default=False, verbose_name="Fully Paid")
    
    def update_payment_status(self):
        self.total_paid = sum(payment.amount for payment in self.partial_payments.all())
        self.is_fully_paid = self.total_paid >= self.prix
        self.save()

    def __str__(self):
        return f"{self.service.libelle} for {self.customer_file.raison_sociale}"

class Associe(models.Model):
    customer_file = models.ForeignKey(CustomerFile, related_name="associes", on_delete=models.CASCADE)
    nom = models.CharField(max_length=45, verbose_name="Nom", null=True, blank=True)
    prenom = models.CharField(max_length=45, verbose_name="Prénom", null=True, blank=True)
    datn = models.DateField(verbose_name="Date de Naissance", null=True, blank=True)
    cine = models.CharField(max_length=45, verbose_name="CIN", null=True, blank=True)
    adresse = models.CharField(max_length=45, verbose_name="Adresse", null=True, blank=True)
    parts = models.IntegerField(verbose_name="Parts", null=True, blank=True)
    montant = models.FloatField(verbose_name="Montant", null=True, blank=True)
    user_create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Créé par")
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class EDocument(models.Model):
    customer_file = models.ForeignKey(CustomerFile, related_name="edocuments", on_delete=models.CASCADE)
    file = models.FileField(upload_to="documents/", verbose_name="Fichier")
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Document for {self.customer_file}"

class Month(models.Model):
    MONTH_CHOICES = [
        (1, "Janvier"), (2, "Février"), (3, "Mars"), (4, "Avril"),
        (5, "Mai"), (6, "Juin"), (7, "Juillet"), (8, "Août"),
        (9, "Septembre"), (10, "Octobre"), (11, "Novembre"), (12, "Décembre"),
    ]

    year = models.IntegerField(verbose_name="Année")
    month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, verbose_name="Mois")
    is_active = models.BooleanField(default=False, verbose_name="Activé pour la préparation")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        unique_together = ("year", "month")
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"{self.get_month_display()} {self.year} - {'Activé' if self.is_active else 'Désactivé'}"

@receiver(post_migrate)
def create_current_year_months(sender, **kwargs):
    current_year = date.today().year

    for month in range(1, 13):
        Month.objects.get_or_create(year=current_year, month=month)
    print(f"Les mois de {current_year} ont été créés ou mis à jour avec succès.")

class Payment(models.Model):
    customer_file = models.ForeignKey(
        'CustomerFile', on_delete=models.CASCADE, related_name="payments",
        verbose_name="Dossier Client"
    )
    service = models.ForeignKey(
        'CustomerService', on_delete=models.CASCADE, related_name="payments",
        verbose_name="Service"
    )
    month = models.IntegerField(verbose_name="Mois")
    year = models.IntegerField(verbose_name="Année")
    is_paid = models.BooleanField(default=False, verbose_name="Payé")
    date_payment = models.DateField(null=True, blank=True, verbose_name="Date de Paiement")
    note = models.TextField(null=True, blank=True, verbose_name="Notes")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de Création")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Date de Modification")

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        unique_together = ('customer_file', 'service', 'month', 'year')  # Assurer l'unicité des paiements pour le même mois/année.

    def __str__(self):
        return f"{self.service.service.libelle} ({self.month}/{self.year}) - {'Payé' if self.is_paid else 'Non Payé'}"

class ContratPersonnePhysique(models.Model):
    customer_file = models.ForeignKey(
        CustomerFile,
        related_name="contrats_physiques",
        on_delete=models.CASCADE,
        verbose_name="Fichier Client"
    )
    nom_prenom = models.CharField(max_length=255, verbose_name="Nom et Prénom")
    loyer_mensuel_contrat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Loyer mensuel (contrat)")
    loyer_mensuel_plateforme = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Loyer mensuel (plateforme)")
    date_debut = models.DateField(verbose_name="Date de Début")
    date_fin = models.DateField(verbose_name="Date de Fin")
    date_naissance = models.DateField(null=True, blank=True, verbose_name="Date de Naissance")
    adresse = models.TextField(null=True, blank=True, verbose_name="Adresse")
    date_contrat = models.DateField(verbose_name="Date du Contrat")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de Création")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Date de Modification")

    @property
    def duree_contrat(self):
        """
        Calculer la durée du contrat en jours, mois, et années.
        """
        if self.date_debut and self.date_fin:
            delta = self.date_fin - self.date_debut
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30
            return f"{years} ans, {months} mois, {days} jours"
        return "Durée inconnue"

class ContratPersonneMorale(models.Model):
    customer_file = models.ForeignKey(
        CustomerFile, 
        related_name="contrats_moraux", 
        on_delete=models.CASCADE, 
        verbose_name="Fichier Client"
    )
    nom_soc = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nom de la société")
    id_contrat = models.AutoField(primary_key=True, verbose_name="Numéro du contrat")
    registre_commerce = models.CharField(max_length=255, verbose_name="Numéro du registre de commerce")
    nom_representant = models.CharField(max_length=255, verbose_name="Nom complet du représentant légal")
    cin_representant = models.CharField(max_length=50, verbose_name="CIN du représentant légal")
    date_naissance_representant = models.DateField(null=True, blank=True, verbose_name="Date de naissance du représentant légal")
    adresse = models.TextField(null=True, blank=True, verbose_name="Adresse")
    loyer_mensuel_contrat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Loyer mensuel (contrat)")
    loyer_mensuel_plateforme = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Loyer mensuel (plateforme)")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    date_contrat = models.DateField(verbose_name="Date du contrat")
    periode_renouvellement = models.CharField(max_length=50, null=True, blank=True, verbose_name="Période de renouvellement")
    user_create = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="contrats_personne_morale_createur",  # Nom unique
        verbose_name="Créé par"
    )
    user_edit = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="contrats_personne_morale_editeur",  # Nom unique
        verbose_name="Modifié par"
    )
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Date de Création en Système")
    date_edit = models.DateTimeField(auto_now=True, verbose_name="Dernière Modification")

    def __str__(self):
        return f"Contrat #{self.id_contrat} - {self.id_contrat}"
    
    @property
    def duree_contrat(self):
        """
        Calculer la durée du contrat en jours, mois, et années.
        """
        if self.date_debut and self.date_fin:
            delta = self.date_fin - self.date_debut
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30
            return f"{years} ans, {months} mois, {days} jours"
        return "Durée inconnue"