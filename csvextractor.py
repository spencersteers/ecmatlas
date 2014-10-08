from pprint import pprint
from datetime import datetime
import sys
import csv
import re
import os
import ecmatlas.models as models

DEBUG = True
ErrorLog = ""
ExperimentId = models.Experiments()

DateTime = re.compile(r"(?P<YYYY>\d{4})-(?P<MM>\d{2})-(?P<DD>\d{2})T(?P<hh>\d{2}):(?P<mm>\d{2}):(?P<ss>\d{2})Z")
Header = re.compile(r"(Header\s-+)\t*\n")
SearchTitle = re.compile(r"Search\stitle\t+(?P<SearchTitle>[\w| ]+)\t*")
Timestamp = re.compile(r"Timestamp\t+(?P<Timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\t*")
ExpirementType = re.compile(r"Expirement type\t+(?P<ExpirementType>[\d|.]+)\t*")																	
User = re.compile(r"User\t+(?P<User>[\w*| ]+)\t*")
Email = re.compile(r"Email\t+(?P<Email>[\w|@|.]+)\t*")
ReportUrl = re.compile(r"Report UR[I|L]\t+(?P<ReportUrl>[\w+|:|.|/|=|?|\-|\d|_]+)\t*")																	
PeakListDataPath = re.compile(r"Peak list data path\t+(?P<PeakListDataPath>[\w|:|\\|/|_|.]+)\t*")																	
PeakListFormat = re.compile(r"Peak list format\t+(?P<PeakListFormat>[\w| ]+)\t*")																	
SearchType = re.compile(r"Search type\t+(?P<SearchType>[\w| ]+)\t*")
MascotVersion = re.compile(r"Mascot version\t+(?P<MascotVersion>[\d|.]+)\t*")																	
Database = re.compile(r"Database\t+(?P<Database>[\w|:| ]+)\t*")
FastaFile = re.compile(r"Fasta file\t+(?P<FastaFile>[\w|:| |.]+)\t*")
TotalSequences = re.compile(r"Total sequences\t+(?P<TotalSequences>\d+)\t*")
TotalResidues = re.compile(r"Total residues\t+(?P<TotalResidues>\d+)\t*")
SequencesAfterTaxonomy = re.compile(r"Sequences after taxonomy filter\t+(?P<SequencesAfterTaxonomy>\w*)\t*")
NumberOfQueries = re.compile(r"Number of queries\t*(?P<NumberOfQueries>\d+)\t*")
Warning = re.compile(r"Warning\t+(?P<Warning>[\w| |.]+)\t*")
SearchParamaters = re.compile(r"Search Parameters\s*-*\t*\n")
TaxonomyFilter = re.compile(r"Taxonomy filter[.| |\t]+(?P<TaxonomyFilter>[\w| ]+)\t*")
Enzyme = re.compile(r"Enzyme\t+(?P<Enzyme>[\w| ]+)\t*")
MaximumMissedCleavages = re.compile(r"Maximum Missed Cleavages\t+(?P<MaximumMissedCleavages>[\d]+)\t*")
QuantitationMethod = re.compile(r"Quantitation method\t+(?P<QuantitationMethod>[\w| ]+)\t*")
PeptideMassTolerance = re.compile(r"Peptide Mass Tolerance\t+(?P<PeptideMassTolerance>[\d]+)\t*")
PeptideMassToleranceUnits = re.compile(r"Peptide Mass Tolerance Units\t+(?P<PeptideMassToleranceUnits>[\w| ]+)\t*")
FragmentMassTolerance = re.compile(r"Fragment Mass Tolerance\t+(?P<FragmentMassTolerance>[\d|\w| ]+)\t*")
FragmentMassToleranceUnits = re.compile(r"Fragment Mass Tolerance Units\t+(?P<FragmentMassToleranceUnits>[\w| ]+)\t*")
MassValues = re.compile(r"Mass values\t+(?P<MassValues>[\w| ]+)\t*")
InstrumentType = re.compile(r"Instrument type\t+(?P<InstrumentType>[\w| ]+)\t*")
IsotopeErrorMode = re.compile(r"Isotope error mode\t+(?P<IsotopeErrorMode>[\d]+)\t*")
FormatParameters = re.compile(r"Format parameters -*")	
SignificanceThreshold = re.compile(r"Significance threshold\t+(?P<SignificanceThreshold>[\d]+)\t*")
MaxNumberOfHits = re.compile(r"Max. number of hits\t+(?P<MaxNumberOfHits>[\d]+)\t*")
UseMudPITProteinScoring = re.compile(r"Use MudPIT protein scoring\t+(?P<UseMudPITProteinScoring>[\d]+)\t*")
IonsScoreCutoff = re.compile(r"Ions score cut-off\t+(?P<IonsScoreCutoff>[\d]+)\t*")
IncludeSamesetProteins = re.compile(r"Include same-set proteins\t+(?P<IncludeSamesetProteins>[\d]+)\t*")
IncludeSubsetProteins = re.compile(r"Include same-set proteins\t+(?P<IncludeSubsetProteins>[\d]+)\t*")
IncludeUnassigned = re.compile(r"Include unassigned\t+(?P<IncludeUnassigned>[\d]+)\t*")																	
RequireBoldRed = re.compile(r"Require bold red\t+(?P<RequireBoldRed>[\d]+)\t*")
UseHomologyThreshold = re.compile(r"Use homology threshold\t+(?P<UseHomologyThreshold>[\d]+)\t*")
GroupProteinFamilies = re.compile(r"Group protein families\t+(?P<GroupProteinFamilies>[\d]+)\t*")


ProteinHitsBreak = re.compile(r"Protein hits\s*-*")
protDescName = re.compile(r"(?P<Name>[\w|\(|\)| |-]+) ") 
protDescSpecies = re.compile(r"OS=(?P<Species>[\w| ]+) ")
protDescGeneName = re.compile(r"[GN|Gene_Symbol]+=(?P<GeneName>[\w|\d]+)") #Tax_Id=10090 Gene_Symbol=Myh6 Myosin-6
protLongDescGeneName = re.compile(r"[GN|Gene_Symbol]+=(?P<LongGeneName>[\w| |\d]+)") #Tax_Id=10090 Gene_Symbol=Myh6 Myosin-6

FixedModificationsBreak = re.compile(r"Fixed modifications[\s|\t|\n|-]+")
VariableModificationsBreak = re.compile(r"Variable modifications[\s|\t|\n|-]+")

def screenPrint(classObj):
    atters = vars(classObj)
    print classObj.__class__.__name__
    for item in atters.items():
        key,value = item
        for i in xrange(30 - len(key)): sys.stdout.write(".")
        print key, ":",value
    print
    pass
        

def fetchWithReg(recordline, regexp, name=''):
    global ErrorLog
    try:
        m =  regexp.search(recordline[0]+"\t"+recordline[1])
        if name and m != None:
            #for i in xrange(27 - len(name)): sys.stdout.write("-")
            #print name, ":",m.group(name)
            return m.group(name)
    except:
        ErrorLog =  ErrorLog + "There was an error with " +  name + ". \n"
        return None

def makeProt(oneProt):
    global ErrorLog
    tempProt = models.Proteins()
    tempProtHit = models.ProteinHits()
    #--print oneProt
    for elem in oneProt:
        m = protDescGeneName.search(elem)
        l = protLongDescGeneName.search(elem)
        if m != None and l != None: 
            tempProt.GeneName    = m.group("GeneName")
            tempProtHit.GeneName = m.group("GeneName")
            tempProt.LongGeneName    = l.group("LongGeneName")
            tempProtHit.LongGeneName = l.group("LongGeneName")
        m = protDescName.search(elem) 
        if m != None: 
            tempProt.Name        = m.group("Name")
        m = protDescSpecies.search(elem) 
        if m != None: 
            tempProt.Species     = m.group("Species")
    if tempProt.GeneName == None:
        ErrorLog += "Error!: Could not get GeneName for " + oneProt[0] +":"+ oneProt[1] +"\n"
        return None

    try:
        tempProtHit.HitNumber             = int(oneProt[0])
        tempProtHit.FamilyMember          = oneProt[1]
        tempProtHit.Score                 = int(oneProt[3])
        tempProtHit.Mass                  = int(oneProt[4])
        tempProtHit.NormalizedMatches     = tempProtHit.Matches
        tempProtHit.Matches               = int(oneProt[5])
        tempProtHit.MatchesSignificance   = int(oneProt[6])
        tempProtHit.Sequences             = int(oneProt[7])
        tempProtHit.SequencesSignigicance = int(oneProt[8])
        tempProtHit.Coverage              = float(oneProt[9])

        tempProt.HitNumber         = int(oneProt[0])
        tempProt.ProtAcc           = oneProt[1]
        tempProt.Length            = int(oneProt[10])

    except:
        ErrorLog += "Error!: On " + oneProt[0] +":"+ oneProt[1] +"\n"

    global ExperimentId
    
    
    alreadyExists = models.Proteins.objects.filter(LongGeneName=tempProt.LongGeneName)
    if alreadyExists:
        ErrorLog += "\nAlert: LongGeneName " + str(tempProt.LongGeneName) + " Already exists\n"
        tempProt = alreadyExists[0]
        ErrorLog += "\nAlert: LongGeneName " + str(tempProt) + " used.\n"

    tempProtHit.ExperimentID = ExperimentId
    tempProtHit.ProteinID    = tempProt

    alreadyExistsToo = models.ProteinHits.objects.filter(ExperimentID=tempProtHit.ExperimentID)
    alreadyExistsToo.filter(ProteinID = tempProtHit.ProteinID)
    
    if alreadyExistsToo:
        ErrorLog += "\nWarning!: This hit already exists for ExperimentID " + str(tempProtHit.ExperimentID.id) + " Already exists\n"
        tempProtHit = alreadyExistsToo[0]
        ErrorLog += "\nAlert: Prothit " + str(tempProtHit) + " used, Unclear if this is duplicate\n"

    return (tempProt, tempProtHit)


def makeVariableModifications(oneMod):
    global ErrorLog
    tempVarMod = models.VariableModifications()
    if len(oneMod) >= 4:
        tempVarMod.name = oneMod[1]
        tempVarMod.delta = oneMod[2]
        tempVarMod.neutralLosses = oneMod[3]
    if tempVarMod.name == None:
        ErrorLog += "Error!: Could not get modifiaton name for " + oneMod +"\n"
        return None

    return tempVarMod

def makeExperiment(dataTable):

    expirementData = models.Experiments()
    
    for row in dataTable:
        expirementData.SearchTitle = fetchWithReg(row, SearchTitle, name='SearchTitle') or expirementData.SearchTitle 
        expirementData.Timestamp = fetchWithReg(row, Timestamp, name='Timestamp') or expirementData.Timestamp  
        if expirementData.ExpirementType != None: expirementData.ExpirementType = fetchWithReg(row, ExpirementType, name = 'ExpirementType') or expirementData.ExpirementType
        expirementData.User = fetchWithReg(row, User, name='User') or expirementData.User  
        expirementData.Email = fetchWithReg(row, Email, name='Email') or expirementData.Email  
        expirementData.ReportURI = fetchWithReg(row, ReportUrl, name='ReportUrl') or expirementData.ReportURI  
        expirementData.PeakListDataPath = fetchWithReg(row, PeakListDataPath, name='PeakListDataPath') or expirementData.PeakListDataPath  
        expirementData.PeakListFormat = fetchWithReg(row, PeakListFormat, name='PeakListFormat') or expirementData.PeakListFormat  
        expirementData.SearchType = fetchWithReg(row, SearchType, name='SearchType') or expirementData.SearchType  
        expirementData.MascotVersion = fetchWithReg(row, MascotVersion, name='MascotVersion') or expirementData.MascotVersion  
        expirementData.Database = fetchWithReg(row, Database, name='Database') or expirementData.Database  
        expirementData.FastaFile = fetchWithReg(row, FastaFile, name='FastaFile') or expirementData.FastaFile  
        expirementData.TotalSequences = (fetchWithReg(row, TotalSequences, name='TotalSequences')) or expirementData.TotalSequences  
        if expirementData.TotalSequences != None: expirementData.TotalSequences = int(expirementData.TotalSequences)
        expirementData.TotalResidues = (fetchWithReg(row, TotalResidues, name='TotalResidues')) or expirementData.TotalResidues  
        if expirementData.TotalResidues != None: expirementData.TotalResidues = int(expirementData.TotalResidues)
        expirementData.SequencesAfterTaxonomyFilter = (fetchWithReg(row, SequencesAfterTaxonomy, name='SequencesAfterTaxonomy')) or expirementData.SequencesAfterTaxonomyFilter  
        if expirementData.SequencesAfterTaxonomyFilter != None: expirementData.SequencesAfterTaxonomyFilter = int(expirementData.SequencesAfterTaxonomyFilter)
        expirementData.NumberOfQueries = (fetchWithReg(row, NumberOfQueries, name='NumberOfQueries')) or expirementData.NumberOfQueries  
        if expirementData.NumberOfQueries != None: expirementData.NumberOfQueries = int(expirementData.NumberOfQueries)
        expirementData.Warning = fetchWithReg(row, Warning, name='Warning') or expirementData.Warning  
        expirementData.TaxonomyFilter = fetchWithReg(row, TaxonomyFilter, name='TaxonomyFilter') or expirementData.TaxonomyFilter  
        expirementData.Enzyme = fetchWithReg(row, Enzyme, name='Enzyme') or expirementData.Enzyme  
        expirementData.MaximumMissedCleavages = (fetchWithReg(row, MaximumMissedCleavages, name='MaximumMissedCleavages')) or expirementData.MaximumMissedCleavages  
        if expirementData.MaximumMissedCleavages != None: expirementData.MaximumMissedCleavages = int(expirementData.MaximumMissedCleavages)
        expirementData.PeptideMassTolerance = (fetchWithReg(row, PeptideMassTolerance, name='PeptideMassTolerance')) or expirementData.PeptideMassTolerance  
        if expirementData.PeptideMassTolerance != None: expirementData.PeptideMassTolerance = float(expirementData.PeptideMassTolerance )
        expirementData.PeptideMassToleranceUnits = fetchWithReg(row, PeptideMassToleranceUnits, name='PeptideMassToleranceUnits') or expirementData.PeptideMassToleranceUnits  
        expirementData.FragmentMassTolerance = (fetchWithReg(row, FragmentMassTolerance, name='FragmentMassTolerance')) or expirementData.FragmentMassTolerance  
        if expirementData.FragmentMassTolerance != None: expirementData.FragmentMassTolerance = float(expirementData.FragmentMassTolerance )
        expirementData.FragmentMassToleranceUnits = fetchWithReg(row, FragmentMassToleranceUnits, name='FragmentMassToleranceUnits') or expirementData.FragmentMassToleranceUnits  
        expirementData.MassValues = fetchWithReg(row, MassValues, name='MassValues') or expirementData.MassValues  
        expirementData.InstrumentType = fetchWithReg(row, InstrumentType, name='InstrumentType') or expirementData.InstrumentType  
        expirementData.IsotopeErrorMode = (fetchWithReg(row, IsotopeErrorMode, name='IsotopeErrorMode')) or expirementData.IsotopeErrorMode  
        if expirementData.IsotopeErrorMode != None: expirementData.IsotopeErrorMode = int(expirementData.IsotopeErrorMode)
        expirementData.SignificanceThreshold = (fetchWithReg(row, SignificanceThreshold, name='SignificanceThreshold')) or expirementData.SignificanceThreshold  
        if expirementData.SignificanceThreshold != None: expirementData.SignificanceThreshold = float(expirementData.SignificanceThreshold )
        expirementData.MaxNumberOfHits = ('1' == fetchWithReg(row, MaxNumberOfHits, name='MaxNumberOfHits')) or expirementData.MaxNumberOfHits  
        expirementData.UseMudPITProteinScoring = ('1' == fetchWithReg(row, UseMudPITProteinScoring, name='UseMudPITProteinScoring')) or expirementData.UseMudPITProteinScoring  
        expirementData.IonsScoreCutoff = ('1' == fetchWithReg(row, IonsScoreCutoff, name='IonsScoreCutoff')) or expirementData.IonsScoreCutoff  
        expirementData.IncludeSamesetProteins = ('1' == fetchWithReg(row, IncludeSamesetProteins, name='IncludeSamesetProteins')) or expirementData.IncludeSamesetProteins  
        expirementData.IncludeSubsetProteins = ('1' == fetchWithReg(row, IncludeSubsetProteins, name='IncludeSubsetProteins')) or expirementData.IncludeSubsetProteins  
        expirementData.IncludeUnassigned = ('1' == fetchWithReg(row, IncludeUnassigned, name='IncludeUnassigned')) or expirementData.IncludeUnassigned  
        expirementData.RequireBoldRed = ('1' == fetchWithReg(row, RequireBoldRed, name='RequireBoldRed')) or expirementData.RequireBoldRed  
        expirementData.UseHomologyThreshold = ('1' == fetchWithReg(row, UseHomologyThreshold, name='UseHomologyThreshold')) or expirementData.UseHomologyThreshold  
        expirementData.GroupProteinFamilies = ('1' == fetchWithReg(row, GroupProteinFamilies, name='GroupProteinFamilies')) or expirementData.GroupProteinFamilies  

    m =  DateTime.search(expirementData.Timestamp)                              
    expirementData.Timestamp = datetime(int(m.group('YYYY')), int(m.group("MM")), int(m.group("DD")), 
                                        int(m.group("hh")), int(m.group("mm")), int(m.group("ss")))   
    
    
    global ErrorLog
    global ExperimentId
    
    alreadyExists1 = models.Experiments.objects.filter(Timestamp=expirementData.Timestamp)
    if alreadyExists1:
        ErrorLog += "\tWarning!:: Expreiment with Timestamp " + str(expirementData.Timestamp) + " Already exists in Database\n"
        ErrorLog += ": Using " + str(alreadyExists1[0]) + " \n"
        expirementData = alreadyExists1[0]
        ExperimentId = expirementData
        return expirementData
    
    ExperimentId = expirementData
    return expirementData
    


def NormalizeTheMatches(ProtHits):
    global ErrorLog
    totalMatch = 0
    for prot in ProtHits:
        try: totalMatch = totalMatch + int(prot.Matches)
        except: ErrorLog = ErrorLog + "Could not convert Matches for " + prot.GeneName + "\n"
    for prot in ProtHits:
        try:
            prot.NormalizedMatches = float(int(prot.Matches))/float(totalMatch)
        except: 
            ErrorLog = ErrorLog + "Could not set NormalizedMatches for " + prot.GeneName + "\n"
    pass

ProtAcc                 = -1
Name                    = -1
Species                 = -1
Length                  = -1
IsoelectricPoint        = -1
TaxidermyString         = -1
TaxidermyID             = -1
Sequence                = -1
HitNumber               = -1
FamilyMember            = -1
Score                   = -1
Mass                    = -1
NormalizedMatches       = -1
Matches                 = -1
MatchesSignificance     = -1
Sequences               = -1
SequencesSignigicance   = -1
Coverage                = -1
def assignColumns(protRow):
    global ProtAcc, Name, Species, Length, IsoelectricPoint
    global TaxidermyString, TaxidermyID, Sequence, HitNumber, FamilyMember
    global Score, Mass, NormalizedMatches, Matches, MatchesSignificance
    global Sequences, SequencesSignigicance, Coverage 
    colStrings =   ["prot_hit_numa",
                    "prot_acc",
                    "prot_desc",	
                    "prot_score",	
                    "prot_mass",	
                    "prot_matches",	
                    "prot_matches_sig",	
                    "prot_sequences",	
                    "prot_sequences_sig",	
                    "prot_cover",	
                    "prot_len"]
    ProtAcc                 = -1
    Name                    = -1
    Species                 = -1
    Length                  = -1
    IsoelectricPoint        = -1
    TaxidermyString         = -1
    TaxidermyID             = -1
    Sequence                = -1
    HitNumber               = -1
    FamilyMember            = -1
    Score                   = -1
    Mass                    = -1
    NormalizedMatches       = -1
    Matches                 = -1
    MatchesSignificance     = -1
    Sequences               = -1
    SequencesSignigicance   = -1
    Coverage                = -1
    

def main(path='NoPath'):
    if path == 'NoPath': return "No path was given"
    debugString = ""
    resultsProt = []
    resultsProtHit = []
    resultsExperiment = []
    resultsMod = []

    filepath = os.path.join(os.path.dirname(__file__), 'cloud9expirement/media' + path).replace('\\','/')

    with open(filepath, 'rb') as csvfile:
        filereader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        hitProts = False
        modification = False
        modification_count = 0 
        for row in filereader:
            if "".join(row) == "": 
                modification_count += 1
                continue
            if modification_count >= 2: modification = False
            if row[0] == "prot_hit_num": continue
            if FixedModificationsBreak.search("".join(row)) != None: 
                modification = True
                modification_count = 0
                continue
            if VariableModificationsBreak.search("".join(row)) != None:
                modification = True
                modification_count = 0
                continue
            if hitProts:
                Prot, ProtHit = makeProt(row)
                resultsProt.append(Prot)
                resultsProtHit.append(ProtHit)
            if modification:
                if row[0] == "Identifier": continue
                x = makeVariableModifications(row)
                resultsMod.append(x)
            else:
                if ProteinHitsBreak.search("".join(row)) != None:  
                    hitProts = True
                    continue
                resultsExperiment.append([row[0],row[1]])

    resultsExperiment = makeExperiment(resultsExperiment)
    resultsExperiment.save()

    print resultsMod
    for varMod in resultsMod : 
        varMod.ExperimentID = ExperimentId
        varMod.save()
    
    NormalizeTheMatches(resultsProtHit)
    global ErrorLog
    for i in xrange(len(resultsProt)): 
        protDB, protHitDb = (resultsProt[i],resultsProtHit[i])
        protHitDb.ExperimentID = resultsExperiment
        ErrorLog += "\t</br>about to save protien : " + str(protDB)
        protDB.save()
        protHitDb.ProteinID = protDB
        ErrorLog += "</br>and this protien is tied to hit : " + str(protHitDb)
        protHitDb.save()
        ErrorLog += str(protDB) + " and " + str(protHitDb) + " were saved.</br>"
        ErrorLog += str(protHitDb.ExperimentID) + ":" + str(protHitDb.ProteinID)\
                  + " for ProteinHit ID pair.</br>"
        ErrorLog += "\t</br>"



    if DEBUG: return "File Parsing completed. (ALREADY EXISTS ERRORS MEAN THAT THE ITEM IS ALREADY IN THE DATABASE). ErrorLog: </br>" + ErrorLog
    return "File Parsing completed"
    
def go(path):
    global ErrorLog
    print "Parsing file at " + path
    returnString = main(path)
    return returnString


