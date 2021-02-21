import xml.etree.ElementTree as ET 
import json
import datetime
from dateutil.parser import parse

def getMostStudiedDrugs(data):
    """get 15 most studied drugs that appeared in trials for each disease
    Args: data: dict
    Returns: mostStudiedDrugsDict: dict 
    """
    mostStudiedDrugsDict = {}
    
    for study in data['search_results']['study']:
        try:
            # no drug was used, so we skip
            if type(study['interventions']) is type(None):
                continue
            # only one type of intervention
            elif type(study['interventions']['intervention']) is dict:
                if study['interventions']['intervention']['@type'] is "Drug" or "Biological":
                    if each['#text'] not in mostStudiedDrugsDict:
                        mostStudiedDrugsDict[each['#text']]=1
                    else:
                        mostStudiedDrugsDict[each['#text']]+=1
            # two or more interventions
            else:
                for each in study['interventions']['intervention']:
                    # print(each['@type'])
                    if each['@type'] is "Drug" or "Biological":
                        if each['#text'] not in mostStudiedDrugsDict:
                            mostStudiedDrugsDict[each['#text']]=1
                        else:
                            mostStudiedDrugsDict[each['#text']]+=1
        except:
            break
    # sort by the frequencies
    mostStudiedDrugsDict = sorted(mostStudiedDrugsDict.items(), key=lambda x: x[1], reverse=True)
    
    # return 15 most studied drugs
    return mostStudiedDrugsDict[:15]

def getAdverseEvents(data):
    """get 10 most serious adverse events that occured in trials for each disease
    Args: data: dict
    Returns: mostAdverseEvents: dict 
    """
    mostAdverseEvents={}
    return mostAdverseEvents

def getAllPartB(data):
    """Get Part B"""
    mostStudiedDrugsDict = getMostStudiedDrugs(data)
    mostAdverseEvents = getAdverseEvents(data)

    """Print Part B"""
    print("Most Studied Drugs and their frequencies: ", mostStudiedDrugsDict, "\n")
    print("Most Serious Adverse Events that occurred: ", mostAdverseEvents)