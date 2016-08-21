#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import time
import os

def pickle_path():
    dir_path = os.path.dirname(__file__)
    return os.path.join(dir_path, "random_number_list.pickle")

def getRandomSeed():
    """
    Get a number to use to seed the random number
    """
    fp = open(pickle_path(), 'r')
    #fp = open("C:/Users/gkeating/eclipse_workspace/poker_project/random_number_list.pickle", 'r')
    randomNumbers = pickle.load(fp)
    fp.close()
    t = time.time()
    return randomNumbers[int(t*100000)%10000]
            
if __name__=="__main__":
    print getRandomSeed()