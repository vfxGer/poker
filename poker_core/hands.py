#!/usr/bin/python
# -*- coding: utf-8 -*-
##################################
#  File:      /home/gerardk/eclipseWorkspace/AllPersonalProjects/poker/hands.py
#  Originally Created By:     gerardk
#  Originally Created On:     21 Feb 2012
#  Modified and Maintained by:   gerardk
#  Purpose:
"""
"""
#
#################################
#TODO: create a hand object

from functools import cmp_to_key
    
def getSequentialChunks(nums):
    """
    Copied from http://code.activestate.com/lists/python-list/524938/
    """
    chunks = []
    chunk = []
    for i,v in enumerate(nums[:-1]):
        v2 = nums[i+1]
        if v2-v == 1:
            if not chunk:
                chunk.append(v)
            chunk.append(v2)
        else:
            if not chunk:
                chunk.append(v)
            chunks.append(chunk)
            chunk = []
    if chunk:
        chunks.append(chunk)
    return chunks
 
def getLenMap(map_):
    result = {}
    for k in map_:
        result[k] = len(map_[k])
    return result
    
def getSuitMap(hand):
    """
    Return a map where the key is card suit and the value is list
    """
    result = {}
    for card in hand:
        cards = result.get(card.suit, [])
        cards.append(card)
        result[card.suit] = cards
    return result

def getRankMapOfHand(hand):
    """
    Return a map where the key is card rank and the value is a list of cards
    """
    result = {}
    for card in hand:
        cards = result.get(card.rank, [])
        cards.append(card)
        result[card.rank] = cards
    return result
    
def getNumberOfRankMap(hand):
    """
    Returns the number of cards with rank map
    """
    rankMap = getRankMapOfHand(hand)
    return getLenMap(rankMap)

def getNumberOfSuitMap(hand):
    return getLenMap(getSuitMap(hand))
    
def isSequentialRanks(hand, numberOfCards=5):
    """
    """
    def checkSeq(nums): 
        nums.sort()
        chunks = getSequentialChunks(nums)
        for chunk in chunks:
            if len(chunk)>=numberOfCards:
                return chunk
        return False
    
    ranks = []
    for card in hand:
        ranks.append(card.rank)
    chunk = checkSeq(ranks)
    if chunk:
        return max(chunk)
    
    ranks = []    
    for card in hand:
        if card.rank==14:
            ranks.append(1)
        else:
            ranks.append(card.rank)
    chunk = checkSeq(ranks)
    if chunk:
        return max(chunk)
    else:
        return chunk

def getHighestRankInSeq(hand):
    result = max(hand).rank
    if result!=14:
        return result
    else:
        withoutAce = hand[:]
        del(withoutAce[withoutAce.index(max(hand))])
        if max(withoutAce).rank==13:
            return 14
        else:
            return max(withoutAce).rank
        
def containsStraightFlush(hand):
    """
    Tests hand, which is a list of cards, to see if it contains a straight flush
    """
    suitMap = getSuitMap(hand)
    for suit in suitMap:
        if len(suitMap[suit])>=5:
            if isSequentialRanks(suitMap[suit]):
                return getHighestRankInSeq(suitMap[suit])
    return False

def containsNumberOfSameRank(hand, value):
    """
    Returns True or False if the hand contain ranks with the number as value
    """
    return value in getNumberOfRankMap(hand).values()
    
def getHighestRankOfNumber(hand, value):
    """
    """
    rankMap = getNumberOfRankMap(hand)
    if not value in rankMap.values():
        return 0
    result = 0
    for rank in rankMap:
        if rankMap[rank]==value:
            if result<rank:
                result = rank
    return result
        
    
    

def containsFourOfAKind(hand):
    """
    Tests hand which is a list of cards to see if it contains a straight flush
    """
    return getHighestRankOfNumber(hand, 4)

def containsFullHouse(hand):
    if containsNumberOfSameRank(hand, 2) and containsNumberOfSameRank(hand, 3):
        return getHighestRankOfNumber(hand, 3)
    else:
        return False

def containsFlush(hand):
    return 5 in getNumberOfSuitMap(hand).values()

def containsStraight(hand):
    return isSequentialRanks(hand, numberOfCards=5)
        

def containsThreeOfAKind(hand):
    return getHighestRankOfNumber(hand, 3)

def containsTwoPair(hand):
    ranks = getTwoPairRanks(hand)
    if ranks:
        return max(ranks)
    else:
        return False
    
def getTwoPairRanks(hand):
    rankMap = getNumberOfRankMap(hand)
    pairFound = 0
    ranks = []
    for rank in rankMap:
        if rankMap[rank]==2:
            ranks.append(rank)
            pairFound+=1
        if pairFound==2:
            return sorted(ranks)
    return []

def containsOnePair(hand):
    return getHighestRankOfNumber(hand, 2)

def getHighestCard(hand):
    return max(hand)

def getPokerHandsDB():
    return [
        ['One Pair', containsOnePair],
        ['Two Pair', containsTwoPair],
        ['Three of a kind', containsThreeOfAKind],
        ['Straight', containsStraight],
        ['Flush', containsFlush],
        ['Full House', containsFullHouse],
        ['Four of a kind', containsFourOfAKind],
        ['Straight flush', containsStraightFlush],
        ]
    
def getPokerHandRanking(hand):
    pokerHandDB = getPokerHandsDB()
    foundRank = None
    for rank,[_, containsFunc] in enumerate(pokerHandDB):
        res = int(containsFunc(hand))
        if res:
            foundRank = res + rank*20
    return foundRank
            
def compareHands(hand1, hand2):
    ranking1 = getPokerHandRanking(hand1)
    ranking2 = getPokerHandRanking(hand2)
    cmpResult = cmp(ranking1, ranking2)
    if cmpResult!=0:
        return cmpResult
    #because two pair needs to compare a pair of ranks
    if getHandName(hand1)=='Two Pair':
        ranks1 = getTwoPairRanks(hand1)
        ranks2 = getTwoPairRanks(hand2)
        cmpResult = cmp(ranks1, ranks2)
        if cmpResult!=0:
            return cmpResult
    highCard1 = getHighestCard(hand1)
    highCard2 = getHighestCard(hand2)
    return cmp(highCard1, highCard2)

def getHandName(hand):
    pokerHandDB = getPokerHandsDB()    
    ranking = None
    for rank,[_, containsFunc] in enumerate(pokerHandDB):
        if containsFunc(hand):
            ranking = rank
    if ranking!=None:
        return pokerHandDB[ranking][0]
    return "Highest Card"

def get_best_hands(hands):
    ms = []
    for i, hand in enumerate(hands):
        if i==0:
            ms.append(hand)
        else:
            r = compareHands(ms[-1], hand)
            if r==-1:
                ms = [hand]
            elif r==0:
                ms.append(hand)
            else:
                assert r==1
    return ms



def get_best_hands_from_map(your_round):
    highest = get_best_hands(your_round.values())
    # needs Python 2.7+ or 3
    return {k:v for k,v in your_round.items() if v in highest}

