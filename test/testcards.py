#!/usr/bin/python
# -*- coding: utf-8 -*-
##################################
#  File:      /home/gerardk/eclipseWorkspace/AllPersonalProjects/poker/testcards.py
#  Originally Created By:     gerardk
#  Originally Created On:     15 Feb 2012
#  Modified and Maintained by:   gerardk
#  Purpose:
"""
"""
#################################

import unittest
import mock

from poker_core import cards

class CardTests(unittest.TestCase):
    def setUp(self):
        self.cardD1 = cards.Card(suit=cards.DIAMOND, rank=1)
        self.cardD2 = cards.Card(suit=cards.DIAMOND, rank=2)
        self.cardC1 = cards.Card(suit=cards.CLUB, rank=1)
        self.cardH2 = cards.Card(suit=cards.HEART, rank=2)
        
        
    def testInValidSuit(self):
        try:
            cards.Card("a", 14)
        except cards.CardError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        try:
            cards.Card("s", 14)
        except cards.CardError:
            self.assertTrue(False)
            
    def testAceRank(self):
        card = cards.Card(suit=cards.CLUB, rank=1)
        self.assertEqual(card.rank, 14)
        
    def testSameSuit(self):
        self.assertEqual(self.cardD1.suit, self.cardD2.suit)
        
    def testDifferentSuit(self):
        self.assertNotEqual(self.cardD1.suit, self.cardC1.suit)
        
    def testSameRank(self):
        self.assertEqual(self.cardD1.rank, self.cardC1.rank)
        
    def testDifferentRank(self):
        self.assertNotEqual(self.cardD1.rank, self.cardH2.rank)
        
    def testRankOrderGreaterThen(self):
        self.assertTrue(self.cardD1.rank > self.cardH2.rank)
        
    def testRankOrderGreaterThenEqual(self):
        self.assertTrue(self.cardD1.rank  >= self.cardH2.rank)
        
    def testRankOrderLessThen(self):
        self.assertTrue(self.cardH2.rank<self.cardD1.rank)
    
    def testGetRankSting(self):
        self.assertEqual(self.cardD1.getRankString(), "A")
        
    def testShotHandHandCreation(self):
        handString = "9D AD JC"
        handDefined = [cards.Card(suit=cards.DIAMOND, rank=9),
                       cards.Card(suit=cards.DIAMOND, rank=1),
                       cards.Card(suit=cards.CLUB, rank=11)]
        self.assertEqual(cards.createHandFromShortHand(handString), handDefined)
        
    def testConvertToInt(self):
        self.assertEqual(int(self.cardD1), 14)
         
class PackTests(unittest.TestCase):
    def setUp(self):
        self.packOfCards = cards.Pack()
        
    def test52CardsAtInit(self):
        packOfCards = cards.Pack()
        self.assertEqual(len(packOfCards), 52)
        self.assertNotEqual(len(packOfCards), 51)
        
    def testDeal2GetTwoCards(self):
        self.packOfCards.resetPack()
        twoCards = self.packOfCards.getCards(2)
        self.assertEqual(len(twoCards), 2)
        self.assertEqual(len(self.packOfCards), 52-2)
        self.packOfCards.resetPack()
        
    def testResetCards(self):
        _ = self.packOfCards.getCards(2)
        self.packOfCards.resetPack()
        self.assertEqual(len(self.packOfCards), 52)

    @mock.patch('poker_core.randomnumbers.getRandomSeed')
    def testShuffle(self, mockRandomSeedMock):
        mockRandomSeedMock.return_value = 45462923
        lenBeforeShuffle = len(self.packOfCards)
        self.packOfCards.shuffle()
        self.assertEqual(lenBeforeShuffle, len(self.packOfCards))

    def test_takeCard(self):
        card = self.packOfCards.pickCard("9D")
        self.assertEqual(card.suit, cards.DIAMOND)
        self.assertEqual(len(self.packOfCards), 51)

def main():
    unittest.main()
    
if __name__=="__main__":
    main()
