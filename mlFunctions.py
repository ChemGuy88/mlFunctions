#!/usr/bin/env pytho3
# -*- coding: utf-8 -*-

'''
Machine Learning code
by Herman Autore

This is code that I've developed over time from classes and personal projects
'''

import datetime, markdown, re, os, sys, time
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.preprocessing as pp
from scipy import misc
from sklearn import datasets
from sklearn.decomposition import PCA, SparsePCA, MiniBatchSparsePCA
from sklearn.externals import joblib
from sklearn.linear_model import Lasso, Ridge
from sklearn.preprocessing import StandardScaler
from IPython import get_ipython

# For running IPython magic commands (e.g., %matplotlib)
# ipython = get_ipython()

# Display plots inline and change default figure size
# ipython.magic("matplotlib")

# Use latex in matplotlib
plt.rc('text', usetex=True)

'''
Functions
'''


def tic():
    '''
    Start marker for keeping time.
    '''
    # should create a class so I don't have to capture object so it works like in Matlab
    TIC = time.time()
    return TIC


def toc(TIC, mute=False):
    '''
    Counts how much time has passed since tic() was called, when one of its instances has been passed.
    '''
    TOC = time.time()
    d = TOC - TIC
    t = datetime.timedelta(seconds=d)
    if not mute:
        print('Elapsed time was %s (h:mm:ss)' % t)
    return t


def macAlarm(soundName = 'Pop'):
    bashCommand = 'afplay /System/Library/Sounds/%s.aiff' % soundName
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

def beep():
    sys.stdout.write("\a") # If you're on another screen this puts a notification on Terminal
    sys.stdout.flush()

def alarm(SECS = 1, Hz = 440):
	# duration = 1  # second
	# freq = 440  # Hz
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (SECS, Hz))

def alarm1():
    alarm(0.5,220)
    alarm(0.25,0)
    alarm(0.5,220)
    alarm(0.5,0)
    alarm(0.25,440)
    alarm(0.15,0)
    alarm(0.35,440)
    alarm(0.5,0)
    alarm(0.5,220)
    alarm(0.25,0)
    alarm(0.5,220)
    alarm(0.25,0)
    # Should replace lines below with a pop-up notification instead of hacking with "\a"
    sys.stdout.write("\a") # If you're on another screen this puts a notification on Terminal
    sys.stdout.flush()

def blocks(file, size=65536):
    '''
    From https://stackoverflow.com/a/9631635/5478086
    '''
    while True:
        b = file.read(size)
        if not b:
            break
        yield b

def getNumLines0(fname):
    '''
    From https://stackoverflow.com/a/9631635/5478086
    '''
    with open(fname, 'r', encoding="utf-8", errors='ignore') as f:
        genObj = (bl.count('\n') for bl in blocks(f))
        s = sum(genObj)
        print('%s has %d lines.' % (fname, s))

def getNumLines(fname, verbose=1):
    '''
    docstring
    '''
    # Verbose start
    if verbose > 0:
        TicSum = datetime.timedelta(0,0,0)
        timeStamp = ts()
        print('\n[%s] Counting number of lines in %s.' % (str(timeStamp), fname))
        # spinner = Spinner('')
        Tic = tic()
    with open(fname) as f:
        lines = (1 for line in f)
        numLines = 0
        for line in lines:
            numLines += 1
            if verbose > 0:
                pass
                # spinner.next()
    if verbose > 0:
        # spinner.finish()
        Toc = toc(Tic)
        TicSum += Toc

    # verbose exit
    if verbose > 0:
        print('\n[%s] There were %s lines in %s.' % (str(timeStamp), numLines, fname))

    return numLines

def run_from_ipython():
    '''
    Check if IPython has been imported. Useful for figuring out if a program has been called via $ python or $ ipython
    Credits to https://stackoverflow.com/questions/5376837/how-can-i-do-an-if-run-from-ipython-test-in-python
    '''
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def ts(dt=None, roundTo=60):
    '''
    Terminal-style prompt timeStamp for troubleshooting code. Can round a datetime object to any time lapse in seconds.
    ============================================================================
    Based on: Thierry Husson (2012) https://stackoverflow.com/a/10854034/5478086
    ============================================================================
    INPUT:
        dt : datetime.datetime object, default now.
        roundTo : Closest number of seconds to round to, default 1 minute.
    OUTPUT:
        A datetime object
    '''

    if dt == None:
        dt = datetime.datetime.now()
    if roundTo == None:
        return dt
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo

    return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

def importSASpdf(fname, copy='False'):
    '''
    Reads PDF files saved by SAS Studio and removes the leading numbers and whitespace. Saves result in the same directory with the file extension '.sas'.
    INPUT: fname, a full path string to the file PDF
           copy, boolean, (default 'False'), if 'True', will return the list of strings object.
    OUTPUT: a '.sas' file at fname.sas
            (optional) a list of strings.
    '''
    f = open(fname)
    lines = f.readlines()
    r = []
    for line in lines:
        ind = line.find(' ') + 1
        r.append(line[ind:])
    g = open(fname+'.sas','w')
    g.writelines(r)
    if copy:
        return r

def l1(vector, axis):
    result = np.linalg.norm(vector, axis=axis, ord=1)
    return result

def plotMatrices(dataFrame, path, fprefix, diag='hist'):
    I,J = dataFrame.shape
    NUMPLOTS = 10
    a = 0
    b = NUMPLOTS
    for i in range(J/NUMPLOTS):
        pd.plotting.scatter_matrix(dataFrame.iloc[:,a:b], alpha=0.2, figsize=(10, 8), diagonal=diag)
        fname = path + fprefix + '_%d.png' % (i+1)
        plt.savefig(fname)
        plt.close()
        plt.pause(0.01)
        a += NUMPLOTS
        b += NUMPLOTS

def makeDigraph_0(dft, type='clusters'):
	'''
	INPUT: dft, a pandas dataframe with labeled columns
           type: a string denoting the graph type as defined by the following three options:
           \'clusters\' graphs only nodes that are connected to other nodes
           \'selfs\' graphs only isolated nodes
           \'both\' graphs all significant nodes
	'''
	I,J = dft.shape
	G = nx.DiGraph()
	nodes = dft.columns

	# make edges
	edges = []
	for i in range(J):
		for j in range(J):
			weight = dft.iloc[i,j]
			if type == 'clusters':
				if (abs(weight) > 0.01) and (i != j):
					node1 = nodes[i]
					node2 = nodes[j]
					G.add_edge(node1,node2,weight=weight)
			if type == 'selfs':
				if (abs(weight) > 0.01) and (i == j):
					node1 = nodes[i]
					node2 = nodes[j]
					G.add_edge(node1,node2,weight=weight)
			if type == 'both':
				if (abs(weight) > 0.01):
					node1 = nodes[i]
					node2 = nodes[j]
					G.add_edge(node1,node2,weight=weight)
	return G

def makeDigraph(dft, type='clusters'):
    '''
    INPUT: dft, a pandas dataframe with labeled columns
           type: a string denoting the graph type as defined by the following three options:
           \'clusters\' graphs only nodes that are connected to other nodes
           \'selfs\' graphs only isolated nodes
           \'both\' graphs all significant nodes
    '''
    I,J = dft.shape
    G = nx.DiGraph()
    nodes = dft.columns

    # Create progress bar if J is very large
    if J > 1000:
        toolbar_width = 40
        print('Problem is extremely high-dimensional. Setting-up progress bar.')
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
        countdown = J*J
        countdown_step = int(np.ceil(countdown / float(toolbar_width)))
        # scale toolbar


    step = 0
    # make edges
    edges = []
    for i in range(J):
        for j in range(J):
            step += 1
            weight = dft.iloc[i,j]
            if type == 'clusters':
                if (abs(weight) > 0.01) and (i != j):
                    node1 = nodes[i]
                    node2 = nodes[j]
                    G.add_edge(node1,node2,weight=weight)
            if type == 'selfs':
                if (abs(weight) > 0.01) and (i == j):
                    node1 = nodes[i]
                    node2 = nodes[j]
                    G.add_edge(node1,node2,weight=weight)
            if type == 'both':
                if (abs(weight) > 0.01):
                    node1 = nodes[i]
                    node2 = nodes[j]
                    G.add_edge(node1,node2,weight=weight)
            if J > 1000:
                if step == countdown_step:
                    step = 0
                    sys.stdout.write("-")
                    sys.stdout.flush()
    sys.stdout.write("\n")
    return G

def match(first, second):
    '''
    From https://www.geeksforgeeks.org/wildcard-character-matching/
    The main function that checks if two given strings match.
    The first string may contain wildcard characters
    '''

    # If we reach at the end of both strings, we are done
    if len(first) == 0 and len(second) == 0:
        return True

    # Make sure that the characters after '*' are present
    # in second string. This function assumes that the first
    # string will not contain two consecutive '*'
    if len(first) > 1 and first[0] == '*' and  len(second) == 0:
        return False

    # If the first string contains '?', or current characters
    # of both strings match
    if (len(first) > 1 and first[0] == '?') or (len(first) != 0
        and len(second) !=0 and first[0] == second[0]):
        return match(first[1:],second[1:]);

    # If there is *, then there are two possibilities
    # a) We consider current character of second string
    # b) We ignore current character of second string.
    if len(first) !=0 and first[0] == '*':
        return match(first[1:],second) or match(first,second[1:])

    return False
