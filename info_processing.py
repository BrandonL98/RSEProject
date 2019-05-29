import json_operations
from collections import OrderedDict

def process_camera_detection(data):
    # data passed in is in format:
    # {"name": prob} about who's at the door
    
    prev_record = json_operations.readFromJSONFile('people_count')

    for key,val in prev_record.items():
        if (key == "unknown"):
            if (prev_record[key] > 0.25):
                prev_record[key] = val - 0.25
        else:
            if (prev_record[key] > 0.1):
                prev_record[key] = val - 0.1

    for key,val in data.items():
        found = False
        for key2,val2 in prev_record.items():
            if (key == key2):
                prev_record[key2] = val + val2
                found = True
        if(found == False):
            prev_record[key] = val
    
    json_operations.writeToJSONFile('people_count', prev_record)

    new_list = sort_data_by_value(prev_record)
    new_record = process_data(new_list)

    json_operations.writeToJSONFile('whos_at_door', new_record)

def sort_data_by_value(data):
    values = []
    for key in data:
        values.append(data[key])

    values.sort(reverse = True)

    people = []
    for value in values:
        for key,val in data.items():
            if (val == value):
                people.append(key)
                data[key] = -1

    return people

def process_data(people):
    # given the name of people
    # create a dictionary with key = name and val = homeowner/visitor/stranger

    d = OrderedDict()

    for individual in people:

        added = False

        f = open("homeowners.txt", "r")

        if individual == 'unknown':
            d[individual] = "stranger"
            added = True

        for line in f:

            line = line.rstrip()

            if line == individual:

                d[individual] = "homeowner"
                added = True
                continue

        if added == False:

            d[individual] = "visitor"
    
    return d


