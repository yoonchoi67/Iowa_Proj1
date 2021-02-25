import xml.etree.ElementTree as ET 
import json
import datetime
from dateutil.parser import parse

def getSponsors(data):
    """
    - get lead sponsoring and collaborating number for each sponsors_dict
    - get the number of collaborators for each studies to get mean, median, etc.
    Args: data: dict
    Returns: sponsors_dict, collaborators: dict
    """
    # { {sponsorName: {lead sponsor: int, collaborator: int} } }
    sponsors_dict = {}
    # { num_of_collaborator_in_study: int, num_of_collaborator_in_study: int, ...}
    collaborators = {}
    for study in data['search_results']['study']:
        try:
            # put the sponsors_dict dictionary into a variable
            temp_sponsor_dict = study['sponsors']
            # no sponsors_dict
            if type(temp_sponsor_dict['lead_sponsor']) is type(None):
                continue
            # one lead sponsor, no collaborator
            elif "collaborator" not in temp_sponsor_dict:
                print(temp_sponsor_dict['lead_sponsor'])
                print(type(temp_sponsor_dict['lead_sponsor']))      
                a=temp_sponsor_dict['lead_sponsor'].replace(" ", "")
                if temp_sponsor_dict['lead_sponsor'] not in sponsors_dict:
                    sponsors_dict[a]['lead_sponsor'] = 1
                else:
                    sponsors_dict[a]['lead_sponsor'] +=1
            # one lead sponsor, one collaborator 
            elif type(temp_sponsor_dict['collaborator']) is str:
                if study['collaborator'] not in sponsors_dict:
                    sponsors_dict[temp_sponsor_dict['lead_sponsor']]['collaborator'] = 1
                else:
                    sponsors_dict[temp_sponsor_dict['lead_sponsor']]['collaborator'] +=1
                # also put the number of collaborator (one) in collaborators dictionary
                if 1 not in collaborators:
                    collaborators[1] = 1
                else:
                    collaborators[1] +=1
            # one lead sponsor, multiple collaborators
            else:
                collaborator_len_of_the_study = len(temp_sponsor_dict['collaborator'])
                for each_collaborators in temp_sponsor_dict['collaborator']:
                    if each_collaborators not in sponsors_dict:
                        sponsors_dict[temp_sponsor_dict['lead_sponsor']]['collaborator'] = 1
                    else:
                        sponsors_dict[temp_sponsor_dict['lead_sponsor']]['collaborator'] +=1
                # also put the number of collaborator (one) in collaborators dictionary
                if collaborator_len_of_the_study not in collaborators:
                    collaborators[collaborator_len_of_the_study] = 1
                else:
                    collaborators[collaborator_len_of_the_study] +=1
        except Exception as e:
            print("BROKEN AT RANK: ", study['@rank'])
            print(e)
            break

    # sort by the frequencies
    sponsors_dict = sorted(sponsors_dict.items(), key=lambda x: x[1], reverse=True)
    collaborators = sorted(collaborators.items(), key=lambda x: x[1], reverse=True)
    
    # return sponsor
    return sponsors_dict, collaborators


def getAllPartC(data):
    """Get Part C"""
    sponsors_dict, collaborators = getSponsors(data)
    
    """Print Part C"""
    print("Sponsors: ", sponsors_dict, "\n")
    print("Collaborators: ", collaborators)