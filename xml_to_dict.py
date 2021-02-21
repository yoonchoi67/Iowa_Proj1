import xmltodict, json, os
import formatDrugNames

#preliminary parsing
#================================================================================#

# create an outfile.json (HepA Results) output file if not exists
if not os.path.exists('data/outfile.json'):
    open('data/outfile.json', 'w').close()

# convert SearchResults.xml to outfile.json if it hadn't been done before
if os.stat("data/outfile.json").st_size == 0:
    with open('data/SearchResults.xml', 'r', encoding='utf-8') as myfile:
        with open('data/outfile.json', 'w', encoding='utf-8') as outfile:
            obj = xmltodict.parse(myfile.read())
            json.dump(obj, outfile, indent=4, sort_keys=True)

# json load
f=open('data/outfile.json')
data=json.load(f)

# create an COVIDoutfile.json (COVID Results) output file if not exists
if not os.path.exists('data/COVIDoutfile.json'):
    open('data/COVIDoutfile.json', 'w').close()

# convert SearchResults.xml to outfile.json if it hadn't been done before
if os.stat("data/COVIDoutfile.json").st_size == 0:
    with open('data/COVIDSearchResults.xml', 'r', encoding='utf-8') as myfile:
        with open('data/COVIDoutfile.json', 'w', encoding='utf-8') as outfile:
            obj = xmltodict.parse(myfile.read())
            json.dump(obj, outfile, indent=4, sort_keys=True)

# json load
f=open('data/COVIDoutfile.json')
data=json.load(f)

#================================================================================#