import xml.etree.ElementTree as ET 
import json
import datetime
from dateutil.parser import parse
import matplotlib.pyplot as plt

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

def getTrends(data):
    """get study duration of the studies
    Args: data: dict
    Returns: duration_dict: dict
    """
    start_year_dict = {}
    end_year_dict = {}
    anytime_dict = {}

    duration_dict = {}
    
    for study in data['search_results']['study']:
        startdate = ''
        end = ''
        if not 'completion_date' in study:
            if 'primary_completion_date' in study:
                end = parse(study['primary_completion_date'])
            elif 'last_update_posted' in study:
                end = parse(study['last_update_posted'])
        else:
            end = parse(study['completion_date'])
        
        if not 'start_date' in study:
            if 'study_first_posted' in study:
                startdate = parse(study['study_first_posted'])
        else:
            startdate = parse(study['start_date'])

        #update start_year_dict
        if startdate.year not in start_year_dict: start_year_dict[startdate.year] = 1
        else: start_year_dict[startdate.year] += 1
        
        #update end_year_dict
        if end.year not in end_year_dict: end_year_dict[end.year] = 1
        else: end_year_dict[end.year] += 1
        
        #update anytime_dict
        duration = end.year - startdate.year + 1
        for i in range(duration):
            yr = startdate.year + i
            if yr not in anytime_dict: anytime_dict[yr] = 1
            else: anytime_dict[yr] += 1

    return start_year_dict, anytime_dict, end_year_dict

def getAllPartB(data):
    """Get Part B"""
    mostStudiedDrugsDict = getMostStudiedDrugs(data)
    mostAdverseEvents = getAdverseEvents(data)
    start, anytime, end = getTrends(data)

    """Print Part B"""
    # print("Most Studied Drugs and their frequencies: ", mostStudiedDrugsDict, "\n")
    # print("Most Serious Adverse Events that occurred: ", mostAdverseEvents, "\n")
    print("Number of trials started at each year: ", start, "\n")
    print("Number of trials ongoing at any year: ", anytime, "\n")
    print("Number of trials ended at each year: ", end, "\n")
    
    """ Show Bar Graph """
    fig = plt.figure()
    plt.bar(range(len(start)), list(start.values()), align='center')
    plt.xticks(range(len(start)), list(start.keys()))
    fig.suptitle('Start year')
    plt.xlabel('year')
    plt.ylabel('frequency')
    plt.show()

    """ Show Box Chart """
    # not sure if we need this
    x = [k for k, v in start.items()]
    plt.boxplot(x)
    plt.show()
