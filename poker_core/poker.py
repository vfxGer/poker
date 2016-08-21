#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import cards

def playTexasEm():
    p1Cards = []
    p2Cards = []
    sharedCards = []
    cardPack = cards.Pack()
    ######
    cardPack.shuffle()
    p1Cards.extend(cardPack.getCards(1))
    p2Cards.extend(cardPack.getCards(1))
    
    p1Cards.extend(cardPack.getCards(1))
    p2Cards.extend(cardPack.getCards(1))
    
    print "p1: %s %s"%(p1Cards[0], p1Cards[1])
    print "p2: %s %s"%(p2Cards[0], p2Cards[1])
    time.sleep(1)
    sharedCards.extend(cardPack.getCards(3))
    print "%s %s %s" % (sharedCards[0], sharedCards[1], sharedCards[2])
    r=raw_input("Bet:")
    sharedCards.extend(cardPack.getCards(1))
    print "%s %s %s %s" % (sharedCards[0], sharedCards[1], sharedCards[2], sharedCards[3])
    r=raw_input("Bet:")
    sharedCards.extend(cardPack.getCards(1))
    print "%s %s %s %s %s" % (sharedCards[0], sharedCards[1], sharedCards[2], sharedCards[3], sharedCards[4])
    r=raw_input("Bet:")
    
def test():
    cardPack = cards.Pack()
    cardPack.shuffle()
    hand = cardPack.getCards(5)
    for c in hand:
        print "%s " % c,
    print " "
    
if __name__=="__main__":
    playTexasEm()