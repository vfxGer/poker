#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""

import random
import logging

import randomnumbers


class CardError(Exception):
    """
    For error's that occur with poker
    """
    pass
DIAMOND, SPADE, CLUB, HEART = "d", "s", "c", "h"

def createHandFromShortHand(shortHand):
    """
    Creates a list of card objects from a string
    eg 9D AD JC
    """ 
    cards = shortHand.split(" ")
    logging.debug(cards)
    return [createCardFromShort(card) for card in cards]
    
def createCardFromShort(shrtCard):
    suit = shrtCard[-1].lower()
    rawRank = shrtCard[:-1]
    if rawRank == "A":
        rank = 14
    elif rawRank == "K":
        rank = 13
    elif rawRank == "Q":
        rank = 12
    elif rawRank == "J":
        rank = 11
    else:
        rank = int(rawRank)
    return Card(suit, rank)
    
class Card(object):
    """
    Represents a card in a pack of cards
    
    Ranks
     
    * 11 Jack 
    * 12 Queen 
    * 13 King 
    * 14 Ace
    
    Suits
    
    * d diamond
    * s spade
    * c club 
    * h heart
    """
    POSSIBLE_SUITS = [ DIAMOND, SPADE, CLUB, HEART ]        
    def __init__(self, suit, rank):
        if not suit in self.POSSIBLE_SUITS:
            raise CardError, "Not a valid suit %s" % suit
        self.rank = int(rank)
        if self.rank==1:
            self.rank = 14
        if not self.rank in range(2,15):
            raise CardError, "Not a valid rank %s" % rank
        self.suit = suit
        
    def __repr__(self):
        modName = "cards"
        res = "%s.Card("%modName
        if self.suit==HEART:
            res += "%s.HEART"%modName
        elif self.suit==SPADE:
            res += "%s.SPADE"%modName
        elif self.suit==DIAMOND:
            res += "%s.DIAMOND"%modName
        elif self.suit==CLUB:
            res += "%s.CLUB"%modName
        res+=",%d)"%(self.rank)
        return res
        
    def __cmp__(self, other):
        try:
            return cmp(self.rank, other.rank)
        except AttributeError:
            raise AttributeError("Can only compare cards to other cards")
    
    def __str__(self):
        if self.suit==HEART:
            suitString = "H"
        elif self.suit==SPADE:
            suitString = "S"
        elif self.suit==DIAMOND:
            suitString = "D"
        elif self.suit==CLUB:
            suitString = "C"
        rankString = self.getRankString()
        return "%s%s" % (rankString, suitString)
    
    def __unicode__(self):
        if self.suit==HEART:
            suitString = unichr(9829)
        elif self.suit==SPADE:
            suitString = unichr(9824)
        elif self.suit==DIAMOND:
            suitString = unichr(9830)
        elif self.suit==CLUB:
            suitString = unichr(9827)
        rankString = self.getRankString()
        return "%s%s" % (rankString, suitString)
    
    def __int__(self):
        return self.rank
    
    def getRankString(self):
        """
        """
        if self.rank==14:
            return "A"
        elif self.rank==13:
            return "K"
        elif self.rank==12:
            return "Q"
        elif self.rank==11:
            return "J"
        else:
            return "%d" % self.rank
        
class Pack(object):
    def __init__(self):
        self.cards = []
        for i in xrange(1,14):
            for s in Card.POSSIBLE_SUITS:
                self.cards.append(Card(s, i))
        self.dealtCards = []
        
    def __len__(self):
        return len(self.cards)
            
    def resetPack(self):
        self.cards.extend(self.dealtCards)
        
    def shuffle(self):
        random.seed(randomnumbers.getRandomSeed())
        random.shuffle(self.cards)
        
    def getCards(self, number=1):
        result = []
        for _ in xrange(number):
            newCard = self.cards.pop()
            self.dealtCards.append(newCard)
            result.append(newCard)
        return result
    
    def pickCard(self, name):
        card = createCardFromShort(name)
        self.cards.remove(card)
        self.dealtCards.append(card)
        return card

        