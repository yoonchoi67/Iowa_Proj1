import xml.etree.ElementTree as ET 
import json
import datetime
from dateutil.parser import parse

def getSponsors(data):
    """
    - get lead sponsoring and collaborating number for each lead_dict
    - get the number of collaborators for each studies to get mean, median, etc.
    Args: data: dict
    Returns: lead_dict, collaborators: dict
    """
    # dictionary that counts the entity and their frequency as a lead sponsor and a collaborator
    lead_dict = {}
    collab_dict = {}
    # frequency of collaborators per study
    collaborators = {}

    for study in data['search_results']['study']:
        try:
            """ get lead_sponsor and collaborator into variables """
            temp_sponsors = study['sponsors']
            temp_lead_sponsor = temp_sponsors['lead_sponsor']
            # try and except becaue there might be no collaborator field
            try: temp_collaborators = temp_sponsors['collaborator']
            except: temp_collaborators = None
            
            """ dictionary of sponsors and their frequency """
            # if the lead sponsor is not in the dictionary yet
            if temp_lead_sponsor not in lead_dict: lead_dict[temp_lead_sponsor] = 1
            # if the lead sponsor is already in the dictionary, increment the times it was a lead sponsors
            else: lead_dict[temp_lead_sponsor] +=1

            """ dictionary of collaborators and their frequency """
            # no collaborator
            if type(temp_collaborators) is type(None): continue

            # one collaborator 
            elif type(temp_collaborators) is str:
                # if the collaborator is not in the dictionary yet
                if temp_collaborators not in collab_dict: collab_dict[temp_collaborators] = 1
                # if the collaborator is already in the dictionary, increment the times it collaborated
                else: collab_dict[temp_collaborators] += 1

                # also put the number of collaborator (one) in collaborators dictionary
                if 1 not in collaborators: collaborators[1] = 1
                else: collaborators[1] += 1

            # multiple collaborators
            else:
                collab_len = len(temp_collaborators)
                for each in temp_collaborators:
                    if each not in collab_dict: collab_dict[each] = 1
                    else: collab_dict[each] += 1

                # also put the number of collaborator (one) in collaborators dictionary
                if collab_len not in collaborators: collaborators[collab_len] = 1
                else: collaborators[collab_len] += 1
                
        except Exception as e:
            print("BROKEN AT RANK: ", study['@rank'])
            break

    # sort by the frequencies
    lead_dict = sorted(lead_dict.items(), key=lambda x: x[1], reverse=True)
    collab_dict = sorted(collab_dict.items(), key=lambda x: x[1], reverse=True)
    
    # return sponsor
    return lead_dict, collab_dict, collaborators


def getOverlaps(hep_dict, covid_dict):
    """
    - get overlap between Hep A sponsors and COVID-19 sponsors
    Args: hep_data, covid_data: dict
    Returns: overlap_dict: dict
    """
    return


def getAllPartC(data):
    """Get Part C"""
    lead_dict, collab_dict, collaborators = getSponsors(data)
    
    """Print Part C"""
    print("- Number of sponsors: ", len(lead_dict))
    print("- Sponsors: ", lead_dict[:15])
    print("- Number of collaborators: ", len(collab_dict))
    print("- Collaborators: ", collab_dict[:15])
    
    print("- Collaborators per study and their frequencies: ", collaborators)
    