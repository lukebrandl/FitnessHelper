# -*- coding: utf-8 -*-
"""
classes for exercise assistant
"""

class Exercise(object):
    def __init__(self,uid,name,part):
        self.uid=uid
        self.name=name
        self.part=part
        self.description='No description'
        
class ExerciseInstance(object):
    def __init__(self,exercise,reps,sets,rest):    
        self.exercise=exercise
        self.reps=reps
        self.sets=sets
        self.rest=rest
        self.time=(rest+20)*sets
        
class Routine(object):
    def __init__(self,uid,name):
        self.uid=uid
        self.name=name
        self.exercises=[]
 