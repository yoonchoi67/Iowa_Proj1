import re
import json
import urllib.request
def getStandardName(term):
    term = term.replace(' ','%')
    term = term.replace('&','')
    base="https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term={}&option=1".format(term)
    with urllib.request.urlopen(base) as response:
        jsonData = json.loads(response.read())
    try:
        firstMatch = jsonData['approximateGroup']['candidate'][0]
    except:
        #was unable to find the term, proceed without further action
        return term
    getNameURL = "https://rxnav.nlm.nih.gov/REST/rxcui/{}.json".format(firstMatch['rxcui'])
    with urllib.request.urlopen(getNameURL) as response:
        nameData = json.loads(response.read())
    try:
        return nameData['idGroup']['name'].lower()
    except:
        print(term)
        print(base)
        print(firstMatch)
        print(nameData)
        soefijo

def removeDosing(singleDrug):
    #remove dose information
    
    units=["ml","mol","g","mg","%",]
    singleDrug = re.sub(r"""(high|medium|low|[1-4]|one|two|three|four)(\s)+dose(s)?""",'', singleDrug)
    singleDrug = re.sub(r"""([0-9]+)(\.)?(\s)?(ml|mol|g|mg|kg|%)(/(ml|mol|g|mg|kg|%))?""",'', singleDrug)
    singleDrug = re.sub(r"""group(\s)(([a-e+])|([0-5]+))""",'', singleDrug)
    singleDrug = re.sub(r"""\[.*\]""",'', singleDrug)
    singleDrug = re.sub(r"""\(.*\)""",'', singleDrug)
    #remove stop words and terms of type of delivery
    singleDrug = re.sub(r"""\sof\s""",'', singleDrug)
    singleDrug = re.sub(r"""injection""",'', singleDrug)
    singleDrug = re.sub(r"""\spill""",'', singleDrug)
    singleDrug = re.sub(r"""oral\s""",'', singleDrug)
    singleDrug = re.sub(r"""\soral""",'', singleDrug)
    singleDrug = re.sub(r"""((once|twice)\s)?daily""",'', singleDrug)
    return singleDrug
    
def formatDrugName(singleDrug):
    singleDrug = singleDrug.lower()
    #get rid of unicode
    singleDrug = singleDrug.encode("ascii","ignore").decode()
    #common subsitutions
    if "placebo" in singleDrug or "saline" in singleDrug:
        return "placebo"
    if "standard" in singleDrug or "usual" in singleDrug:
        return "standard care"
    if "hqc" in singleDrug:
        return 'hydroxychloroquine sulfate'
    if "plasma" in singleDrug:
        return "convalescent plasma"
    if "no intervention" in singleDrug or "none" in singleDrug or "n/a" in singleDrug:
        return "no intervention"
    singleDrug = removeDosing(singleDrug)
    singleDrug = singleDrug.strip()
    try:
        singleDrug = getStandardName(singleDrug)
    except:
        print("HTTP error!")
    return singleDrug
