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
        if end.year > 2021: pass # I did this because there are some ridiculuous numbers like 2100
        elif end.year not in end_year_dict: end_year_dict[end.year] = 1
        else: end_year_dict[end.year] += 1
        
        #update anytime_dict
        duration = end.year - startdate.year + 1
        for i in range(duration):
            yr = startdate.year + i
            if yr > 2021: continue # I did this because there are some ridiculuous numbers like 2100
            elif yr not in anytime_dict: anytime_dict[yr] = 1
            else: anytime_dict[yr] += 1
    
    start_year_dict = sorted(start_year_dict.items(), key=lambda x: x[0])
    anytime_dict = sorted(anytime_dict.items(), key=lambda x: x[0])
    end_year_dict = sorted(end_year_dict.items(), key=lambda x: x[0])

    return start_year_dict, anytime_dict, end_year_dict

def getAllPartB(data):
    """Get Part B"""
    mostStudiedDrugsDict = getMostStudiedDrugs(data)
    mostAdverseEvents = getAdverseEvents(data)
    start, anytime, end = getTrends(data)

    """Print Part B"""
    print("Most Studied Drugs and their frequencies: ", mostStudiedDrugsDict, "\n")
    print("Most Serious Adverse Events that occurred: ", mostAdverseEvents, "\n")
    print("Number of trials started at each year: ", start, "\n")
    print("Number of trials ongoing at any year: ", anytime, "\n")
    print("Number of trials ended at each year: ", end, "\n")
    
    """ Messy but it works. Bar graphs and Box charts """
    if True:
        """ Start """
        """ Bar Graph """
        fig = plt.figure()
        plt.bar(range(len(start)), [val[1] for val in start], align='center')
        plt.xticks(range(len(start)), [val[0] for val in start], rotation='vertical')
        fig.suptitle('Start year bar graph')
        plt.xlabel('year')
        plt.ylabel('frequency')
        plt.show()
        """ Box Chart """
        # not sure if we need this
        fig = plt.figure()
        x = [val[0] for val in start]
        plt.boxplot(x)
        fig.suptitle('Start year box chart')
        plt.xlabel('frequency')
        plt.ylabel('year')
        plt.show()
        
        """ Study at any time of the year"""
        """ Bar Graph """
        fig = plt.figure()
        plt.bar(range(len(anytime)), [val[1] for val in anytime], align='center')
        plt.xticks(range(len(anytime)), [val[0] for val in anytime], rotation='vertical')
        fig.suptitle('Study at any time of the year bar graph')
        plt.xlabel('year')
        plt.ylabel('frequency')
        plt.show()
        """ Box Chart """
        # not sure if we need this
        fig = plt.figure()
        x = [val[0] for val in anytime]
        plt.boxplot(x)
        fig.suptitle('anytime year box chart')
        plt.xlabel('frequency')
        plt.ylabel('year')
        plt.show()

        """ End """
        """ Bar Graph """
        fig = plt.figure()
        plt.bar(range(len(end)), [val[1] for val in end], align='center')
        plt.xticks(range(len(end)), [val[0] for val in end], rotation='vertical')
        fig.suptitle('End year bar graph')
        plt.xlabel('year')
        plt.ylabel('frequency')
        plt.show()
        """ Box Chart """
        # not sure if we need this
        fig = plt.figure()
        x = [val[0] for val in end]
        plt.boxplot(x)
        fig.suptitle('End year box chart')
        plt.xlabel('frequency')
        plt.ylabel('year')
        plt.show()
