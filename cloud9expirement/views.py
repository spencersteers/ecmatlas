# -*- coding: utf-8 -*-
import os
import re
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.core import serializers
from django.core.mail import send_mail, BadHeaderError
from django.views.generic.edit import UpdateView

from django.db.models import Q
from ecmatlas.models import Experiments, Proteins, ProteinHits, VariableModifications, Artical, Document
#from ecmatlas.models import *
from django.db import models
from django.shortcuts import render
import operator
from operator import __or__ as OR
import csv
from itertools import chain
from ecmatlas.GeneCategory import GeneCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ecmatlas.models import Document
from cloud9expirement.forms import DocumentForm

import django.core.exceptions
import csvextractor
import ecmatlas.models
from cloud9expirement.forms import EmailForm

#from django.views.generic import TemplateView
def validate(request):
    try:
        if not request.user.is_authenticated():
            return redirect('/admin/')
        if Experiments.objects.filter(validated=False): 
            return redirect('/validate.ExperimentsUpdate/')
        if VariableModifications.objects.filter(validated=False):
            return redirect('/validate.VariableModificationsUpdate/')
        if Proteins.objects.filter(validated=False):
            return redirect('/validate.ProteinsUpdate/')
        if ProteinHits.objects.filter(validated=False):
            return redirect('/validate.VariableModifications/')
        return redirect('/datainput.html')
    except:
        return redirect('/datainput.html')
        
class ExperimentsUpdate(UpdateView):
    model = ecmatlas.models.Experiments
    success_url = "/validate/"
    template_name_suffix = '_update_form'

    def get_object(self):
        
        obj = Experiments.objects.filter(validated=False)
        if not obj : raise Exception('None to fix')
        return obj[0]

        pass

class ProteinsUpdate(UpdateView):
    model = ecmatlas.models.Proteins
    success_url = "/validate/"
    template_name_suffix = '_update_form'

    def get_object(self):
        
        try: 
            obj = Proteins.objects.filter(validated=False)
            if not obj : raise Exception('None to fix')
            return obj[0]
        except ecmatlas.models.Proteins.DoesNotExist:
            pass
        pass


class ProteinHitsUpdate(UpdateView):
    model = ecmatlas.models.ProteinHits
    success_url = "/validate/"
    template_name_suffix = '_update_form'

    def get_object(self):
        
        try: 
            obj = ProteinHits.objects.filter(validated=False)
            if not obj : raise Exception('None to fix')
            return obj[0]
        except ecmatlas.models.ProteinHits.DoesNotExist:
            pass
        pass
        

class ArticalUpdate(UpdateView):
    model = ecmatlas.models.Artical
    pass

class VariableModificationsUpdate(UpdateView):
    model = ecmatlas.models.VariableModifications
    success_url = "/validate/"
    template_name_suffix = '_update_form'


    def get_object(self):
        
        try: 
            obj = VariableModifications.objects.filter(validated=False)
            if not obj : raise Exception('None to fix')
            return obj[0]
        except ecmatlas.models.VariableModifications.DoesNotExist:
            pass
        pass
        
def methods(request):

    t = get_template("freehtml5buildings/methods.html")

    c = {}
    c.update(csrf(request))

    html = t.render(Context(c))

    return HttpResponse(html)
    
def links(request):

    t = get_template("freehtml5buildings/links.html")

    c = {}
    c.update(csrf(request))

    html = t.render(Context(c))

    return HttpResponse(html)

def index(request):

    t = get_template("freehtml5buildings/index.html")

    c = {}
    c.update(csrf(request))

    html = t.render(Context(c))

    return HttpResponse(html)
    
def projects(request):

    t = get_template("freehtml5buildings/projects.html")

    html = t.render(Context({}))

    return HttpResponse(html)

def introduction(request):

    t = get_template("freehtml5buildings/introduction.html")

    form_data = {}

    form_data['Species'] = request.POST.getlist('Species')[0]

    c = {}
    c.update(csrf(request))

    c['form_data'] = form_data

    html = t.render(Context(c))

    return HttpResponse(html)

def introduction2(request):

    t = get_template("freehtml5buildings/introduction2.html")

    form_data = {}

    form_data['Species'] = request.POST.getlist('Species')[0]

    c = {}
    c.update(csrf(request))

    c['form_data'] = form_data

    html = t.render(Context(c))

    return HttpResponse(html)    

def introduction3(request):

    t = get_template("freehtml5buildings/introduction3.html")

    form_data = {}

    form_data['Species'] = request.POST.getlist('Species')[0]

    c = {}
    c.update(csrf(request))

    c['form_data'] = form_data

    html = t.render(Context(c))

    return HttpResponse(html)    

def ecmproteins(request):

    t = get_template("freehtml5buildings/ecmproteins.html")

    form_data = {}

    form_data['Species'] = request.POST.getlist('Species')[0]
    form_data['Tissues'] = request.POST.getlist('Tissues')
    form_data['ExperimentType'] = request.POST.getlist('ExperimentType')

    c = {}
    c.update(csrf(request))

    c['form_data'] = form_data

    html = t.render(Context(c))

    return HttpResponse(html)
    
def experiment_type(request):

    t = get_template("freehtml5buildings/experiment_type.html")

    form_data = {}

    form_data['Species'] = request.POST.getlist('Species')[0]
    form_data['Tissues'] = request.POST.getlist('Tissues')

    c = {}
    c.update(csrf(request))

    c['form_data'] = form_data

    html = t.render(Context(c))

    return HttpResponse(html)
    
def tissues(request):

    t = get_template("freehtml5buildings/tissues.html")

    form_data = {}

    form_data['Species'] = request.POST.getlist('Species')[0]

    c = {}
    c.update(csrf(request))

    c['form_data'] = form_data

    html = t.render(Context(c))

    return HttpResponse(html)

def readout_and_output(request):

    t = get_template("freehtml5buildings/readout_and_output.html");

    form_data = {};

    form_data['Species'] = request.POST.getlist('Species')[0]
    form_data['Tissues'] = request.POST.getlist('Tissues')
    form_data['ExperimentType'] = request.POST.getlist('ExperimentType')
    form_data['GeneType'] = request.POST.getlist('GeneType')

    c = {}
    c.update(csrf(request))

    c['form_data'] = form_data

    html = t.render(Context(c))

    return HttpResponse(html)

def search(request):
    return search_result(request)

# Search feature

def advanceSearch(request):
    a = GeneCategory()
    b = a.categories()
    c = {'b': b}
    c.update(csrf(request))
    return render_to_response("freehtml5buildings/advanceSearch.html", c, context_instance=RequestContext(request))

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query
    
def stats(request):
    #tempQuery = None
    #tempQuery = Experiments.objects.filter(Species = 'Homo Sapiens')
    #numberOfHomoSapienDataSets = tempQuery.count()
    numberOfHomoSapienDataSets = len(Experiments.objects.filter(Species = 'Homo Sapiens'))
    numberOfRattusDataSets = len(Experiments.objects.filter(Species = 'Rattus'))
    numberOfMusMusDataSets = len(Experiments.objects.filter(Species = 'Mus Mus'))
    numberOfBovineDataSets = len(Experiments.objects.filter(Species = 'Bovine'))
    numberOfOtherPrimatesDataSets = len(Experiments.objects.filter(Species__contains="Other Primates"))
    
    numberOfBloodDataSets = len(Experiments.objects.filter(Tissue = 'Blood'))
    numberOfBoneDataSets = len(Experiments.objects.filter(Tissue = 'Bone'))
    numberOfBrainDataSets = len(Experiments.objects.filter(Tissue = 'Brain'))
    numberOfBrownFatDataSets = len(Experiments.objects.filter(Tissue = 'Brown Fat'))
    numberOfEyeDataSets = len(Experiments.objects.filter(Tissue = 'Eye'))
    numberOfHeartDataSets = len(Experiments.objects.filter(Tissue = 'Heart'))
    numberOfKidneyDataSets = len(Experiments.objects.filter(Tissue = "Kidney"))
    numberOfLiverDataSets = len(Experiments.objects.filter(Tissue = 'Liver'))
    numberOfLowerGIDataSets = len(Experiments.objects.filter(Tissue = 'Lower GI'))
    numberOfLungDataSets = len(Experiments.objects.filter(Tissue = 'Lung'))
    numberOfLymphDataSets = len(Experiments.objects.filter(Tissue = 'Lymph'))
    numberOfMammaryGlandDataSets = len(Experiments.objects.filter(Tissue = 'Mammary Gland'))
    numberOfOvaryDataSets = len(Experiments.objects.filter(Tissue = 'Ovary'))
    numberOfPancreasDataSets = len(Experiments.objects.filter(Tissue = 'Pancreas'))
    numberOfProstateDataSets = len(Experiments.objects.filter(Tissue = 'Prostate'))
    numberOfSkeletalMuscleDataSets = len(Experiments.objects.filter(Tissue = 'Skeletal Muscle'))
    numberOfSpleenDataSets = len(Experiments.objects.filter(Tissue = 'Spleen'))
    numberOfStomachDataSets = len(Experiments.objects.filter(Tissue = 'Stomach'))
    numberOfTendonDataSets = len(Experiments.objects.filter(Tissue = 'Tendon'))
    numberOfTestisDataSets = len(Experiments.objects.filter(Tissue = 'Testis'))
    numberOfThyroidDataSets = len(Experiments.objects.filter(Tissue = 'Thyroid'))
    numberOfUrineDataSets = len(Experiments.objects.filter(Tissue = 'Urine'))
    numberOfUterusDataSets = len(Experiments.objects.filter(Tissue = 'Uterus'))
    numberOfWhiteFatDataSets = len(Experiments.objects.filter(Tissue = 'White Fat'))
    
    # return number of Genetypes
    GeneList = []
    GNCategory = GeneCategory()
    GeneList.extend(GNCategory.genesymbol('COL Mod'))
    numberOfColModDataSets = len(ProteinHits.objects.filter(GeneName__in = GeneList))
    
    GeneList = []
    GeneList.extend(GNCategory.genesymbol('Collagens'))
    numberOfCollagensDataSets = len(ProteinHits.objects.filter(GeneName__in = GeneList))
    
    GeneList = []
    GeneList.extend(GNCategory.genesymbol('ECM Glycoproteins'))
    numberOfECMGlycoproteinsDataSets = len(ProteinHits.objects.filter(GeneName__in = GeneList))
    
    GeneList = []
    GeneList.extend(GNCategory.genesymbol('ECM Regulators'))
    numberOfECMRegulatorsDataSets = len(ProteinHits.objects.filter(GeneName__in = GeneList))
    
    GeneList = []
    GeneList.extend(GNCategory.genesymbol('ECM-affiliated Proteins'))
    numberOfECMAffiliatedProteinsDataSets = len(ProteinHits.objects.filter(GeneName__in = GeneList))
    
    GeneList = []
    GeneList.extend(GNCategory.genesymbol('Major Contaminants'))
    numberOfMajorContaminantsDataSets = len(ProteinHits.objects.filter(GeneName__in = GeneList))
    
    GeneList = []
    GeneList.extend(GNCategory.genesymbol('Proteoglycans'))
    numberOfProteoglycansDataSets = len(ProteinHits.objects.filter(GeneName__in = GeneList))
    
    GeneList = []
    GeneList.extend(GNCategory.genesymbol('Secreted Factors'))
    numberOfSecretedFactorsDataSets = len(ProteinHits.objects.filter(GeneName__in = GeneList))
    
    return render(request, 'freehtml5buildings/stats.html', {'numberOfHomoSapienDataSets': numberOfHomoSapienDataSets, 
    'numberOfRattusDataSets': numberOfRattusDataSets,
    'numberOfMusMusDataSets': numberOfMusMusDataSets, 
    'numberOfBovineDataSets': numberOfBovineDataSets,
    'numberOfOtherPrimatesDataSets':numberOfOtherPrimatesDataSets,
    'numberOfBloodDataSets' : numberOfBloodDataSets, 
    'numberOfBoneDataSets': numberOfBoneDataSets, 
    'numberOfBrainDataSets': numberOfBrainDataSets,
    'numberOfBrownFatDataSets': numberOfBrownFatDataSets,
    'numberOfEyeDataSets': numberOfEyeDataSets, 
    'numberOfHeartDataSets': numberOfHeartDataSets, 
    'numberOfKidneyDataSets': numberOfKidneyDataSets, 
    'numberOfLiverDataSets': numberOfLiverDataSets,
    'numberOfLowerGIDataSets': numberOfLowerGIDataSets,
    'numberOfLungDataSets': numberOfLungDataSets,
    'numberOfLymphDataSets':numberOfLymphDataSets,
    'numberOfMammaryGlandDataSets': numberOfMammaryGlandDataSets,
    'numberOfOvaryDataSets': numberOfOvaryDataSets,
    'numberOfPancreasDataSets': numberOfPancreasDataSets,
    'numberOfProstateDataSets':numberOfProstateDataSets,
    'numberOfSkeletalMuscleDataSets':numberOfSkeletalMuscleDataSets,
    'numberOfSpleenDataSets':numberOfSpleenDataSets,
    'numberOfStomachDataSets':numberOfStomachDataSets,
    'numberOfTendonDataSets':numberOfTendonDataSets,
    'numberOfTestisDataSets':numberOfTestisDataSets,
    'numberOfThyroidDataSets':numberOfThyroidDataSets,
    'numberOfUrineDataSets':numberOfUrineDataSets,
    'numberOfUterusDataSets':numberOfUterusDataSets,
    'numberOfWhiteFatDataSets':numberOfWhiteFatDataSets,
    'numberOfColModDataSets':numberOfColModDataSets,
    'numberOfCollagensDataSets':numberOfCollagensDataSets,
    'numberOfECMGlycoproteinsDataSets':numberOfECMGlycoproteinsDataSets,
    'numberOfECMRegulatorsDataSets':numberOfECMRegulatorsDataSets,
    'numberOfECMAffiliatedProteinsDataSets':numberOfECMAffiliatedProteinsDataSets,
    'numberOfMajorContaminantsDataSets':numberOfMajorContaminantsDataSets,
    'numberOfProteoglycansDataSets':numberOfProteoglycansDataSets, 
    'numberOfSecretedFactorsDataSets':numberOfSecretedFactorsDataSets})

def results(request):
    
    # Setting queries to none in case these are not found.
    query_string = ''
    found_entries = None
    found_experiments = None
    found_pro_hits = None
    temp = None
    GeneList = []
       
    if (request.method == 'POST'):
        # Get the lists of selected items coming from the advance search website
        SpeciesList = request.POST.getlist('Species')
        TypeList = request.POST.getlist('Type')
        TissueList = request.POST.getlist('Tissues')
        ExtractionList = request.POST.getlist('ExtractionMethod')
        ExptTypeList = request.POST.getlist('ExperimentType')
        GeneTypeList = request.POST.getlist('GeneType')
        found_experiments = Experiments.objects.filter(Species__in = SpeciesList)
        
        ''' Check to see which catergories for experiment have been chosen '''    
        if SpeciesList:
            found_experiments = Experiments.objects.filter(Species__in = SpeciesList)
            if TypeList:
                found_expeiments = found_experiments.filter(TissueType__in = TypeList)
            if TissueList:
                found_experiments = found_experiments.filter(Tissue__in = TissueList)
            if ExtractionList:
                found_experiments = found_experiments.filter(ExtractionMethod__in = ExtractionList)
            if ExptTypeList:
                found_experiments = found_experiments.filter(ExpirementType__in = ExptTypeList)
        elif TypeList:
            found_experiments = Experiments.objects.filter(TissueType__in = TypeList)
            if TissueList:
                found_experiments = found_experiments.filter(Tissue__in = TissueList)
            if ExtractionList:
                found_experiments = found_experiments.filter(ExtractionMethod__in = ExtractionList)
            if ExptTypeList:
                found_experiments = found_experiments.filter(ExpirementType__in = ExptTypeList)
        elif TissueList:
            found_experiments = Experiments.objects.filter(Tissue__in = TissueList)
            if ExtractionList:
                found_experiments = found_experiments.filter(ExtractionMethod__in = ExtractionList)
            if ExptTypeList:
                found_experiments = found_experiments.filter(ExpirementType__in = ExptTypeList)
        elif ExtractionList:
            found_experiments = Experiments.objects.filter(ExtractionMethod__in = ExtractionList)
            if ExptTypeList:
                found_experiments = found_experiments.filter(ExpirementType__in = ExptTypeList)
        elif ExptTypeList:
            found_experiments = Experiments.objects.filter(ExpirementType__in = ExptTypeList)

        ''' Link Experiments with Protein Hits '''
        if found_experiments:
            found_pro_hits = ProteinHits.objects.filter(ExperimentID__in = found_experiments).select_related('ExperimentID')
            
        # Produce a protein hits queryset with or without experiment selection 
        if ('q' in request.POST) and request.POST['q'].strip():
            if found_pro_hits:
                query_string = request.POST['q']
                entry_query = get_query(query_string, ['GeneName',])
                found_pro_hits = found_pro_hits.filter(entry_query).select_related('ExperimentID')
            else:
                query_string = request.POST['q']
                entry_query = get_query(query_string, ['GeneName',])
                found_pro_hits = ProteinHits.objects.filter(entry_query).select_related('ExperimentID')
        
        # Generate a list of gene types and produce queryset based on this gene type list
        if GeneTypeList:
            temp = GeneCategory()
            for x in GeneTypeList:
                GeneList.extend(temp.genesymbol(x))
                
            if found_pro_hits:
                found_pro_hits = found_pro_hits.filter(GeneName__in = GeneList).select_related('ExperimentID')
            else:
                found_pro_hits = ProteinHits.objects.filter(GeneName__in = GeneList).select_related('ExperimentID')
        
        # Updating the experiments found according to protein hits found
        if found_pro_hits:
            if found_experiments:
                found_experiments = found_experiments.filter(reduce(lambda x, y: x | y, [Q(id__contains = word.ExperimentID.id) for word in found_pro_hits]))
            else:
                found_experiments = Experiments.objects.filter(reduce(lambda x, y: x | y, [Q(id = word.ExperimentID.id) for word in found_pro_hits]))
        else:
            found_experiments = None
           
    # Saves the found queries for later use in the program
    request.session['export_experiments'] = found_experiments
    request.session['export_pro_hits'] = found_pro_hits
    
    return render(request, 'freehtml5buildings/results.html', {'found_experiments': found_experiments, 'found_pro_hits': found_pro_hits})

def csv_download(request, experiments, proteins_hits, usr_choice):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="results.csv"'

    writer = csv.writer(response)
    
    header = []
    for exp in experiments:
        header.append(str(exp.SearchTitle))
    
    writer.writerow(['Gene Name'] + [exp for exp in header])
    
    proteins = set([x for x in Proteins.objects.all() for y in proteins_hits if x == y.ProteinID])
    
    NumList = []
    GeneNameStr = ""
    for prot in proteins:
        GeneNameStr = str(prot)
        tempQ = proteins_hits.filter(ProteinID = prot).distinct()
        for exp in experiments:
            found = False
            for t in tempQ:
                if exp == t.ExperimentID:
                    if usr_choice == "NormalizeID":
                        NumList.append(str(t.NormalizedMatches))
                    else:
                        NumList.append(str(t.Matches))
                    found = True
                    break
                else:
                    found = False
            if found == False:
                NumList.append((str(0)))
        writer.writerow([GeneNameStr] + [num for num in NumList])
        GeneNameStr = ""
        NumList = []
    return response

def results2(request):
    experiments = request.session['export_experiments']
    proteins_hits = request.session['export_pro_hits']
    #proteins set created below to save processing
    
    if experiments == None or proteins_hits == None:
        return render(request, 'freehtml5buildings/results2.html')    
    
    if (request.method == 'POST'):
        output_choice = request.POST['choice']
        usr_choice = request.POST['choice2']
        IDList = request.POST.getlist('Selection')
        
        if IDList:
            if IDList[0] != "All":
                #experiments = Experiments.objects.filter(reduce(lambda x, y: x | y, [Q(id__contains=word) for word in IDList]))
                experiments = Experiments.objects.filter(id__in = IDList)
                #proteins_hits = ProteinHits.objects.filter(ExperimentID__in = experiments)
                #experiments = experiments.filter(reduce(lambda x, y: x | y, [Q(id__contains=word) for word in IDList]))
                proteins_hits = proteins_hits.filter(ExperimentID__in = experiments)
                
        if experiments.count() > 3:
            output_choice = 'CSV'

    if output_choice == 'CSV':
        return csv_download(request, experiments, proteins_hits, usr_choice)
    else:
        proteins = set([x for x in Proteins.objects.all() for y in proteins_hits if x == y.ProteinID])
        NormID = []
        for prot in proteins:
            temp1 = []
            temp1.append(str(prot.LongGeneName))
            tempQ = proteins_hits.filter(ProteinID = prot).distinct()
            for exp in experiments:
                found = False
                for t in tempQ:
                    if exp == t.ExperimentID:
                        if usr_choice == "NormalizeID":
                            temp1.append("{0:.5f}".format(t.NormalizedMatches))
                        else:
                            temp1.append("{0:.5f}".format(t.Matches))
                        found = True
                        break
                    else:
                        found = False
                if found == False:
                    temp1.append(0)
            NormID.append(temp1)
        return render(request, 'freehtml5buildings/results2.html', {'experiments': experiments, 'proteins_hits': proteins_hits, 'proteins': proteins, 'NormID': NormID})
#--------------------------------------------------------------------------------------------------------------------------

def experiment(request, experiment_id):
    experiment = None
    found_pro_hits = None
    experiment = Experiments.objects.get(pk=experiment_id)
    found_pro_hits = ProteinHits.objects.filter(ExperimentID=experiment)
    return render(request, 'freehtml5buildings/experiment.html', {'experiment':experiment, 'found_pro_hits': found_pro_hits})

def protein(request, protein_id):
    protein = None
    found_exp = None
    protein = ProteinHits.objects.get(pk=protein_id)
    found_exp = Experiments.objects.filter(proteinhits__ExperimentID = protein.ExperimentID)
#    print(found_exp.)
    return render(request, 'freehtml5buildings/protein.html', {'found_exp':found_exp})

def contact(request):

    if request.method == 'POST':
        # A POST request: Handle Form Upload
        form = EmailForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            contactInputTextEmailSubject = form.cleaned_data['contactInputTextEmailSubject']
            contactEmailMessage = form.cleaned_data['contactEmailMessage']
            
            '''if not contactInputTextEmailSubject:
                raise ValidationError("You must enter a subject!")
            if not contactEmailMessage:
                raise ValidationError("You must enter a message!")'''

            #send email
            send_mail(contactInputTextEmailSubject, contactEmailMessage, 'theflooddevteam@gmail.com', ['anthony.nicolosi78i@gmail.com'], fail_silently=False)
 
            return render_to_response("freehtml5buildings/contact.html", context_instance=RequestContext(request))

    return render(request, 'freehtml5buildings/contact.html')

    
def datainput(request):
    #check logged in
    if not request.user.is_authenticated():
        return redirect('/admin/')
    t = get_template("freehtml5buildings/dataInput.html")
    DATA = "Please select an option"
    html = t.render(Context({'pageData' : DATA}))
    return HttpResponse(html)
    



def list(request):
    #check logged in
    if not request.user.is_authenticated():
        return redirect('/admin/')
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        os.path.join(os.path.dirname(__file__), 'templates/list.html').replace('\\','/'),
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
    
def expunge(request):
    #check logged in
    if not request.user.is_authenticated():
        return redirect('/admin/')
        
    path = os.path.join(os.path.dirname(__file__), 'media').replace('\\','/')
    docpath = "".join(request.path)[8:]
    fullpath = path + docpath
    foundDocument = Document.objects.filter(docfile=docpath[1:])
    if foundDocument: 
        foundDocument[0].delete()
        os.unlink(fullpath)
        return HttpResponseRedirect(reverse('list'))    
    else: 
        t = get_template("freehtml5buildings/dataInput.html")
        DATA = "document not found " + docpath
        html = t.render(Context({'pageData' : DATA}))
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('list'))    


def parseDocument(request):
    #check logged in
    if not request.user.is_authenticated():
        return redirect('/admin/' % request.path)
    path = "".join(request.path)
    DATA = csvextractor.go(path)
    
    t = get_template("freehtml5buildings/dataInput.html")
    html = t.render(Context({'pageData' : DATA}))
    return HttpResponse(html)
    
def fourOhFour(request):
    return HttpResponse("404! Page cannot be found.")
    
def search_result(request):
    query_string = ''
    found_entries = None

    if (request.method == 'POST'):
        selected_choice = request.POST['choice']
        print(selected_choice)
        if selected_choice == 'Experiment':
            print("Hello")
            '''
    if ('q' in request.GET) and request.GET['q'].strip():
            
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['GeneName',])
        found_entries = Proteins.objects.filter(entry_query)
    '''    
    return render(request, 'freehtml5buildings/search.html', {'found_entries': found_entries , 'query_string': query_string})
    