import xml.etree.ElementTree as ET 
import json
import datetime
from dateutil.parser import parse
import partA, partB, partC

def parseXML(xmlfile): 
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    tag = root.tag
    phases_dictionary = {}
    study_counter = 0;
    for elem in root.iter():
        
        if elem.tag == 'study':
            study_counter+=1
            print(elem.attrib)
        if elem.tag == 'phases':
            counter = 0;
            for child in elem:
                print(child.text)
                counter = counter + 1
            if not study_counter in phases_dictionary:
                phases_dictionary[study_counter] = counter
        
    print(phases_dictionary)


def parseJSON(jsonfile):
    """Do Json stuff"""
    f=open(jsonfile)
    data=json.load(f)

    """filter out the studies we want to look at"""
    data_list = filterResults(data)
    data['search_results']['study'] = data_list

    """Part A"""
    # comment this in or out if you want to print part A results
    # partA.getAllPartA(data)
    
    """Part B"""
    # comment this in or out if you want to print part B results
    # partB.getAllPartB(data)

    """Part C"""
    # comment this in or out if you want to print part C results
    partC.getAllPartC(data)

"""Initial"""
def filterResults(data):
    """filter those that do not meet criteria, such as it not having what it is testing.
       this reduces the number of hepA studies to 71, and covid studies to 1536.
    Args: data: dict
    Returns: data_dict: dict
    """
    data_dict = []
    search = data['search_results']['query'].encode('utf-8')
    for study in data['search_results']['study']:
        if not 'conditions'  in study:
            print("NOT IN STUDY")
        # elif str(type(study['conditions'])) == "<type 'NoneType'>":
        elif type(study['conditions']) is type(None):
            continue
            # print("NULL")
        else:
            # if str(type(study['conditions']['condition'])) == "<type 'unicode'>":
            if type(study['conditions']['condition']) is str:
                if search in study['conditions']['condition'].encode('utf-8'):
                    data_dict.append(study)
                    #print("MATCH" + " " + study['@rank'])
            else:
                for cond in study['conditions']['condition']:
                    if search in cond.encode('utf-8'):
                        data_dict.append(study)
                        
                        #print("MATCH"+ " " + study['@rank'])
    return data_dict

            
    
def main():
    print("HEPATITIS A:")
    parseJSON('data/outfile.json')
    print("\n\n")
    print("COVID-19:")
    parseJSON('data/COVIDoutfile.json')
    
      
      
if __name__ == "__main__": 
  
    # calling main function 
    main() 

"""
other_ids
age_groups
interventions
exp_acc_types
locations
completion_date
nct_id
outcome_measures
phases
documents
study_first_posted
title
primary_completion_date
conditions
start_date
study_types
status
study_designs
acronym
sponsors
@rank
funded_bys
min_age
last_update_posted
study_results
url
gender
enrollment
"""
