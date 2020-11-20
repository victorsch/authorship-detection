from __future__ import division
import os
import sys
import nltk
from nltk import word_tokenize
from collections import Counter

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


# Average Number of Commas Per Sentece
def avgCommaOne1():
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

def avgCommaOne2():
    new = []
    length = len(token2)
    commas = 0
    sentences = 0
    for x in range(0,len(token2) - 2):
        new.append(token2[x] + ',' + token2[x+1] + ',' + token2[x+2] + ',')
        if(token2[x+2] == ','):
            commas += 1
        if(token2[x+2] == '.'):
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