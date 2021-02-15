
import xml.etree.ElementTree as ET 
import json
from formatDrugNames import formatDrugName
import datetime
from dateutil.parser import parse

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
    data_list = filterResults(data)
    data['search_results']['study'] = data_list
    phase_dict = getPhaseData(data)
    status_dict = getActivityStatus(data)
    intervention_dict, num_intervention = getInterventionStatus(data)
    study_type = getStudyType(data)
    gender_dict = getGenderData(data)
    #get age eligibility data
    hasResult_dict = getResultAvailabilityData(data)
    print("Phases and their frequencies:")
    print(phase_dict)
    print("Trial statuses and their frequencies:")
    print(status_dict)
    print("Trial intervention methods and their freuqnecies:")
    print(intervention_dict)
    print("Number of interventions per trial and their frequencies")
    print(num_intervention)
    print("Study type and their frequency:")
    print(study_type)
    print("Genders and their frequency:")
    print(gender_dict)
    print("Study results and their frequency:")
    print(hasResult_dict)
    age_group = getAgeGroups(data)
    print("Age groups/frequencies: ")
    print(age_group)
    min_age, max_age = getMinMaxAge(data)
    print("Min Age: ")
    print(min_age)
    print("max age: ")
    print(max_age)
    print("Study duration in months:")
    getStudyDuration(data)
    
    #IN PROGRESS FUNCTIONS:
    print("Enrollment counts:")
    enrollmentCount(data)
    print("Location counts:")
    locationCount(data)
    print("study design data:")
    studyDesignData(data)


def filterResults(data):
    data_dict = []
    search = data['search_results']['query'].encode('utf-8')
    for study in data['search_results']['study']:
        if not 'conditions'  in study:
            print("NOT IN STUDY")
        elif str(type(study['conditions'])) == "<type 'NoneType'>":
            print("NULL")
        else:
            if str(type(study['conditions']['condition'])) == "<type 'unicode'>":
                if search in study['conditions']['condition'].encode('utf-8'):
                    data_dict.append(study)
                    #print("MATCH" + " " + study['@rank'])
            else:
                for cond in study['conditions']['condition']:
                    if search in cond.encode('utf-8'):
                        data_dict.append(study)
                        
                        #print("MATCH"+ " " + study['@rank'])
    return data_dict
        
def getStudyDuration(data):
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
            #print(study['completion_date'])
        
        if not 'start_date' in study:
            if 'study_first_posted' in study:
                startdate = parse(study['study_first_posted'])
        else:
            startdate = parse(study['start_date'])
        #print(str(end) + " - " + str(startdate))
        num_months = (end.year - startdate.year) * 12 + (end.month - startdate.month)
        if not num_months in duration_dict:
            duration_dict[num_months] = 1
        else:
            duration_dict[num_months] += 1

    print(duration_dict)
def getStudyResults(data):
    type_dict = {}
    for study in data['search_results']['study']:
        if not study['study_results'] in type_dict:
            type_dict[study['study_results']] = 1
        else:
            type_dict[study['study_results']] += 1
    print(type_dict)

def getAgeGroups(data):
    age_group = {}
    for study in data['search_results']['study']:
        if str(type(study['age_groups']['age_group']))=="<type 'unicode'>":
            p = study['age_groups']['age_group']
            if not p in age_group:
                age_group[p] = 1
            else:
                age_group[p] += 1
        else:
            sep = '/'
            p = sep.join(study['age_groups']['age_group'])
            if not p in age_group:
                age_group[p] = 1
            else:
                age_group[p] += 1
    return age_group

def getMinMaxAge(data):
    max_age_group = {}
    min_age_group = {}
    for study in data['search_results']['study']:
        if 'max_age' in study:
            if not study['max_age'] in max_age_group:
                max_age_group[study['max_age']] = 1
            else:
                max_age_group[study['max_age']] += 1
        if 'min_age' in study:
            if not study['min_age'] in min_age_group:
                min_age_group[study['min_age']] = 1
            else:
                min_age_group[study['min_age']] += 1
    return min_age_group, max_age_group

def getGender(data):
    gender_dict = {}
    for study in data['search_results']['study']:
        if 'gender' in study:
            if not study['gender'] in gender_dict:
                gender_dict[study['gender']] = 1
            else:
                gender_dict[study['gender']] += 1
        else:
            if not "Not Available" in gender_dict:
                gender_dict["Not Available"] = 1
            else:
                gender_dict["Not Available"] += 1
    return gender_dict

def getStudyType(data):
    study_type_dict = {}
    for study in data['search_results']['study']:
        if not study['study_types'] in study_type_dict:
            study_type_dict[study['study_types']] = 1
        else:
            study_type_dict[study['study_types']] += 1
    return study_type_dict

def getInterventionStatus(data):
    intervention_dict = {}
    num_intervention_dict = {}
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


def studyDesignData(data):
    study_dict = {};
    type_dict = {}
    for study in data['search_results']['study']:
        dictionary = {}
        if str(type(study['study_designs'])) == "<type 'NoneType'>":
            if not "None" in study_dict:
                 study_dict["None"] = 1
            else:
                study_dict["None"] += 1
        else:
            if str(type(study['study_designs']['study_design'])) == "<type 'unicode'>":
                print(study['study_designs']['study_design'])
            else:
                for x in study['study_designs']['study_design']:
                    l = x.split(':')
                    #dictionary[l[0]] = l[1]
                      
                #print(l)
       # print(dictionary)

            #print(study['study_designs']['study_design'])
    print(study_dict)
    print(type_dict)
             

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

    return phases_dictionary


def locationCount(data):
    type_dict = {}
    for study in data['search_results']['study']:
        if not type(study['locations']) in type_dict:
            type_dict[type(study['locations'])] = 1
        else:
            type_dict[type(study['locations'])] += 1

    print(type_dict)

def enrollmentCount(data):
    type_dict = {}
    enrollmentCount = 0
    studyCount = 0
    for study in data['search_results']['study']:
        studyCount+=1
        if 'enrollment' in study:
            x = 0
            if not study['enrollment'] in type_dict:
                x = int(study['enrollment'])
                enrollmentCount+=x
                type_dict[study['enrollment']] = 1
            else:
                x = int(study['enrollment'])
                enrollmentCount+=x
                type_dict[study['enrollment']] += 1
    print(enrollmentCount)
    print(studyCount)
    print(type_dict)

def getGenderData(data):
    gender_dictionary = {}
    for i, study in enumerate(data['search_results']['study']):
        # if gender for the study is available
        try:
            gdr=study['gender']
            if not gdr in gender_dictionary:
                gender_dictionary[gdr]=1
            else:
                gender_dictionary[gdr]+=1
        # no gender information available
        except:
            if not 'Not Available' in gender_dictionary:
                gender_dictionary['Not Available']=1
            else:
                gender_dictionary['Not Available']+=1
    return gender_dictionary



def getResultAvailabilityData(data):
    resultAvailability_dictionary = {}
    for i, study in enumerate(data['search_results']['study']):
        result=study['study_results']
        if not result in resultAvailability_dictionary:
            resultAvailability_dictionary[result]=1
        else:
            resultAvailability_dictionary[result]+=1

    return resultAvailability_dictionary

def getDrugDictionary(data):
    drug_dict = {}
    num_intervention_dict = {}
    for study in data['search_results']['study']:
        if type(study['interventions']) is type(None):
            if not "None" in drug_dict:
                drug_dict["None"] = 1
            else:
                drug_dict["None"] += 1
        else:
            
            if str(type(study['interventions']['intervention']))=="<type 'dict'>":
                print('hey this happened!')
                return
                if not 1 in num_intervention_dict:
                    num_intervention_dict[1] = 1
                else:
                    num_intervention_dict[1] += 1
                if not study['interventions']['intervention']["@type"] in drug_dict:
                    drug_dict[study['interventions']['intervention']["@type"]] = 1
                else:
                    drug_dict[study['interventions']['intervention']["@type"]] += 1
            else:
                i = len(study['interventions']['intervention'])
                if not i in num_intervention_dict:
                    num_intervention_dict[i] = 1
                else:
                    num_intervention_dict[i] += 1
                for x in study['interventions']['intervention']:
                    if type(x) is str:
                        continue
                    drug_name = formatDrugName(x['#text'])
                    if not drug_name in drug_dict:
                        drug_dict[drug_name] = 1
                    else:
                        drug_dict[drug_name] += 1


    return drug_dict
    
def main():
    print("HEPATITIS A:")
    parseJSON('data/outfile.json')
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
