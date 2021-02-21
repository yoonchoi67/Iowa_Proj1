import xml.etree.ElementTree as ET 
import json
import datetime
from dateutil.parser import parse

def getStudyDuration(data):
    """get study duration of the studies
    Args: data: dict
    Returns: duration_dict: dict
    """
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
    return duration_dict

def getStudyResults(data):
    """get study results
    Args: data: dict
    Returns: type_dict: dict 
    """
    type_dict = {}
    for study in data['search_results']['study']:
        if not study['study_results'] in type_dict:
            type_dict[study['study_results']] = 1
        else:
            type_dict[study['study_results']] += 1
    return type_dict

def getAgeGroups(data):
    """get age group of the studies
    Args: data: dict
    Returns: age_group: dict
    """
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
    """get min max age of the studies
    Args: data: dict
    Returns: min_age_group, max_age_group: dict
    """
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
    """get gender of the studies
    Args: data: dict
    Returns: gender_dict: dict
    """
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
    """get study type of the studies
    Args: data: dict
    Returns: study_type_dict: dict
    """
    study_type_dict = {}
    for study in data['search_results']['study']:
        if not study['study_types'] in study_type_dict:
            study_type_dict[study['study_types']] = 1
        else:
            study_type_dict[study['study_types']] += 1
    return study_type_dict

def getInterventionStatus(data):
    """get intervention status of the studies
    Args: data: dict
    Returns: intervention_dict, num_intervention_dict: dict
    """
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
            
            # if str(type(study['interventions']['intervention']))=="<type 'dict'>":
            if type(study['interventions']['intervention']) is dict:
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
    """get activity status of the studies
    Args: data: dict
    Returns: status_dict: dict
    """
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
    """get study design of the studies
    Args: data: dict
    Returns: status_dict: dict
    """
    study_dict = {}
    type_dict = {}
    study_list = []
    for study in data['search_results']['study']:
        dictionary = {}
        # if str(type(study['study_designs'])) == "<type 'NoneType'>":
        if type(study['study_designs']) is type(None):
            if not "None" in study_dict:
                 study_dict["None"] = 1
            else:
                study_dict["None"] += 1
        else:
            # if str(type(study['study_designs']['study_design'])) == "<type 'unicode'>":
            if type(study['study_designs']['study_design']) is str:
                
                l = study['study_designs']['study_design'].split(':')
                dictionary[l[0]] = l[1]
                study_list.append(dictionary)
            else:
                for x in study['study_designs']['study_design']:
                    
                    l = x.split(':')
                    dictionary[l[0]] = l[1]
                    study_list.append(dictionary)

                #print(l)
        #print(study['@rank'])
        #print(dictionary)
    primary_purpose_dict = {}
    intervention_model_dict = {}
    allocation_dict = {}
    masking_dict = {}
    study_design_types = {}
    time_perspective_dict = {}
    observational_model_dict = {}
    for x in study_list:
        if 'Primary Purpose' in x:
            var = x['Primary Purpose'].encode('utf-8')
            if not var in primary_purpose_dict:
                primary_purpose_dict[var] = 1
            else:
                primary_purpose_dict[var]+=1
        if 'Intervention Model' in x:
            var = x['Intervention Model'].encode('utf-8')
            if not var in intervention_model_dict:
                intervention_model_dict[var] = 1
            else:
                intervention_model_dict[var]+=1
        if 'Allocation' in x:
            var = x['Allocation'].encode('utf-8')
            if not var in allocation_dict:
                allocation_dict[var] = 1
            else:
                allocation_dict[var]+=1
        if 'Masking' in x:
            var = x['Masking'].encode('utf-8')
            if not var in masking_dict:
                masking_dict[var] = 1
            else:
                masking_dict[var]+=1
        if 'Time Perspective' in x:
            var = x['Time Perspective'].encode('utf-8')
            if not var in time_perspective_dict:
                time_perspective_dict[var] = 1
            else:
                time_perspective_dict[var]+=1
        if 'Observational Model' in x:
            var = x['Observational Model'].encode('utf-8')
            if not var in observational_model_dict:
                observational_model_dict[var] = 1
            else:
                observational_model_dict[var]+=1
    print(" a. primary_purpose_dict: ", primary_purpose_dict)
    print(" b. intervention_model_dict: ", intervention_model_dict)
    print(" c. allocation_dict: ", allocation_dict)
    print(" d. masking_dict: ", masking_dict)
    print(" e. time_perspective_dict: ", time_perspective_dict)
    print(" f. observational_model_dict: ", observational_model_dict)
             
def getPhaseData(data):
    """get phase data of the studies
    Args: data: dict
    Returns: phases_dictionary: dict
    """
    phases_dictionary = {}
    countNone = 0;
    countMulti = 0
    countSingle = 0;
    
    # do analysis on each study through json format
    for study in data['search_results']['study']:
        
        if type(study['phases']) is type(None):
            # countNone+=1
            if not "None" in phases_dictionary:
                phases_dictionary["None"] = 1
            else:
                phases_dictionary["None"] += 1

        else:
            for phase in study['phases']:
                #print(type(study['phases'][phase]))
                # if str(type(study['phases'][phase]))=="<type 'unicode'>":
                if type(study['phases'][phase]) is str:
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

def getLocationCount(data):
    """get location data of the studies
    Args: data: dict
    Returns: total_loc, total_study: int
             type_dict: dict
    """
    type_dict = {}
    total_loc = 0
    total_study = 0
    for study in data['search_results']['study']:
        total_study += 1
        # if str(type(study['locations'])) == "<type 'NoneType'>":
        if type(study['locations']) is type(None):
            if not 'None' in type_dict:
                type_dict[0] = 1
            else:
                type_dict[0] += 1
        else:
            if 'location' in study['locations']:
                # if str(type(study['locations']['location'])) == "<type 'unicode'>":
                if type(study['locations']['location']) is str:
                    total_loc+=1
                    #print(study['locations']['location'].encode('utf-8'))
                    if not 1 in type_dict:
                        type_dict[1] = 1
                    else:
                        type_dict[1] += 1
                else:
                    count = 0
                    for x in study['locations']['location']:
                        count+=1
                    total_loc+=count
                    if not count in type_dict:
                        type_dict[count] = 1
                    else:
                        type_dict[count] += 1

    return total_loc, total_study, type_dict

def getEnrollmentCount(data):
    """get enrollment data of the studies
    Args: data: dict
    Returns: enrollmentCount, studyCount: int
    """
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
    return enrollmentCount, studyCount

def getGenderData(data):
    """get gender data of the studies
    Args: data: dict
    Returns: gender_dictionary: dict
    """
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
    """get result availability data of the studies
    Args: data: dict
    Returns: resultAvailability_dictionary: dict
    """
    resultAvailability_dictionary = {}
    for i, study in enumerate(data['search_results']['study']):
        result=study['study_results']
        if not result in resultAvailability_dictionary:
            resultAvailability_dictionary[result]=1
        else:
            resultAvailability_dictionary[result]+=1

    return resultAvailability_dictionary

def getAllPartA(data):
    """Get Part A"""
    #get various data we want
    phase_dict = getPhaseData(data)
    status_dict = getActivityStatus(data)
    intervention_dict, num_intervention = getInterventionStatus(data)
    study_type = getStudyType(data)
    gender_dict = getGenderData(data)
    #get age eligibility data
    hasResult_dict = getResultAvailabilityData(data)
    age_group = getAgeGroups(data)
    min_age, max_age = getMinMaxAge(data)
    study_duration=getStudyDuration(data)
    enrollmentCount, studyCount = getEnrollmentCount(data)
    total_loc, total_study, type_dict = getLocationCount(data)    

    """Print Part A"""
    print("1. Phases and their frequencies: ", phase_dict, "\n")
    print("2. Trial statuses and their frequencies: ", status_dict, "\n")
    print("3. Trial intervention methods and their frequencies: ", intervention_dict, "\n")
    print("4. Number of interventions per trial and their frequencies: ", num_intervention, "\n")
    print("5. Study type and their frequency: ", study_type, "\n")
    print("6. Genders and their frequency: ", gender_dict, "\n")
    print("7. Age groups/frequencies: ", age_group, "\n")
    print("8. Min Age: ", min_age, "\n")
    print("9. max age: ", max_age, "\n")
    print("10. Study results and their frequency: ", hasResult_dict, "\n")
    print("11. Study duration in months: ", study_duration, "\n")
    #IN PROGRESS FUNCTIONS:
    print("12. Enrollment counts: ", enrollmentCount, "\n")
    print("13. Study counts: ", studyCount, "\n")
    print("14. Total location counts: ", total_loc, "\n")
    print("15. Total study counts: ", total_study, "\n")
    print("16. Location per study counts: ", type_dict, "\n")
    print("17. study design data: ")
    studyDesignData(data)
