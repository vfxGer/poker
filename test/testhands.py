#!/usr/bin/python
# -*- coding: utf-8 -*-
##################################
#  File:      /home/gerardk/eclipseWorkspace/AllPersonalProjects/poker/testhands.py
#  Originally Created By:     gerardk
#  Originally Created On:     21 Feb 2012
#  Modified and Maintained by:   gerardk
#  Purpose:
"""
"""
# $Id:  $
# $HeadURL:  $
#
#################################
__svnVersion__ = "$Rev:  $".split()[1]
import unittest

from poker_core import hands
from poker_core import cards

class TestHands(unittest.TestCase):
    def setUp(self):
        self.fullHouseHand = [cards.Card(suit=cards.CLUB, rank=1),
                             cards.Card(suit=cards.DIAMOND, rank=1),
                            cards.Card(suit=cards.HEART, rank=1),
                            cards.Card(suit=cards.SPADE, rank=2),
                            cards.Card(suit=cards.HEART, rank=2)
                               ]
        self.fullHouse7Card = [cards.Card(cards.CLUB,8), 
             cards.Card(cards.CLUB,10), 
             cards.Card(cards.HEART,9), 
             cards.Card(cards.SPADE,3), 
             cards.Card(cards.CLUB,3),
             cards.Card(cards.SPADE,10), 
             cards.Card(cards.DIAMOND,10)
             ]

        self.noHand = [cards.Card(suit=cards.CLUB, rank=1),
                             cards.Card(suit=cards.DIAMOND, rank=3),
                            cards.Card(suit=cards.HEART, rank=6),
                            cards.Card(suit=cards.SPADE, rank=9),
                            cards.Card(suit=cards.HEART, rank=11)
                               ]
        self.twoPairHand1 = [cards.Card(cards.DIAMOND, 11),
                    cards.Card(cards.HEART, 9),
                    cards.Card(cards.HEART, 14),
                    cards.Card(cards.SPADE, 7),
                    cards.Card(cards.HEART, 4),
                    cards.Card(cards.HEART, 11),
                    cards.Card(cards.SPADE, 4)
                    ]
        self.test7CardOnePair = [cards.Card(cards.CLUB,6), 
         cards.Card(cards.SPADE,6), 
         cards.Card(cards.DIAMOND,4), 
         cards.Card(cards.DIAMOND,2), 
         cards.Card(cards.SPADE,3), 
         cards.Card(cards.CLUB,8), 
         cards.Card(cards.CLUB,13)]

    def testNotContainsStraightFlush(self):
        notStraightHand = [cards.Card(suit=cards.HEART, rank=2),
                        cards.Card(suit=cards.CLUB, rank=3),
                        cards.Card(suit=cards.CLUB, rank=4),
                        cards.Card(suit=cards.CLUB, rank=5),
                        cards.Card(suit=cards.CLUB, rank=6)
                           ]
        self.assertFalse(hands.containsStraightFlush(notStraightHand))
        
    def testRanksIsSequentailHand(self):
        seqHand = [cards.Card(suit=cards.CLUB, rank=2),
                        cards.Card(suit=cards.CLUB, rank=3),
                        cards.Card(suit=cards.DIAMOND, rank=4),
                        cards.Card(suit=cards.HEART, rank=5),
                        cards.Card(suit=cards.CLUB, rank=6)
                           ]
        self.assertTrue(hands.isSequentialRanks(seqHand))
        
        nonSeqHand = [cards.Card(suit=cards.HEART, rank=2),
                        cards.Card(suit=cards.CLUB, rank=2),
                        cards.Card(suit=cards.DIAMOND, rank=4),
                        cards.Card(suit=cards.HEART, rank=5),
                        cards.Card(suit=cards.CLUB, rank=6)
                           ]
        self.assertFalse(hands.isSequentialRanks(nonSeqHand))
     
    def testContainsStraightFlushHand(self):
        straightFlushHand = [cards.Card(suit=cards.CLUB, rank=1),
                        cards.Card(suit=cards.CLUB, rank=2),
                        cards.Card(suit=cards.CLUB, rank=3),
                        cards.Card(suit=cards.CLUB, rank=4),
                        cards.Card(suit=cards.CLUB, rank=5)
                           ]
        
        self.assertTrue(hands.containsStraightFlush(straightFlushHand))
        
    def testContainsStraightFlushHand7Cards(self):
        straightFlushHand = [cards.Card(suit=cards.CLUB, rank=1),
                        cards.Card(suit=cards.CLUB, rank=2),
                        cards.Card(suit=cards.CLUB, rank=3),
                        cards.Card(suit=cards.CLUB, rank=4),
                        cards.Card(suit=cards.CLUB, rank=5),
                        cards.Card(suit=cards.CLUB, rank=10),
                        cards.Card(suit=cards.CLUB, rank=8)
                           ]
        self.assertTrue(hands.containsStraightFlush(straightFlushHand))
            
    def testContainsStraightFlushRoyalHand(self):
        straightFlushHand = [cards.Card(suit=cards.CLUB, rank=1),
                        cards.Card(suit=cards.CLUB, rank=10),
                        cards.Card(suit=cards.CLUB, rank=11),
                        cards.Card(suit=cards.CLUB, rank=12),
                        cards.Card(suit=cards.CLUB, rank=13)
                           ]
        self.assertTrue(hands.containsStraightFlush(straightFlushHand))
        
    def testContainsFourOfAKind(self):
        fourOfAKindHand = [cards.Card(suit=cards.CLUB, rank=2),
                             cards.Card(suit=cards.DIAMOND, rank=2),
                            cards.Card(suit=cards.HEART, rank=2),
                            cards.Card(suit=cards.SPADE, rank=2),
                            cards.Card(suit=cards.HEART, rank=6)
                               ]
        self.assertTrue(hands.containsFourOfAKind(fourOfAKindHand))
        
    def testNotContainsFourOfAKind(self):
        fourOfAKindHand = [cards.Card(suit=cards.CLUB, rank=1),
                             cards.Card(suit=cards.DIAMOND, rank=2),
                            cards.Card(suit=cards.HEART, rank=2),
                            cards.Card(suit=cards.SPADE, rank=2),
                            cards.Card(suit=cards.HEART, rank=6)
                               ]
        self.assertFalse(hands.containsFourOfAKind(fourOfAKindHand))
    
    def testContainsFullHouse(self):
        self.assertTrue(hands.containsFullHouse(self.fullHouseHand))
        
    def testNotContainsFullHouse(self):
        notFullHouseHand = [cards.Card(suit=cards.CLUB, rank=1),
                             cards.Card(suit=cards.DIAMOND, rank=3),
                            cards.Card(suit=cards.HEART, rank=1),
                            cards.Card(suit=cards.SPADE, rank=2),
                            cards.Card(suit=cards.HEART, rank=2)
                               ]
        self.assertFalse(hands.containsFullHouse(notFullHouseHand))
    
    def testContainsFlush(self):
        testHand = [cards.Card(suit=cards.CLUB, rank=5),
                             cards.Card(suit=cards.CLUB, rank=11),
                            cards.Card(suit=cards.CLUB, rank=4),
                            cards.Card(suit=cards.CLUB, rank=12),
                            cards.Card(suit=cards.CLUB, rank=8)
                               ]
        self.assertTrue(hands.containsFlush(testHand))
        
    def testNotContainsFlush(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=5),
                             cards.Card(suit=cards.CLUB, rank=11),
                            cards.Card(suit=cards.CLUB, rank=4),
                            cards.Card(suit=cards.CLUB, rank=12),
                            cards.Card(suit=cards.CLUB, rank=8)
                               ]
        self.assertFalse(hands.containsFlush(testHand))
        
    def testGetSequentialChunks(self):
        nums = [5, 6, 4, 1, 2, 3]
        self.assertEqual(hands.getSequentialChunks(nums),
                                        [[5, 6], [4], [1, 2, 3]])
        self.assertEqual(nums, [5, 6, 4, 1, 2, 3])
        
    def testContainsStraight(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=2),
                    cards.Card(suit=cards.HEART, rank=3),
                    cards.Card(suit=cards.SPADE, rank=4),
                    cards.Card(suit=cards.CLUB, rank=5)
                    ]
        self.assertTrue(hands.containsStraight(testHand))
    
    def testNotContainsStraight(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=2),
                    cards.Card(suit=cards.HEART, rank=3),
                    cards.Card(suit=cards.SPADE, rank=4),
                    cards.Card(suit=cards.CLUB, rank=6)
                    ]
        self.assertFalse(hands.containsStraight(testHand))
    
    def testContainsThreeOfAKind(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=1),
                    cards.Card(suit=cards.HEART, rank=1),
                    cards.Card(suit=cards.SPADE, rank=4),
                    cards.Card(suit=cards.CLUB, rank=6)
                    ]
        self.assertTrue(hands.containsThreeOfAKind(testHand))
    
    def testNotContainsThreeOfAKind(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=1),
                    cards.Card(suit=cards.HEART, rank=3),
                    cards.Card(suit=cards.SPADE, rank=4),
                    cards.Card(suit=cards.CLUB, rank=6)
                    ]
        self.assertFalse(hands.containsThreeOfAKind(testHand))
        
    def testContainsTwoPair(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=1),
                    cards.Card(suit=cards.HEART, rank=3),
                    cards.Card(suit=cards.SPADE, rank=3),
                    cards.Card(suit=cards.CLUB, rank=6)
                    ]
        self.assertTrue(hands.containsTwoPair(testHand))
        
    def testNotContainsTwoPair(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=1),
                    cards.Card(suit=cards.HEART, rank=3),
                    cards.Card(suit=cards.SPADE, rank=4),
                    cards.Card(suit=cards.CLUB, rank=6)
                    ]
        self.assertFalse(hands.containsTwoPair(testHand))
        
    def testContainsOnePair(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=1),
                    cards.Card(suit=cards.HEART, rank=3),
                    cards.Card(suit=cards.SPADE, rank=4),
                    cards.Card(suit=cards.CLUB, rank=6)
                    ]
        self.assertTrue(hands.containsOnePair(testHand))
        
    def testContainsOnePair7Cards(self):
        
        self.assertTrue(hands.containsOnePair(self.test7CardOnePair))
        
    def testNotContainsOnePair(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=2),
                    cards.Card(suit=cards.HEART, rank=3),
                    cards.Card(suit=cards.SPADE, rank=4),
                    cards.Card(suit=cards.CLUB, rank=6)
                    ]
        self.assertFalse(hands.containsOnePair(testHand))
        
    def testGetHighestCard(self):
        testHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=2),
                    cards.Card(suit=cards.HEART, rank=3),
                    cards.Card(suit=cards.SPADE, rank=4),
                    cards.Card(suit=cards.CLUB, rank=6)
                    ]
        self.assertEqual(hands.getHighestCard(testHand).rank, 14)
        
    def testGetPokerHandRanking(self):
        self.assertEqual(hands.getPokerHandRanking(self.fullHouseHand), 114)
        
    def testCompareHandsOne(self):
        flushHand = [cards.Card(suit=cards.CLUB, rank=5),
                             cards.Card(suit=cards.CLUB, rank=11),
                            cards.Card(suit=cards.CLUB, rank=4),
                            cards.Card(suit=cards.CLUB, rank=12),
                            cards.Card(suit=cards.CLUB, rank=8)
                               ]
        flushHand2 = [cards.Card(suit=cards.DIAMOND, rank=5),
                             cards.Card(suit=cards.DIAMOND, rank=11),
                            cards.Card(suit=cards.DIAMOND, rank=4),
                            cards.Card(suit=cards.DIAMOND, rank=12),
                            cards.Card(suit=cards.DIAMOND, rank=8)
                               ]
        highCardHand = [cards.Card(suit=cards.DIAMOND, rank=1),
                    cards.Card(suit=cards.CLUB, rank=2),
                    cards.Card(suit=cards.HEART, rank=3),
                    cards.Card(suit=cards.SPADE, rank=4),
                    cards.Card(suit=cards.CLUB, rank=6)
                    ]
        self.assertEqual(hands.compareHands(flushHand, highCardHand), 1)
        self.assertEqual(hands.compareHands(highCardHand, flushHand), -1)
        self.assertEqual(hands.compareHands(flushHand2, flushHand), 0)
        
    def testAcesPairBeatsFivePair(self):
        """        
        Higher ranking pairs defeat lower ranking pairs; if two hands have the same pair, the non-paired cards (the kickers) are compared in descending order to determine the winner.
        """
        comCards =cards.createHandFromShortHand("9D AD 7H JS 6C")
        aceCards =cards.createHandFromShortHand("4D AC")
        fiveCards =cards.createHandFromShortHand("5C 5D")
        self.assertEqual(hands.compareHands(comCards+aceCards, comCards+fiveCards), 1)
        
    def testGetHighestRankOfNumber(self):
        hand =cards.createHandFromShortHand("9D AD 7H JS 6C 5C 5D")
        self.assertEqual(hands.getHighestRankOfNumber(hand, 2), 5)
        
    def testFullHouse7Card(self):
        commonCards = [cards.Card(cards.DIAMOND,10), 
         cards.Card(cards.SPADE,12), 
         cards.Card(cards.CLUB,8), 
         cards.Card(cards.DIAMOND,2), 
         cards.Card(cards.CLUB,4)]
        p0Cards = [cards.Card(cards.HEART,11), cards.Card(cards.CLUB,6)]
        p1Cards = [cards.Card(cards.SPADE,6), cards.Card(cards.DIAMOND,14)]
        self.assertEqual(hands.compareHands(p0Cards+commonCards, p1Cards+commonCards), -1)
        
    def testGetHandName(self):
        self.assertEqual(hands.getHandName(self.fullHouseHand), "Full House")
        self.assertEqual(hands.getHandName(self.noHand), "Highest Card")
        self.assertEqual(hands.getHandName(self.twoPairHand1), "Two Pair")
        self.assertEqual(hands.getHandName(self.test7CardOnePair), "One Pair")
        
    def testCompareStraightFlushes(self):
        hand1 =cards.createHandFromShortHand("10D JD QD KD AD")
        hand2 =cards.createHandFromShortHand("AD 2D 3D 4D 5D")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)
        
        hand3 =cards.createHandFromShortHand("9D 10D JD QD KD")
        hand4 =cards.createHandFromShortHand("2D 3D 4D 5D 6D")
        self.assertEqual(hands.compareHands(hand3, hand4), 1)
        
    def testComparePoker(self):
        hand1 =cards.createHandFromShortHand("10D KC KH KS KD")
        hand2 =cards.createHandFromShortHand("2D 2C 2S 2H AD")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)
        
    def testFullHouseCompare(self):
        hand1 =cards.createHandFromShortHand("2D 2C KH KS KD")
        hand2 =cards.createHandFromShortHand("AD AC JS JH JD")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)
        hand1 =cards.createHandFromShortHand("QD QC 4H 4S 4D")
        hand2 =cards.createHandFromShortHand("AD AC 3S 3H 3D")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)
        
    def testFlushCompare(self):
        hand1 =cards.createHandFromShortHand("QC 10C 7C 6C 4C")
        hand2 =cards.createHandFromShortHand("JS 10S 7S 6S 4S")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)
    
    def testStraightCompare(self):
        hand1 =cards.createHandFromShortHand("QC JS 10S 9H 8H 3S 2H")
        hand2 =cards.createHandFromShortHand("JS 10S 9H 8H 7D AS 4H")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)
        
    def test3OfAkindCompare(self):
        hand1 =cards.createHandFromShortHand("QS QH QD 7S 4C")
        hand2 =cards.createHandFromShortHand("JS JC JD AD KC")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)

    def test_flush_to_fullhouse_compare(self):
        #real life example
        community_cards = '6C QC QD AH 3C'
        community_cards = cards.createHandFromShortHand(community_cards)
        my_flush = cards.createHandFromShortHand('JC 5C')
        my_flush.extend(community_cards)

        my_full_house = cards.createHandFromShortHand('6S QH')
        my_full_house.extend(community_cards)

        self.assertEqual(hands.compareHands(my_flush, my_full_house), -1)
        self.assertEqual(hands.compareHands(my_full_house, my_flush), 1)

    def test_get_best_hands(self):
        #real life example
        community_cards = '6C QC QD AH 3C'
        community_cards = cards.createHandFromShortHand(community_cards)
        my_flush = cards.createHandFromShortHand('JC 5C')
        my_flush.extend(community_cards)

        my_full_house = cards.createHandFromShortHand('6S QH')
        my_full_house.extend(community_cards)

        print type(my_full_house)
        self.assertEqual(hands.get_best_hands([my_full_house, my_flush]), [my_full_house])



    def test2PairCompare(self):
        hand1 =cards.createHandFromShortHand("10S 10C 8H 8C 4S")
        hand2 =cards.createHandFromShortHand("8H 8C 4S 4C 10S")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)
        
        hand1 =cards.createHandFromShortHand("10S 10C 8H 8C 4S")
        hand2 =cards.createHandFromShortHand("10S 10C 4S 4H 8H")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)
        
        hand1 =cards.createHandFromShortHand("10S 10C 8H 8S AD")
        hand2 =cards.createHandFromShortHand("10S 10C 8H 8S 4S")
        self.assertEqual(hands.compareHands(hand1, hand2), 1)

    def test_get_best_hands_from_map(self):
        this_hands = []
        this_hands.append(cards.createHandFromShortHand("QS QH"))
        this_hands.append(cards.createHandFromShortHand("JS JC"))
        this_hands.append(cards.createHandFromShortHand("10S 10C"))
        this_hands.append(cards.createHandFromShortHand("8H 8C"))
        this_hands = dict(enumerate(this_hands))
        self.assertEqual(hands.get_best_hands_from_map(this_hands),
                        {0: cards.createHandFromShortHand("QS QH")}
                         )

    def test_get_best_hands_from_map_equal(self):
        this_hands = []
        this_hands.append(cards.createHandFromShortHand("QS QH"))
        this_hands.append(cards.createHandFromShortHand("QC QD"))
        this_hands.append(cards.createHandFromShortHand("JS JC"))
        this_hands.append(cards.createHandFromShortHand("10S 10C"))
        this_hands.append(cards.createHandFromShortHand("8H 8C"))
        this_hands = dict(enumerate(this_hands))
        self.assertEqual(hands.get_best_hands_from_map(this_hands),
                        {0: cards.createHandFromShortHand("QS QH"),
                         1:cards.createHandFromShortHand("QC QD")}
                         )

    def test_get_best_hands_from_map_not_change_arg(self):
        this_hands = []
        this_hands.append(cards.createHandFromShortHand("QS QH"))
        this_hands.append(cards.createHandFromShortHand("QC QD"))
        this_hands.append(cards.createHandFromShortHand("JS JC"))
        this_hands.append(cards.createHandFromShortHand("10S 10C"))
        this_hands.append(cards.createHandFromShortHand("8H 8C"))
        this_hands = dict(enumerate(this_hands))
        saved_copy = this_hands.copy()
        hands.get_best_hands_from_map(this_hands)
        self.assertEqual(saved_copy, this_hands)

    def test_get_best_hands_from_map_1(self):
        community_cards = '6C QC QD AH 3C'
        community_cards = cards.createHandFromShortHand(community_cards)
        this_hands = []
        this_hands.append(cards.createHandFromShortHand('JC 5C'))
        this_hands[-1].extend(community_cards)
        this_hands.append(cards.createHandFromShortHand('6S QH'))
        this_hands[-1].extend(community_cards)

        hand_map = dict(enumerate(this_hands))
        best_hands = hands.get_best_hands_from_map(hand_map)
        print hands.getHandName(hand_map[0])
        print hands.getHandName(hand_map[1])
        self.assertItemsEqual(best_hands.keys(), [1])

def main():
    unittest.main()

    
if __name__=="__main__":
    main()
