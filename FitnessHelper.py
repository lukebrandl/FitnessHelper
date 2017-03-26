# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:51:49 2017

@author: brandl
"""

import logging

from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from Classes import Exercise, ExerciseInstance, Routine

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

########## Various possible states
DEFAULTSTATE=0
MODIFYINGROUTINE=1

@ask.launch
def launch():
#    session.attributes['state']=DEFAULTSTATE
    session.attributes['state']=MODIFYINGROUTINE
    session.attributes['routine']=None
    session.attributes['routines'] = []
    session.attributes['exercises']=[]
    session.attributes['uid'] = 1001

    #DEFAULTS
    myexercise = Exercise(0,'Lunges','Quadriceps').__dict__ 
    session.attributes['exercises'].append(myexercise)
    myexercise = Exercise(1,'sit ups','Abdominals').__dict__ 
    session.attributes['exercises'].append(myexercise)
    myroutine = Routine(10,'Friday 7') .__dict__
    session.attributes['routine']=myroutine
#    myroutine['exercises'].append(ExerciseInstance('Lunges',4,10,30).__dict__)
    myroutine['exercises'].append(ExerciseInstance('sit ups',3,50,30).__dict__)
    session.attributes['routines'].append(myroutine)
    
    return question("Welcome to Fitness Assistant")

################### STATELESS INTENTS
@ask.intent("CreateRoutineIntent", convert={'dayofweek':str,'X':int})
def create_routine(dayofweek,X):

    print ('creating routine############################')
    routine_name=dayofweek+' '+str(X)
    for routine in session.attributes['routines']:
        if routine['name']==routine_name:
            return question("Cannot create this routine, routine with same name already exists")
            ##############################################
    new_routine = Routine(session.attributes['uid'],routine_name)
    session.attributes['uid']=session.attributes['uid']+1
    session.attributes['routines'].append(new_routine.__dict__)
    session.attributes['state']=MODIFYINGROUTINE
    session.attributes['routine']=new_routine.__dict__
#    print( session.attributes['routine'])
    #myroutine=session.attributes['routine']
#    print(session.attributes['routine'])
#    print(session.attributes['routine']['name'])
#    return question(render_template('TestIntent'))
    return question(render_template('CreateRoutineIntent',dayofweek=dayofweek,X=X))
    #'New routine created with name '+new_routine.name+' and id number '+str(new_routine.uid)+\
#    '. Would you like to make any changes? Tell me when you are done modifying the routine')

@ask.intent("ListRoutinesIntent")
def list_routines():
    
    print('###################')
    routines ='' 
    for routine in session.attributes['routines']:
        routines=routines+str(routine['name'])+' \n'
    return question(render_template('ListRoutinesIntent', routines=routines))

@ask.intent("CreateExerciseIntent",convert={'newexercise':str})
def create_exercise(newexercise): 
    exercise_name=newexercise    
    for exercise in session.attributes['exercises']:
        if exercise['name']==exercise_name:
            return question("Cannot create this exercise as an exercise with same name already exists")
    new_exercise=Exercise(session.attributes['uid'],exercise_name,'body')
    session.attributes['uid']=session.attributes['uid']+1
    session.attributes['exercises'].append(new_exercise.__dict__)

    return question(render_template('CreateExerciseIntent',exercise_name=exercise_name))
    
@ask.intent("ListExercisesIntent")
def list_exercises(): 
    
    #print('###################')
    exercises ='' 
    for exercise in session.attributes['exercises']:
        exercises=exercises+str(exercise['name'])+' \n'
    return question(render_template('ListExercisesIntent', exercises=exercises))  
   
   
########## MODIFYING ROUTINE INTENTS
@ask.intent("AddExerciseIntent",convert={'exercise':str,'setnum':int,'repnum':int})
def add_exercise(newexercise,exercise,setnum,repnum):     
    if(session.attributes['state']!=MODIFYINGROUTINE):
        return question("You don't have an active routine to modify. Either chose a routine to modify or create a new routine")
    exercise_name=exercise
    myex=None
    for ex in session.attributes['exercises']:
        if ex['name']==exercise_name:
            myex=ex
    if myex==None:
        return question("I couldn't find this exercise in your exercises. Have you created it yet?")
    myinstance = ExerciseInstance(exercise_name,setnum,repnum,30)
    session.attributes['routine']['exercises'].append(myinstance.__dict__)
    return question(render_template('AddExerciseIntent', len(session.attributes['routine']['exercises'])))
        
            
if __name__ == '__main__':

    app.run(debug=True)