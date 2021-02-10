
import xml.etree.ElementTree as ET 

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
  
  

      
def main(): 
    parseXML('COVIDSearchResults.xml') 
  
    
      
      
if __name__ == "__main__": 
  
    # calling main function 
    main() 