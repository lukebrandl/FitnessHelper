# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:51:49 2017

@author: brandl
"""

import logging

from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from Classes.py import Exercise, ExerciseInstance, Routine

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

########## Various possible states
DEFAULTSTATE=0
MODIFYINGROUTINE=1

@ask.launch
def launch():
    session.attributes['state']=DEFAULTSTATE
    session.attributes['routine']=None
    session.attributes['routines'] = []
    session.attributes['uid'] = 1001

@ask.intent("CreateRoutineIntent", convert={'dayofweek':str,'X':int})
def create_routine(dayofweek,X):

    routine_name=dayofweek+' '+str(X)
    for routine in session.attributes['routines']:
        if routine.name==routine_name:
            return question("Cannot create this routine, routine with same name already exists")
            ##############################################
    new_routine = Routine(session.attributes['uid'],routine_name)
    session.attributes['uid']=session.attributes['uid']+1
    session.attributes['routines'].append(new_routine)
    
    session.attributes['state']=MODIFYINGROUTINE
    session.attributes['routine']=new_routine
    return question('New routine created with name '+new_routine.name+' and id number '+new_routine.uid+\
    '. Would you like to make any changes? Tell me when you are done modifying the routine')

if __name__ == '__main__':

    app.run(debug=True)