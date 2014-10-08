import csv
import os


class GeneCategory:
    Categories = dict()
    def __init__(self, filename=''):
        if not filename: filename = os.path.join(os.path.dirname(__file__), 'Matrisome.txt').replace('\\','/')
        self.sourceFile = filename
        self.Categories = dict()
        with open(filename, 'rb') as csvfile:
            filereader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            for row in filereader:
                if "".join(row) == "": continue
                if row[0].upper() == "CATEGORY": continue
                if row[0] not in self.Categories: 
                    self.Categories[row[0]] = [row[1]]
                else :
                    self.Categories[row[0]].append(row[1])
                
    def categories(self): return sorted(self.Categories) #Sorted only returns keys!! .keys()
    def genesymbol(self, catagory): return self.Categories[catagory]
    
    def __unicode__(self): return str(self.Categories)