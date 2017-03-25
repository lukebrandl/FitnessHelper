# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:51:49 2017

@author: brandl
"""

import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)