import xmltodict, json, os
import formatDrugNames

#preliminary parsing
#================================================================================#

# create an outfile.json output file if not exists
if not os.path.exists('outfile.json'):
    open('outfile.json', 'w').close()

# convert SearchResults.xml to outfile.json if it hadn't been done before
if os.stat("outfile.json").st_size == 0:
    with open('SearchResults.xml', 'r', encoding='utf-8') as myfile:
        with open('outfile.json', 'w', encoding='utf-8') as outfile:
            obj = xmltodict.parse(myfile.read())
            json.dump(obj, outfile, indent=4, sort_keys=True)

# json load
f=open('outfile.json')
data=json.load(f)

#================================================================================#


#analysis
#================================================================================#

store_results = dict()

# do analysis on each study through json format
for each in data['search_results']['study'][:4]:
    # format drug names here
    for inv in each['interventions']['intervention']:
        changed = formatDrugNames.formatDrugName(inv['#text'])
        print(changed)
    # put into final dict, store_results
    store_results[each['@rank']]=each

print("=================")

for each in store_results.items():
    print(each)
    print("\n")

#================================================================================#