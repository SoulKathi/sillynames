#!/usr/bin/env python

from flask import Flask, render_template
import csv
import logging
import random
import sys

CSV_FILE = 'names.csv'
CSV_HEADERS = ('Firstname', 'Lastname', 'Firstlastfunny', 'Resolution',
    'Explanation', 'Author', 'Comment')

logging.basicConfig(level=logging.DEBUG)

class Name:

    def __init__(self, firstname, lastname, firstlastfunny):
        self.firstname = firstname
        self.lastname = lastname
        self.firstlastfunny = firstlastfunny

def read_csv(f):
    dr = csv.DictReader(f, fieldnames=CSV_HEADERS, delimiter=';')
    names = []
    for row in dr:
        logging.debug('Got CSV row: %s' % row)
        name = Name(row['Firstname'], row['Lastname'], row['Firstlastfunny'])

        # The fields are not mandatory, so reading may fail gracefully with a
        # default value.
        name.resolution = row.get('Resolution')
        name.explanation = row.get('Explanation')
        name.author = row.get('Author')
        name.comment = row.get('Comment')
        logging.debug('Read name with firstname %s and lastname %s' %
                (name.firstname, name.lastname))
        names.append(name)
    return names

#
# Initialization.
#
app = Flask(__name__)

#import pdb; pdb.set_trace()

names = read_csv(open(CSV_FILE))

@app.route('/')
def random_name():

    # This ignores the first row, which contains the header.
    name = random.choice(names[1:])

    return render_template('name.html', name=name)
