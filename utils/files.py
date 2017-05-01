import os
import contextlib
import sys
import re
import json

def read_json(path, prefix=None):
    """
    Read a Json File a returns a dict
    It removes comments specified by # before parsing the file.
   
    If the json file has a field with a string "py:..."
    it assumes that it is a python statement and evaluates it
    Args: 
        path (str) In : path to the json file to load

    Returns:
        dict : dict with the json file in path contents

    """
    with open(path,'r') as f:
        filtered = re.sub(re.compile("#.*?\n" ) ,"" ,f.read())
   
    j_file = json.loads(filtered)
    if prefix!=None and 'name' in j_file:
        j_file['name'] = '%s%s'%(prefix,j_file['name'])
    
    #Some times the json might have python code for simplify legibility
    eval_json_python(j_file)
    return j_file

def eval_json_python(j_file):
    """
    Evaluates all the python statements in the json file str fields
    that starts by 'py:'

    Args :
       j_file (dict) InOut : json file contents
    """
    for key in j_file:
        # TODO Add strings in list support
        if type(j_file[key]) is dict:
             eval_json_python(j_file[key])
        elif (type(j_file[key]) is unicode) and (j_file[key][0:3]=='py:'):
             j_file[key] = eval(j_file[key][3:])

class cd:
    """
    Context manager for changing the current working directory
    as seen in https://stackoverflow.com/questions/431684/how-do-i-cd-in-python
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)
        self.newPath = os.path.expandvars(self.newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


