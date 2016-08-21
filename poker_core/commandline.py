#!env python
'''
Created on 2 May 2012

@author: gkeating
'''
import time

import cards
import hands
import logging

def printHand(hand):
    for card in hand:
        print unicode(card) + " ",
    print ""
        
def printStatus(playersCards, comCards):
    print "#"*10
    printHand(comCards)
    
    for number, cards in enumerate(playersCards):
        print "P%d:"%number,
        logging.debug(cards)
        printHand(cards)
    print "#"*10
    print " "
        
def getWinners(playersHands, comCards):
    """
    Return multiple winners for a draw
    """
    fullHands = [h + comCards for h in playersHands]
    maxHand = fullHands[0]
    winners = []
    for player, hand in enumerate(fullHands):
        cmpRes = hands.compareHands(hand, maxHand)
        logging.debug(cmpRes)
        logging.debug(hand)
        logging.debug(hands.getHandName(hand))
        if cmpRes==0:
            winners.append(player)
        elif cmpRes==1:
            winners = [player]
            maxHand = hand
    return winners 
            
def playGame(numberOfPlayers=3):
    sleepTime = 0
    #get deck
    pack = cards.Pack()
    pack.shuffle()
    playersHands = []
    comCards = []
    #deal cards
    for _ in xrange(numberOfPlayers):
        playersHands.append(pack.getCards(2))
    printStatus(playersHands, comCards)
    time.sleep(sleepTime)
    comCards.extend(pack.getCards(3))
    printStatus(playersHands, comCards)
    time.sleep(sleepTime)
    comCards.extend(pack.getCards(1))
    printStatus(playersHands, comCards)
    time.sleep(sleepTime)
    comCards.extend(pack.getCards(1))
    printStatus(playersHands, comCards)
    time.sleep(sleepTime)
    #winner
    winnersName = getWinners(playersHands, comCards)
    print winnersName
    print hands.getHandName(playersHands[winnersName[0]]+comCards)
    
def main():
    while True:
        playGame()
        if 'n' in raw_input("Continue [Y/N]:").lower():
            return  

if __name__=="__main__":
    main()