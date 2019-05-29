import json_operations
from collections import OrderedDict

def open_lock():
    f = open("lock.txt","w+")
    f.write("Unlocked")

def lock_lock():
    f = open("lock.txt","w+")
    f.write("Locked")

def check_lock_status():
    f = open("lock.txt","r")
    return f.readline()

def lock_logic():
    # unlock for homeowner
    door = json_operations.readFromJSONFile('whos_at_door')

    who = list(door.keys())[0]

    if door[who] == 'homeowner':
        open_lock()