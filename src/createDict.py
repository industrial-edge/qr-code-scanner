import json

# Return tag name / tag id dictionary 
def getDict(metadata, connection_name):

    # Create dict
    nameIDMap = {}
    # Create Json Object
    json_metadata = json.loads(metadata)

    # Parse JSON object and create tag name / tag id dictionary 
    connections = json_metadata['connections']
    for element in connections:
        datapointobjects = element['dataPoints']

        if (element['name']==connection_name):

            for element in datapointobjects:
                definitions = element['dataPointDefinitions']
            
                for element in definitions:
                    nameIDMap.update({element['name'] : element['id']})
    
    #return dictionary
    return(nameIDMap)