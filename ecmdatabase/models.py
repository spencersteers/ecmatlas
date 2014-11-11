from django.db import models


# TODO: Choices to CharField/Tables
SPECIES_CHOICES = (
    ('HOMO SAPIENS','Homo Sapiens'),
    ('BOVINE','Bovine'),
    ('RATTUS','Rattus'),
    ('MUS MUS','Mus mus'),
    ('OTHER PRIMATES','Other Primates'),
    ('SHARED', 'Shared')
)

TYPE_CHOICES = (
    ('PRIMARY TISSUE','Primary tissue'),
    ('ISOLATED/CULTURES CELLS', 'Isolated/Cultured cells'),
)

EXTRACTION_METHOD_CHOICES = (
    ('SDS','SDS'),
    ('UREA','Urea'),
    ('TFE', 'TFE'),
    ('GDN-HCI','Gdn-HCI'),
    ('CHEMIVAL DIGESTION','Chemical Digestion'),
    ('OTHER','Other'),
)

TISSUE_CHOICES = (
    ('BONE', 'Bone'),
    ('TENDON', 'Tendon'),
    ('BRAIN', 'Brain'),
    ('EYE', 'Eye'),
    ('PROSTATE', 'Prostate'),
    ('LIVER', 'Liver'),
    ('LUNG', 'Lung'),
    ('KIDNEY', 'Kidney'),
    ('SKIN', 'Skin'),
    ('STOMACH', 'Stomach'),
    ('LOWER GI', 'Lower GI'),
    ('SKELETAL MUSCLE', 'Skeletal Muscle'),
    ('MAMMARY GLAND', 'Mammary Gland'),
    ('OVARY', 'Ovary'),
    ('TESTIS', 'Testis'),
    ('THYROID', 'Thyroid'),
    ('PANCREAS', 'Pancreas'),
    ('WHITE FAT', 'White Fat'),
    ('BROWN FAT', 'Brown Fat'),
    ('HEART', 'Heart'),
    ('SPLEEN', 'Spleen'),
    ('UTERUS', 'Uterus'),
    ('BLOOD','Blood'),
    ('LYMPH','Lymph'),
    ('URINE','Urine'),
)

FLUID_CHOICES = (
    ('BLOOD','Blood'),
    ('LYMPH','Lymph'),
    ('URINE','Urine'),
)

EXPIREMENT_TYPE = (
    ('GLOBAL','global'),
    ('TARGETED','targeted'),
)

# END_TODO

#temp
class Tissue(models.Model):
    name                     = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.name)

class Protein(models.Model):
    '''
    This is the proteins' common data among all experiments
    '''
    sequence                 = models.TextField()
    gene_name                = models.CharField(max_length=255)
    protein_name             = models.CharField(max_length=255, null=True)
    species                  = models.CharField(max_length=255, null=True)
    tissues                  = models.ManyToManyField(Tissue, related_name='proteins')

    def __str__(self):
        return str(self.sequence) + ": " + str(self.protein_name)

class Experiment(models.Model):
    '''
    This is the base experiment model that will contain experiment specific data
    '''
    species                             = models.CharField(max_length=45,choices=SPECIES_CHOICES, null=True)
    tissue                              = models.CharField(max_length=45, choices=TISSUE_CHOICES, null=True)
    tissue_type                         = models.CharField(max_length=45, choices=TYPE_CHOICES, null=True)
    extraction_method                   = models.CharField(max_length=45, choices=EXTRACTION_METHOD_CHOICES, null=True)
    search_title                        = models.CharField(max_length=45,null=True, unique=True)
    timestamp                           = models.DateTimeField(null=True, unique=True)
    expirement_type                     = models.CharField(max_length=8, choices=EXPIREMENT_TYPE, null=True, default="global")
    user                                = models.CharField(max_length=45, null=True)
    email                               = models.CharField(max_length=45, null=True)
    report_uri                          = models.CharField(max_length=255,null=True)
    peak_list_data_path                 = models.CharField(max_length=45, null=True)
    peak_list_format                    = models.CharField(max_length=45, null=True)
    search_type                         = models.CharField(max_length=45, null=True)
    mascot_version                      = models.CharField(max_length=45, null=True)
    database                            = models.CharField(max_length=45, null=True) #one-to-many should be extracted
    fasta_file                          = models.CharField(max_length=45, null=True) #one-to-many should be extracted
    total_sequences                     = models.BigIntegerField(null=True)
    total_residues                      = models.BigIntegerField(null=True)
    sequences_after_taxonomy_filter     = models.BigIntegerField(null=True)
    number_of_queries                   = models.BigIntegerField(null=True)
    warning                             = models.CharField(max_length=255, null=True)
    taxonomy_filter                     = models.CharField(max_length=45, null=True)
    enzyme                              = models.CharField(max_length=45, null=True)
    maximum_missed_cleavages            = models.IntegerField(null=True)
    quantitation_method                 = models.CharField(max_length=45, null=True)
    peptide_mass_tolerance              = models.FloatField(null=True)
    peptide_mass_tolerance_units        = models.CharField(max_length=10, null=True)
    fragment_mass_tolerance             = models.FloatField(null=True)
    fragment_mass_tolerance_units       = models.CharField(max_length=10, null=True)
    mass_values                         = models.CharField(max_length=45, null=True)
    instrument_type                     = models.CharField(max_length=45, null=True)
    isotope_error_mode                  = models.IntegerField(null=True)
    significance_threshold              = models.FloatField(null=True)
    max_number_of_hits                  = models.BooleanField(default=False)
    use_mud_pit_protein_scoring         = models.BooleanField(default=False)
    ions_score_cutoff                   = models.BooleanField(default=False)
    include_sameset_proteins            = models.BooleanField(default=False)
    include_subset_proteins             = models.BooleanField(default=False)
    include_unassigned                  = models.BooleanField(default=False)
    require_bold_red                    = models.BooleanField(default=False)
    use_homology_threshold              = models.BooleanField(default=False)
    group_protein_families              = models.BooleanField(default=False)
    validated                           = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ": " + str(self.search_title) + " " + str(self.timestamp)

class ProteinHit(models.Model):
    '''
    This is the proteins that where hit in experiments
    '''
    experiment                  = models.ForeignKey(Experiment)
    protein                     = models.ForeignKey(Protein)
    gene_name                   = models.CharField(max_length=45)
    hit_number                  = models.IntegerField(null=True)
    family_member               = models.CharField(max_length=45,null=True)
    score                       = models.IntegerField(null=True)
    mass                        = models.IntegerField(null=True)

    # report normalized version of mass As a fraction of the total in a complete excitement
    # this is done as Mass/Mass of all protiens in expirement
    normalized_matches          = models.FloatField(null=True)
    matches                     = models.IntegerField(null=True)

    # do we weigh the matches in the same way?
    matches_significance        = models.IntegerField(null=True)
    sequences                   = models.IntegerField(null=True)
    sequences_signigicance      = models.IntegerField(null=True)
    coverage                    = models.FloatField(null=True)
    validated                   = models.BooleanField(default=True)

    def __str__(self):
        return str(self.hit_number) + ": " + str(self.gene_nme)

class VariableModification(models.Model):
    '''
    This holds modified variable constants for the expirements
    '''
    experiment                  = models.ForeignKey(Experiment, null=True)
    name                        = models.CharField(max_length=45, null=True)
    delta                       = models.FloatField(null=True)
    neutral_losses              = models.CharField(max_length=255, null=True)
    validated                   = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + ": " + str(self.name) + " " + str(self.delta)
