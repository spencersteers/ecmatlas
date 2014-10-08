'''
Created on Oct 12, 2013 for the CU Anchutz ECMAtlas Project

@author: joshua underwood
'''
from django.db import models
from django.forms import ModelForm

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

SPECIES_CHOICES = (
        ('HOMO SAPIENS','Homo Sapiens'), 
        ('BOVINE','Bovine'),
        ('RATTUS','Rattus'), 
        ('MUS MUS','Mus mus'), 
        ('OTHER PRIMATES','Other Primates'),
    )
    
# (Subcategory, important to capture)
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


class Experiments(models.Model):
    '''
    This is the base experiment model that will contain experiment specific data
    '''
    #Primary Key
    #idExperiments = models.AutoField(primary_key=True) 
    #Foreign Keys
    #Data
    #--Header--
    Species                         = models.CharField(max_length=45,choices=SPECIES_CHOICES, null=True)
    Tissue                          = models.CharField(max_length=45, choices=TISSUE_CHOICES, null=True)
    TissueType                      = models.CharField(max_length=45, choices=TYPE_CHOICES, null=True)
    #fluid                           = models.CharField(max_length=45, choices=FLUID_CHOICES, null=True)
    ExtractionMethod                = models.CharField(max_length=45, choices=EXTRACTION_METHOD_CHOICES, null=True)
    SearchTitle                     = models.CharField(max_length=45,null=True, unique=True)
    Timestamp                       = models.DateTimeField(null=True, unique=True)
    ExpirementType                  = models.CharField(max_length=8, choices=EXPIREMENT_TYPE, null=True, default="global")
    User                            = models.CharField(max_length=45, null=True)
    Email                           = models.CharField(max_length=45, null=True)
    ReportURI                       = models.CharField(max_length=255,null=True)
    PeakListDataPath                = models.CharField(max_length=45, null=True)
    PeakListFormat                  = models.CharField(max_length=45, null=True)
    SearchType                      = models.CharField(max_length=45, null=True)
    MascotVersion                   = models.CharField(max_length=45, null=True)
    Database                        = models.CharField(max_length=45, null=True) #one-to-many should be extracted
    FastaFile                       = models.CharField(max_length=45, null=True) #one-to-many should be extracted
    TotalSequences                  = models.BigIntegerField(null=True)
    TotalResidues                   = models.BigIntegerField(null=True)
    SequencesAfterTaxonomyFilter    = models.BigIntegerField(null=True)
    NumberOfQueries                 = models.BigIntegerField(null=True)
    Warning                         = models.CharField(max_length=255, null=True)
    #--SearchParamaters--
    TaxonomyFilter                  = models.CharField(max_length=45, null=True)
    Enzyme                          = models.CharField(max_length=45, null=True)
    MaximumMissedCleavages          = models.IntegerField(null=True)
    #FixedModifications              = models.CharField(max_length=45, null=True)
    QuantitationMethod              = models.CharField(max_length=45, null=True)
    #VariableModifications           = models.ForeignKey(VariableModifications)
    PeptideMassTolerance            = models.FloatField(null=True)
    PeptideMassToleranceUnits       = models.CharField(max_length=10, null=True)
    FragmentMassTolerance           = models.FloatField(null=True)
    FragmentMassToleranceUnits      = models.CharField(max_length=10, null=True)
    MassValues                      = models.CharField(max_length=45, null=True)
    InstrumentType                  = models.CharField(max_length=45, null=True)
    IsotopeErrorMode                = models.IntegerField(null=True)
    #--FormatParameters--
    SignificanceThreshold           = models.FloatField(null=True)
    MaxNumberOfHits                 = models.BooleanField()
    UseMudPITProteinScoring         = models.BooleanField()
    IonsScoreCutoff                 = models.BooleanField()
    IncludeSamesetProteins          = models.BooleanField()
    IncludeSubsetProteins           = models.BooleanField()
    IncludeUnassigned               = models.BooleanField()
    RequireBoldRed                  = models.BooleanField()
    UseHomologyThreshold            = models.BooleanField()
    GroupProteinFamilies            = models.BooleanField()
    validated                       = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.id) + ": " + str(self.SearchTitle) + " " + str(self.Timestamp)
    
class VariableModifications(models.Model):
    '''
    This holds modified variable constants for the expirements
    '''
    #Primary Key
    #idVariableModifications = models.AutoField(primary_key=True)
    #Foreign Keys
    ExperimentID = models.ForeignKey(Experiments,null=True) 
    #Data    
    name          = models.CharField(max_length=45,null=True)
    delta         = models.FloatField(null=True)
    neutralLosses = models.CharField(max_length=255,null=True)
    validated     = models.BooleanField(default=True)
    
    def __unicode__(self):
        return str(self.id) + ": " + str(self.name) + " " + str(self.delta)
    



class Proteins(models.Model):
    '''
    This is the proteins' common data among all experiments
    '''
    #Primary Key
    #Foreign Keys
    #Data    
    LongGeneName            = models.CharField(max_length=45)#, unique=True)
    GeneName                = models.CharField(max_length=45)#, unique=True)
    ProtAcc                 = models.CharField(max_length=45,null=True)
    Name                    = models.CharField(max_length=45,null=True)
    Species                 = models.CharField(max_length=45, choices=SPECIES_CHOICES, null=True)
    Length                  = models.IntegerField(null=True)
    IsoelectricPoint        = models.IntegerField(null=True)
    TaxidermyString         = models.CharField(max_length=45,null=True)
    TaxidermyID             = models.IntegerField(null=True)
    Sequence                = models.TextField(null=True)
    validated               = models.BooleanField(default=True)
    
    def __unicode__(self):
        return str(self.id) + ": " + str(self.GeneName) + " " + str(self.ProtAcc)
    
#class ProteinsForm(ModelForm):
#    class Meta:
#        model = Proteins

# Creating a form to add an article.
#>>> form = ArticleForm()

# Creating a form to change an existing article.
#>>> article = Article.objects.get(pk=1)
#>>> form = ArticleForm(instance=article)

class ProteinHits(models.Model):
    '''
    This is the proteins that where hit in experiments
    '''
    #Primary Key
    #Foreign Keys
    ExperimentID = models.ForeignKey(Experiments)
    ProteinID = models.ForeignKey(Proteins)
    #Data    
    GeneName                = models.CharField(max_length=45)
    HitNumber               = models.IntegerField(null=True)
    FamilyMember            = models.CharField(max_length=45,null=True)
    Score                   = models.IntegerField(null=True)
    Mass                    = models.IntegerField(null=True)
    NormalizedMatches       = models.FloatField(null=True)   #Report normalized version of mass As a fraction of the total in a complete excitement
                                                    #This is done as Mass/Mass of all protiens in expirement
    Matches                 = models.IntegerField(null=True)
    MatchesSignificance     = models.IntegerField(null=True) #do we weigh the matches in the same way?
    Sequences               = models.IntegerField(null=True)
    SequencesSignigicance   = models.IntegerField(null=True)
    Coverage                = models.FloatField(null=True)
    validated               = models.BooleanField(default=True)
    
    
    def __unicode__(self):
        return str(self.id) + ": " + str(self.HitNumber) + " " + str(self.GeneName)
    

class Artical(models.Model):
    #Primary Key
    ##Uses Default auto-Increment
    #Foreign Keys
    #Data    
    Title   = models.CharField(max_length=255)
    Artical = models.TextField()
    
    def __unicode__(self):
        return str(self.Title) + ' ' + str(self.Artical) 



'''
class Template(models.Model):
    
    #This is the template
   
    #Primary Key
    #Foreign Keys
    #Data    
'''