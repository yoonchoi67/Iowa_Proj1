import xml.etree.ElementTree as ET 
import json
import datetime
import urllib.request

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
                if study['interventions']['intervention']['@type'] == "Drug" or \
                   study['interventions']['intervention']['@type'] == "Biological":
                    if each['#text'] not in mostStudiedDrugsDict:
                        mostStudiedDrugsDict[each['#text']]=1
                    else:
                        mostStudiedDrugsDict[each['#text']]+=1
            # two or more interventions
            else:
                for each in study['interventions']['intervention']:
                    # print(each['@type'])
                    if each['@type'] == "Drug" or ['@type'] == "Biological":
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

def studyHasResults(study):
    return study["study_results"] != "No Results Available"

def retrieveStudyData(nct_id):
    base = "https://clinicaltrials.gov/api/query/full_studies?expr={}&fmt=json".format(nct_id)
    with urllib.request.urlopen(base) as response:
        jsonData = json.loads(response.read())
    fullData = jsonData["FullStudiesResponse"]["FullStudies"][0]["Study"]
    return fullData

def extractAdverseEventsFields(studyData):
    adverseEvents = {"Deaths":0,"NumSeriousEvents":0,
                     "NumVulnerable":0,"SeriousEvents":{}}
    if 'ResultsSection' not in studyData or 'AdverseEventsModule' not in studyData['ResultsSection']:
        return adverseEvents
    baseData = studyData['ResultsSection']['AdverseEventsModule']
    adverseGroupData = baseData["EventGroupList"]["EventGroup"]
    for group in adverseGroupData:
        adverseEvents["Deaths"] += int(group["EventGroupDeathsNumAffected"]) if "EventGroupDeathsNumAffected" in group else 0
        adverseEvents["NumVulnerable"] += int(group["EventGroupSeriousNumAtRisk"]) if "EventGroupSeriousNumAtRisk" in group else 0
        adverseEvents["NumSeriousEvents"] += int(group["EventGroupSeriousNumAffected"]) if "EventGroupSeriousNumAffected" in group else 0
    if adverseEvents["NumSeriousEvents"] != 0:
        seriousEventsData = baseData["SeriousEventList"]["SeriousEvent"]
        for event in seriousEventsData:
            #Note: total affected added over all events will be less than numSeriousEvents,
            #because this splitting means some patients will be double listed
            names = [n.strip() for n in event["SeriousEventTerm"]\
                     .lower()\
                     .replace('pneumonia viral','pneumonia')\
                     .replace('acute respiratory distress','respiratory distress')\
                     .replace('acute respiratory failure','respiratory failure')\
                     .replace('syndrome','')\
                     .split(";")]
            for name in names:
                adverseEvents["SeriousEvents"][name] = {}
                adverseEvents["SeriousEvents"][name]["OrganSystem"] = event["SeriousEventOrganSystem"]
                adverseEvents["SeriousEvents"][name]["NumAffected"] = 0
                for group_affected in event["SeriousEventStatsList"]["SeriousEventStats"]:
                    adverseEvents["SeriousEvents"][name]["NumAffected"] += int(group_affected["SeriousEventStatsNumAffected"])
    return adverseEvents
    
def getAdverseEvents(data):
    """get 10 most serious adverse events that occured in trials for each disease
    Args: data: dict
    Returns: mostAdverseEvents: dict 
    """
    #first, get the events by trial
    seriousEventsByTrial = {}
    seriousEventsByName = {}
    #This will just count the number of events
    #(NOT number affected, will count different
    #things affecting one person's organ system as one event)
    seriousEventsByOrganSystem = {}
    for study in data['search_results']['study']:
        if studyHasResults(study):
            nct_id = study["nct_id"]
            studyData = retrieveStudyData(nct_id)
            seriousEventsByTrial[nct_id] = extractAdverseEventsFields(studyData)
        else:
            continue
    #now, arrange by event name
    for trialName in seriousEventsByTrial.keys():
        trialData = seriousEventsByTrial[trialName]
        if trialData['NumSeriousEvents'] == 0:
            continue
        else:
            for eventName in trialData["SeriousEvents"].keys():
                eventData = trialData["SeriousEvents"][eventName]
                if eventName in seriousEventsByName:
                    seriousEventsByName[eventName]["NumAffected"] += eventData["NumAffected"]
                else:
                    seriousEventsByName[eventName] = eventData
    for eventName in seriousEventsByName.keys():
        eventData = seriousEventsByName[eventName]
        organSystem = eventData["OrganSystem"]
        if organSystem in seriousEventsByOrganSystem:
            seriousEventsByOrganSystem[organSystem]["NumberOfEvents"] += eventData["NumAffected"]
            #seriousEventsByOrganSystem[organSystem]["events"].add(eventName)
        else:
            seriousEventsByOrganSystem[organSystem] = {}
            seriousEventsByOrganSystem[organSystem]["NumberOfEvents"] = eventData["NumAffected"]
            #seriousEventsByOrganSystem[organSystem]["events"] = {eventName}
    #filter out top 10
    allEvents = list(seriousEventsByName.keys())
    sortCriteria = lambda name : seriousEventsByName[name]["NumAffected"]
    allEvents.sort(key = sortCriteria,reverse=True)
    topTenList = allEvents[0:10]
    topTenDict = {}
    for eventName in topTenList:
        topTenDict[eventName] = seriousEventsByName[eventName]
    #Give some summary stats
    print("Number of total participants: {}".format(sum([seriousEventsByTrial[n]["NumVulnerable"] for n in seriousEventsByTrial.keys()])))
    print("Number of total adverse events : {}".format(sum([seriousEventsByTrial[n]["NumSeriousEvents"] for n in seriousEventsByTrial.keys()])))
    print("Number participant deaths : {}".format(sum([seriousEventsByTrial[n]["Deaths"] for n in seriousEventsByTrial.keys()])))
    print("Number of studies with results : {}".format(len(list(seriousEventsByTrial.keys()))))
    print("Number of studies with results that reported at least one adverse event : {}".format(sum([seriousEventsByTrial[n]["NumSeriousEvents"]>0 for n in seriousEventsByTrial.keys()])))
    for k in seriousEventsByOrganSystem.keys():
          print("{}\t{}".format(k,seriousEventsByOrganSystem[k]["NumberOfEvents"]))
    return topTenDict

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
    if False:
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
