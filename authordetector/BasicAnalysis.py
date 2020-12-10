from __future__ import division
import os
import sys
import nltk
from nltk import word_tokenize
from collections import Counter

import sqlite3  # This is to access the database with information about known authors
from sqlite3 import Error
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

# Tensorflow Related
# import tensorflow as tf
# import tensorflow_hub as hub

# Connect to db
def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

# Made the authors table
authors_sql = """
CREATE TABLE authors (
    id integer PRIMARY KEY,
    Name text NOT NULL,
    work1 text NOT NULL,
    work2 text NOT NULL,
    work3 text NOT NULL,
    work4 text NOT NULL,
    work5 text NOT NULL,
    avgsentencelength float NOT NULL,
    avgcommaspersent float NOT NULL,
    unique(Name))"""

# SQL code to add a new author into our database
new_author = """
INSERT INTO authors (
    Name,
    work1,
    work2,
    work3,
    work4,
    work5,
    avgsentencelength,
    avgcommaspersent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""


# Ngram Function
def ngram(inputToken):
    new = []
    for x in range(0,len(inputToken) - 2):
        new.append(inputToken[x] + ',' + inputToken[x+1] + ',' + inputToken[x+2] + ',')
    return(new)


# Average Sentence Length Function
def avgSentLength(input):
    new = []
    tokenizedSentence = word_tokenize(input)
    length = len(tokenizedSentence)
    sentences = 0
    for x in range(0,len(tokenizedSentence) - 2):
        new.append(tokenizedSentence[x] + ',' + tokenizedSentence[x+1] + ',' + tokenizedSentence[x+2] + ',')
        if(tokenizedSentence[x+2] == '.'):
            sentences += 1
    return(length/sentences)


# Average Number of Commas Per Sentence
def avgCommasPerSentence(token):
    new = []
    length = len(token)
    commas = 0
    sentences = 0
    for x in range(0,len(token) - 2):
        new.append(token[x] + ',' + token[x+1] + ',' + token[x+2] + ',')
        if(token[x+2] == ','):
            commas += 1
        if(token[x+2] == '.'):
            sentences += 1
    return(commas/sentences)

#Compare two ngram function
def ngramComparison(ngram1, ngram2):
    ngram1 = word_tokenize(ngram1)
    ngram2 = word_tokenize(ngram2)
    ngram1 = ngram(ngram1)
    ngram2 = ngram(ngram2)
    pct_similarity = (len(list(set(ngram1).intersection(ngram2)))) / len(ngram2)
    print(pct_similarity)
    return(pct_similarity)

def sentenceLengthComparison(input1, input2):
    return( avgSentLength(input1) / avgSentLength(input2))


def add_new_author(name, work1, work2, work3, work4, work5):
    totalworks = work1 + work2 + work3 + work4 + work5
    try:
        avgsentencelen = avgSentLength(totalworks)
        avgcommas = avgCommasPerSentence(word_tokenize(totalworks))
    except ZeroDivisionError as e:
        print("Formatting Error: The texts you provided were not formatted correctly and couldn't be added to the database. Please follow the guidelines provided.")
        return


    con = db_connect()  #  connect to the database
    cur = con.cursor()  #  instantiate a cursor obj

    #  cur.execute(authors_sql) No longer needed since we already created the table

    # Show the possible tables to choose from, probably able to be deleted
    # cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='authors'")

    # Execute the SQL code to add the new author to the database
    cur.execute(new_author, (name,
                             work1,
                             work2,
                             work3,
                             work4,
                             work5,
                             avgsentencelen,
                             avgcommas))

    cur.execute("SELECT * FROM authors")
    print(cur.fetchall())
    con.commit()
    con.close()


def list_authors():
    con = db_connect()  # connect to the database
    cur = con.cursor()  # instantiate a cursor obj


    cur.execute("SELECT * FROM authors")
    return(cur.fetchall())
    con.commit()
    con.close()


list_authors()
#  add_new_author("Victor", "This is a proper text. Take Notes Victor.", "Ernest Hemingway is a. stupid little bitch.", "Ouch my tummy hurts. Please take note.", "Hopefully this submission will. work unlike the previous ones.", "I dont care about your. elbow you old harpey.")
#  add_new_author("Victor", "This is a proper text. Take Notes Victor.", "Ernest Hemingway is a. stupid little bitch.", "Ouch my tummy hurts. Please take note.", "Hopefully this submission will. work unlike the previous ones.", "I dont care about your. elbow you old harpey.")