
import xml.etree.ElementTree as ET 
import json

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
    f=open(jsonfile)
    data=json.load(f)
    phase_dict = getPhaseData(data)
    status_dict = getActivityStatus(data)
    intervention_dict, num_intervention = getInterventionStatus(data)
    print(phase_dict)
    print(status_dict)
    print(intervention_dict)
    print(num_intervention)


def getInterventionStatus(data):
    intervention_dict = {}
    num_intervention_dict = {}
    type_dict = {}
    for study in data['search_results']['study']:
        if type(study['interventions']) is type(None):
            if not "None" in intervention_dict:
                intervention_dict["None"] = 1
                num_intervention_dict[0] = 1
            else:
                intervention_dict["None"] += 1
                num_intervention_dict[0] += 1
        else:
            
            if str(type(study['interventions']['intervention']))=="<type 'dict'>":
                if not 1 in num_intervention_dict:
                    num_intervention_dict[1] = 1
                else:
                    num_intervention_dict[1] += 1
                if not study['interventions']['intervention']["@type"] in intervention_dict:
                    intervention_dict[study['interventions']['intervention']["@type"]] = 1
                else:
                    intervention_dict[study['interventions']['intervention']["@type"]] += 1
            else:
                i = len(study['interventions']['intervention'])
                if not i in num_intervention_dict:
                    num_intervention_dict[i] = 1
                else:
                    num_intervention_dict[i] += 1
                for x in study['interventions']['intervention']:
                    if not x["@type"] in intervention_dict:
                        intervention_dict[x["@type"]] = 1
                    else:
                        intervention_dict[x["@type"]] += 1

 
    return intervention_dict, num_intervention_dict
    
def getActivityStatus(data):
    status_dict = {};
    for study in data['search_results']['study']:
        #print(type(study['status']))
        #print(study['status'])
        status = [];
        sep = ', '
        for key in study['status']:
            if study['status'][key] == 'N':
                status.append("Not Open")
            elif study['status'][key] == 'Y':
                status.append("Open")
            else:
                status.append(study['status'][key])
        p = sep.join(status)
        if not p in status_dict:
                status_dict[p] = 1
        else:
                status_dict[p] += 1
    return status_dict
    
def getPhaseData(data):
    phases_dictionary = {}
    countNone = 0;
    countMulti = 0
    countSingle = 0;
    
    # do analysis on each study through json format
    for study in data['search_results']['study']:
        
        if type(study['phases']) is type(None):
            countNone+=1
            if not "None" in phases_dictionary:
                phases_dictionary["None"] = countNone
            else:
                phases_dictionary["None"] += 1

        else:
            for phase in study['phases']:
                #print(type(study['phases'][phase]))
                if str(type(study['phases'][phase]))=="<type 'unicode'>":
                    countSingle+=1
                    p = study['phases'][phase]
                    if not p in phases_dictionary:
                        phases_dictionary[p] = 1
                    else:
                        phases_dictionary[p] += 1
                else:
                    countMulti+=1
                    sep = '/'
                    p = sep.join(study['phases'][phase])
                    if not p in phases_dictionary:
                        phases_dictionary[p] = 1
                    else:
                        phases_dictionary[p] += 1


                
                

    #print(countNone)
    #print(countMulti)
    #print(countSingle)
    #print(phases_dictionary)
    return phases_dictionary


      
def main():
    parseJSON('data/outfile.json')
    #parseXML('COVIDSearchResults.xml') 
  
    
      
      
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
