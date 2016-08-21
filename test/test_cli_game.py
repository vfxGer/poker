#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'gerardk'

import unittest

import mock

import collections

from cli import game
from cli.players import CLIPlayer, AIPlayerInterface
from poker_core import cards
from cli.player_state import CLI_Player_State

from pprint import pprint

def get_default_players():
    players = collections.OrderedDict({})
    for i in xrange(5):
        players["Player_%d" % i] = AIPlayerInterface()
    players["Ger"] = CLIPlayer()
    return players

class Test_Players(unittest.TestCase):
    @mock.patch("__builtin__.raw_input")
    def test_cli_player_bet_fold(self, mock_raw_input):
        mock_raw_input.return_value = "F"
        player = CLIPlayer()
        res = player.bet([('fold', 0), ('all-in', 50000), ('check', 20000), ('raise', 40000)])
        mock_raw_input.assert_called_once_with("f: Fold, c: Check 20000, r: Raise 40000+, a: All-in 50000\n")
        self.assertEqual(res, ('fold', 0))

    @mock.patch("__builtin__.raw_input")
    def test_cli_player_bet_all_in(self, mock_raw_input):
        mock_raw_input.return_value = "F"
        player = CLIPlayer()
        res = player.bet([('fold', 0), ('all-in', 50000), ('check', 20000), ('raise', 40000)])
        mock_raw_input.assert_called_once_with("f: Fold, c: Check 20000, r: Raise 40000+, a: All-in 50000\n")
        self.assertEqual(res, ('fold', 0))

class Test_game(unittest.TestCase):

    def test_start_game(self):
        this_game = game.CLI_Game()
        this_game.get_game_state()

    def test_get_player_cards_maps(self):
        #given
        this_game = game.CLI_Game()
        deal = [cards.createHandFromShortHand("QS QH"),
                cards.createHandFromShortHand("QC QD")
                ]
        this_game.community_cards = cards.createHandFromShortHand("AC AD AH")


        #TODO: use set game state
        for i in xrange(2):
            new_player = game.Player_State("Player_%d" % i, AIPlayerInterface())
            this_game.players.append(new_player)
            this_game.players[i].cards = deal[i]

        #then
        self.assertEqual(this_game.get_player_cards_maps(),
                         {  'Player_0': cards.createHandFromShortHand("QS QH AC AD AH"),
                            'Player_1': cards.createHandFromShortHand("QC QD AC AD AH")})

    def test_move_button(self):
        this_game = game.CLI_Game()
        #TODO: use set game state
        my_players = []
        for i in xrange(3):
            new_player = CLI_Player_State("Player_%d" % i, AIPlayerInterface())
            this_game.players.append(new_player)
            my_players.append(new_player)
        this_game.button = 0
        this_game.pot = 0
        #
        this_game.move_button()
        #
        self.assertEqual(this_game.current_betters,
                            collections.deque([my_players[1], my_players[2], my_players[0]]))

    def test_get_game_state(self):
        this_game = game.CLI_Game()
        this_game.init_players()
        this_game.new_round()
        state = this_game.get_game_state()
        self.assertEqual(state['game_stage'], None)
        self.assertEqual(state['pot'], 30000)#big and small blinds paid
        self.assertEqual(state['button'], 'Player_0')
        self.assertEqual(state['blind_small'],
                         'Player_1')
        self.assertEqual(state['blind_big'],
                         'Player_2')
        self.assertEqual(state['player_chips'],
                         {'Ger': 50000,
                          'Player_0': 50000,
                          'Player_1': 40000,
                          'Player_2': 30000,
                          'Player_3': 50000,
                          'Player_4': 50000
                            })
        self.assertIn("community_cards", state)
        self.assertEqual(state["community_cards"], [])

    def assert_games_state_equal(self, new_game_state, set_game_state):
        for key in set_game_state:
            if not key in ["news"]:
                self.assertIn(key, new_game_state)
                self.assertEqual(new_game_state[key],
                                 set_game_state[key],
                                 msg="new_game_state[%s]=%s != set_game_state[%s]=%s" \
                                     %(key,  new_game_state[key], key, set_game_state[key]))


#    def test_set_game_state_flop(self):
#        new_state = {
#            'players':get_default_players(),
#            'blind_big': 'Player_2',
#            'blind_small': 'Player_1',
#            'button': 'Player_0',
#            'community_cards': ['7H', '7D', 'KS'],
#            'current_bet': 20000,
#            'game_stage': 'flop',
#            'news': [],
#            'player_chips': {'Ger': 50000,
#                              'Player_0': 50000,
#                              'Player_1': 40000,
#                              'Player_2': 30000,
#                              'Player_3': 50000,
#                              'Player_4': 50000},
#            'pot': 30000}
#        this_game = game.Game()
#        this_game.set_game_state(new_state)
#        this_game_state = this_game.get_game_state()
#        self.assert_games_state_equal(this_game_state, new_state)
#        for key in new_state:
#            self.assertEqual(this_game_state[key],
#                             new_state[key],
#                             msg="this_game_state[%s]=%s != new_state[%s]=%s" \
#                                 %(key, this_game_state[key], key, new_state[key]))
#{'betting': {'Ger': None,
#             'Player_0': None,
#             'Player_1': ('bet', 10000),
#             'Player_2': ('bet', 20000),
#             'Player_3': None,
#             'Player_4': None,
#             'curent_bet': 20000},
# 'blind_big': 'Player_2',
# 'blind_small': 'Player_1',
# 'button': 'Player_0',
# 'cards': {'Ger': ['9C', '2D'],
#           'Player_0': ['6C', '8C'],
#           'Player_1': ['4D', 'AD'],
#           'Player_2': ['6S', '3H'],
#           'Player_3': ['AS', '9D'],
#           'Player_4': ['8S', '7H']},
# 'community_cards': [],
# 'game stage': 'pre-flop',
# 'news': [],
# 'player_chips': {'Ger': 50000,
#                  'Player_0': 50000,
#                  'Player_1': 40000,
#                  'Player_2': 30000,
#                  'Player_3': 50000,
#                  'Player_4': 50000},
# 'pot': 30000}


    def test_betting_options(self):
        #given
        this_game = game.CLI_Game()
        #TODO: use set game state
        for i in xrange(3):
            new_player = CLI_Player_State("Player_%d" % i,
                                           AIPlayerInterface())
            this_game.players.append(new_player)
        this_game.button = 0
        this_game.pot = 0
        this_game.move_button()
        this_game.get_blinds()
        self.assertEqual(this_game.get_small_blind_player().name, 'Player_2')
        self.assertEqual(this_game.get_big_blind_player().name, 'Player_0')
        this_game.betting_stage = "betting"
        print this_game.get_player_chips()
        #when
 #       {'betting': {'Player_0': ('bet', 20000),
 #            'Player_1': None,
 #            'Player_2': ('bet', 10000)},
 #'blind_big': 'Player_0',
 #'blind_small': 'Player_2',
 #'button': 'Player_1',
 #'cards': {'Player_0': ['KS', '5C'],
 #          'Player_1': ['JC', '9S'],
 #          'Player_2': ['KD', '4S']},
 #'community_cards': [],
 #'game stage': 'pre-flop',
 #'news': [],
 #'player_chips': {'Player_0': 30000, 'Player_1': 50000, 'Player_2': 40000},
 #'pot': 30000}
        betting_options = this_game.get_current_betting_options()
        #
        self.assertIn(('fold', 0), betting_options)
        self.assertIn(('all-in', 50000), betting_options)
        self.assertIn(('check', 20000), betting_options)
        self.assertIn(('raise', 40000), betting_options)

    def test_betting_options_more_players(self):
        #given
        this_game = game.CLI_Game()
        #TODO: use set game state
        for i in xrange(6):
            new_player = CLI_Player_State("Player_%d" % i,
                                           AIPlayerInterface())
            this_game.players.append(new_player)
        this_game.button = 0
        this_game.pot = 0
        this_game.move_button()
        this_game.get_blinds()
        self.assertEqual(this_game.get_small_blind_player().name, 'Player_2')
        self.assertEqual(this_game.get_big_blind_player().name, 'Player_3')
        this_game.betting_stage = "betting"
        print this_game.get_player_chips()
        #when
 #       {'betting': {'Player_0': ('bet', 20000),
 #            'Player_1': None,
 #            'Player_2': ('bet', 10000)},
 #'blind_big': 'Player_0',
 #'blind_small': 'Player_2',
 #'button': 'Player_1',
 #'cards': {'Player_0': ['KS', '5C'],
 #          'Player_1': ['JC', '9S'],
 #          'Player_2': ['KD', '4S']},
 #'community_cards': [],
 #'game stage': 'pre-flop',
 #'news': [],
 #'player_chips': {'Player_0': 30000, 'Player_1': 50000, 'Player_2': 40000},
 #'pot': 30000}
        betting_options = this_game.get_current_betting_options()
        #
        self.assertIn(('fold', 0), betting_options)
        self.assertIn(('all-in', 50000), betting_options)
        self.assertIn(('check', 20000), betting_options)
        self.assertIn(('raise', 40000), betting_options)

    def test_preflop_bet(self):
        my_players = collections.OrderedDict({})
        for i in xrange(3):
            my_players["Player_%d" % i] = mock.MagicMock(spec=AIPlayerInterface, name="Player_%d" % i)
            my_players["Player_%d" % i].bet.return_value = ('fold', 0)
        set_state = {
            'players':my_players,
            'blind_big': 'Player_2',
            'blind_small': 'Player_1',
            'button': 'Player_0',
            'game_stage': 'flop',
            'news': [],
            'player_chips': {'Player_0': 50000,
                              'Player_1': 40000,
                              'Player_2': 30000,
                            },
            'current_bet': 20000,
            'pot': 30000}
        this_game = game.CLI_Game()
        this_game.set_game_state(set_state)

        new_game_state = None
        for ng in this_game.iter_step():
            new_game_state = ng
            break
        self.assertTrue(my_players['Player_0'].bet.called)
        for ng in this_game.iter_step():
            new_game_state = ng
            break
        player2_win = {'button': 'Player_1',
                        'player_chips': {'Player_0': 50000,
                                          'Player_1': 40000,
                                          'Player_2': 60000,
                                        },
                        'pot': 0}
        self.assertEqual(new_game_state['player_chips'],
                              player2_win['player_chips'])

    def test_get_betting_history(self):
        my_players = collections.OrderedDict({})
        for i in xrange(3):
            my_players["Player_%d" % i] = mock.MagicMock(spec=AIPlayerInterface, name="Player_%d" % i)
            my_players["Player_%d" % i].bet.return_value = ('fold', 0)
        set_state = {
            'players':my_players,
            'blind_big': 'Player_2',
            'blind_small': 'Player_1',
            'button': 'Player_0',
            'game_stage': 'flop',
            'news': [],
            'player_chips': {'Player_0': 50000,
                              'Player_1': 40000,
                              'Player_2': 30000,
                            },
            'current_bet': 20000,
            'pot': 30000}
        this_game = game.CLI_Game()
        this_game.set_game_state(set_state)

        new_game_state = None
        for ng in this_game.iter_step():
            new_game_state = ng
            break
        from pprint import pprint
        pprint(new_game_state)
        print "-"*10
        self.assertTrue(my_players['Player_0'].bet.called)
        self.assertIn('betting_history', new_game_state)
        self.assertEqual(new_game_state['betting_history'],
                      [('Player_1', [[]]),
                       ('Player_2', [[]]),
                       ('Player_0', [[('fold', 0)]]) ]
                )

    def test_get_betting_history_ante(self):
        my_players = collections.OrderedDict({})
        for i in xrange(3):
            my_players["Player_%d" % i] = mock.MagicMock(spec=AIPlayerInterface, name="Player_%d" % i)
            my_players["Player_%d" % i].bet.return_value = ('fold', 0)
        this_game = game.CLI_Game()
        this_game.set_players(my_players)
        this_game.new_round()

        new_game_state = None

        for ng in this_game.iter_step():
            new_game_state = ng
            break
        for ng in this_game.iter_step():
            new_game_state = ng
            break
        from pprint import pprint
        pprint(new_game_state)
        print "-"*10
        self.assertTrue(my_players['Player_0'].bet.called)
        self.assertIn('betting_history', new_game_state)
        self.assertEqual(new_game_state['betting_history'],
                      [('Player_1', [[('ante', 10000)]]),
                       ('Player_2', [[('ante', 20000)]]),
                       ('Player_0', [[('fold', 0)]]) ]
                )

    def test_start_of_game_betting(self):
        my_players = get_default_players()
        this_game = game.CLI_Game()
        this_game.set_players(my_players)
        this_game.new_round()
        new_game_state = this_game.get_game_state()
        #for ng in this_game.iter_step:
        #    new_game_state = ng
        #    break
        expect_game_state = {'betting': {'Ger': None,
             'Player_0': None,
             'Player_1': 'ante',
             'Player_2': 'ante',
             'Player_3': None,
             'Player_4': None},
             'betting_history': [('Player_3', [[]]),
                                 ('Player_4', [[]]),
                                 ('Ger',      [[]]),
                                 ('Player_0', [[]]),
                                 ('Player_1', [[('ante', 10000)]]),
                                 ('Player_2', [[('ante', 20000)]])
                                 ],
             'blind_big': 'Player_2',
             'blind_small': 'Player_1',
             'button': 'Player_0',
             'community_cards': [],
             'current_bet': 20000,
             'game_stage': None,
             'news': [],
             'player_chips': {'Ger': 50000,
                              'Player_0': 50000,
                              'Player_1': 40000,
                              'Player_2': 30000,
                              'Player_3': 50000,
                              'Player_4': 50000},
             'pot': 30000}
        self.assertItemsEqual(expect_game_state['betting_history'], new_game_state['betting_history'] )
        self.assert_games_state_equal(new_game_state, expect_game_state)

    def test_betting_states(self):
        set_game_state = {'betting': {'Ger': None,
             'Player_0': None,
             'Player_1': ('ante', 10000),
             'Player_2': ('ante', 20000),
             'Player_3': 'fold',
             'Player_4': None},
          #this is a list because it should be ordered
         'betting_history': [('Player_4', [[]]),
                             ('Ger', [[]]),
                             ('Player_0', [[]]),
                             ('Player_1', [[('ante', 10000)]]),
                             ('Player_2', [[('ante', 20000)]]),
                             ('Player_3', [[('fold', 0)]])],
         'blind_big': 'Player_2',
         'blind_small': 'Player_1',
         'button': 'Player_0',
         'community_cards': [],
         'current_bet': 20000,
         'game_stage': 'pre-flop',
         'player_chips': {'Ger': 50000,
                          'Player_0': 50000,
                          'Player_1': 40000,
                          'Player_2': 30000,
                          'Player_3': 50000,
                          'Player_4': 50000},
         'players': get_default_players(),
         'pot': 30000}
        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = this_game.get_game_state()
        self.assert_games_state_equal(new_game_state, set_game_state)

    def test_dealing_cards(self):
        set_game_state = {'betting': {'Ger': None,
             'Player_0': None,
             'Player_1': ('bet', 10000),
             'Player_2': ('bet', 20000),
             'Player_3': 'fold',
             'Player_4': None},
          #this is a list because it should be ordered
         'betting_history': [('Player_4', []),
                             ('Ger', []),
                             ('Player_0', []),
                             ('Player_1', [[('ante', 10000)]]),
                             ('Player_2', [[('ante', 20000)]]),
                             ('Player_3', [[('fold', 0)]])],
         'blind_big': 'Player_2',
         'blind_small': 'Player_1',
         'button': 'Player_0',
         'community_cards': [],
         'current_bet': 20000,
         'game_stage': 'pre-flop',
         'player_chips': {'Ger': 50000,
                          'Player_0': 50000,
                          'Player_1': 40000,
                          'Player_2': 30000,
                          'Player_3': 50000,
                          'Player_4': 50000},
         'players': get_default_players(),
         'pot': 30000}
        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = next(this_game.iter_step)
        self.assertEqual(new_game_state['community_cards'], [])

    def test_dealing_cards(self):
        set_game_state = {'betting': {'Ger': None,
             'Player_0': None,
             'Player_1': ('bet', 10000),
             'Player_2': ('bet', 20000),
             'Player_3': 'fold',
             'Player_4': None},
          #this is a list because it should be ordered
         'betting_history': [('Player_4', []),
                             ('Ger', []),
                             ('Player_0', []),
                             ('Player_1', [[('ante', 10000)]]),
                             ('Player_2', [[('ante', 20000)]]),
                             ('Player_3', [[('fold', 0)]])],
         'blind_big': 'Player_2',
         'blind_small': 'Player_1',
         'button': 'Player_0',
         'community_cards': [],
         'current_bet': 20000,
         'game_stage': 'pre-flop',
         'player_chips': {'Ger': 50000,
                          'Player_0': 50000,
                          'Player_1': 40000,
                          'Player_2': 30000,
                          'Player_3': 50000,
                          'Player_4': 50000},
         'players': get_default_players(),
         'pot': 30000}
        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = next(this_game.iter_step())
        self.assertEqual(new_game_state['community_cards'], [])

    def test_show_player_cards(self):
        set_game_state = {'betting': {'Ger': None,
             'Player_0': None,
             'Player_1': ('bet', 10000),
             'Player_2': ('bet', 20000),
             'Player_3': 'fold',
             'Player_4': None},
                'cards': {'Ger': ["QS", "QH"],
                         'Player_0': ["QC", "QD"],
                         'Player_1': ["JS", "JC"],
                         'Player_2': ["10S", "10C"],
                         'Player_3': ["8H", "8C"],
                         'Player_4': ["2D", "7S"]
                        },
              #this is a list because it should be ordered
             'betting_history': [('Player_4', []),
                                 ('Ger', []),
                                 ('Player_0', []),
                                 ('Player_1', [[('ante', 10000)]]),
                                 ('Player_2', [[('ante', 20000)]]),
                                 ('Player_3', [[('fold', 0)]])],
             'blind_big': 'Player_2',
             'blind_small': 'Player_1',
             'button': 'Player_0',
             'community_cards': [],
             'current_bet': 20000,
             'game_stage': 'pre-flop',
             'player_chips': {'Ger': 50000,
                              'Player_0': 50000,
                              'Player_1': 40000,
                              'Player_2': 30000,
                              'Player_3': 50000,
                              'Player_4': 50000},
             'players': get_default_players(),
             'pot': 30000}
        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = next(this_game.iter_step('Ger'))
        self.assertNotEqual(new_game_state['player_cards'], [])
        self.assertEqual(new_game_state['player_cards'], ["QS", "QH"])

    def test_deal_cards(self):
        set_game_state = {'betting': {'Ger': None,
             'Player_0': None,
             'Player_1': ('bet', 10000),
             'Player_2': ('bet', 20000),
             'Player_3': 'fold',
             'Player_4': None},
              #this is a list because it should be ordered
             #'betting_history': [('Player_4', []),
             #                    ('Ger', []),
             #                    ('Player_0', []),
             #                    ('Player_1', [('ante', 10000)]),
             #                    ('Player_2', [('ante', 20000)]),
             #                    ('Player_3', [],
             'blind_big': 'Player_2',
             'blind_small': 'Player_1',
             'button': 'Player_0',
             'community_cards': [],
             'current_bet': 20000,
             'game_stage': 'pre-flop',
             'player_chips': {'Ger': 50000,
                              'Player_0': 50000,
                              'Player_1': 40000,
                              'Player_2': 30000,
                              'Player_3': 50000,
                              'Player_4': 50000},
             'players': get_default_players(),
             'pot': 30000}
        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = next(this_game.iter_step('Ger'))
        self.assertNotEqual(new_game_state['player_cards'], [])
        self.assertEqual(len(new_game_state['player_cards']), 2)

        #self.assertEqual(new_game_state['player_cards'], ["QS", "QH"])
    def test_winning(self):
        #winners= {'Player_2': [cards.Card(cards.DIAMOND,10), cards.Card(cards.DIAMOND,11)]}
        set_game_state = {'betting': {'Ger': 'fold',
                                     'Player_0': 'fold',
                                     'Player_1': 'fold',
                                     'Player_2': 'ante',
                                     'Player_3': 'fold',
                                     'Player_4': 'fold'},
                         'betting_history': [('Player_2', [[('ante', 20000)]]),
                                             ('Player_0', [[('fold', 0)]]),
                                             ('Player_1', [[('ante', 10000), ('fold', 0)]]),
                                             ('Player_3', [[('fold', 0)]]),
                                             ('Player_4', [[('fold', 0)]]),
                                             ('Ger', [[('fold', 0)]])],
                         'blind_big': 'Player_2',
                         'blind_small': 'Player_1',
                         'button': 'Player_0',
                         'cards': {'Ger': ['8H', '4H'],
                                   'Player_0': ['2S', '2C'],
                                   'Player_1': ['8D', '4S'],
                                   'Player_2': ['10D', 'JD'],
                                   'Player_3': ['JH', '3H'],
                                   'Player_4': ['8C', '10C']},
                         'community_cards': [],
                         'current_bet': 20000,
                         'game_stage': 'payout',
                         'player_cards': ['8H', '4H'],
                         'player_chips': {'Ger': 50000,
                                          'Player_0': 50000,
                                          'Player_1': 40000,
                                          'Player_2': 60000,
                                          'Player_3': 50000,
                                          'Player_4': 50000},
                         'players': get_default_players(),
                         'pot': 0}
        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = next(this_game.iter_step('Ger', debug=True))
        this_game.new_round()
        new_game_state = this_game.get_game_state()
        self.assertEqual(new_game_state['betting']['Player_4'], None)
        self.assertEqual(new_game_state['blind_big'], 'Player_3')
        self.assertNotEqual(new_game_state.get('game_stage'), 'payout')

    def test_get_player_cards_maps(self):
        my_game = game.CLI_Game()
        my_game.init_players()
        my_game.new_round()
        next(my_game.iter_step('Ger', debug=True))
        cards_map = my_game.get_player_cards_maps()
        self.assertItemsEqual(cards_map.keys(), ['Ger',
                                          'Player_0',
                                          'Player_1',
                                          'Player_2',
                                          'Player_3',
                                          'Player_4'])

    def test_check(self):
        mock_player3 = mock.MagicMock()
        mock_player3.bet.return_value = ('check', 20000)
        players = get_default_players()
        players['Player_3'] = mock_player3

        set_game_state = {'betting': {'Ger': None,
                                     'Player_0': None,
                                     'Player_1': 'ante',
                                     'Player_2': 'ante',
                                     'Player_3': None,
                                     'Player_4': None},
                         'betting_history': [('Player_3', [[]]),
                                             ('Player_4', [[]]),
                                             ('Ger', [[]]),
                                             ('Player_0', [[]]),
                                             ('Player_1', [[('ante', 10000)]]),
                                             ('Player_2', [[('ante', 20000)]])],
                         'blind_big': 'Player_2',
                         'blind_small': 'Player_1',
                         'button': 'Player_0',
                         'cards': {'Ger': ['4S', '2S'],
                                   'Player_0': ['2D', 'AH'],
                                   'Player_1': ['8D', '10S'],
                                   'Player_2': ['10D', 'QS'],
                                   'Player_3': ['KS', '6H'],
                                   'Player_4': ['7H', '6C']},
                         'community_cards': [],
                         'current_bet': 20000,
                         'game_stage': 'pre-flop',
                         'news': ['New round'],
                         'player_cards': ['4S', '2S'],
                         'player_chips': {'Ger': 50000,
                                          'Player_0': 50000,
                                          'Player_1': 40000,
                                          'Player_2': 30000,
                                          'Player_3': 50000,
                                          'Player_4': 50000},
                        'players':players,
                        'pot': 30000}

        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = next(this_game.iter_step('Ger', debug=True))
        self.assertEqual(new_game_state['player_chips']['Player_3'], 30000)
        self.assertEqual(new_game_state['pot'], 50000)

    def test_check_no_bet(self):
        mock_Ger = mock.MagicMock()
        mock_Ger.bet.return_value = ('check', 10000)

        mock_player0 = mock.MagicMock()

        players = collections.OrderedDict({})
        players["Player_0" ] = mock_player0
        players["Ger"] = mock_Ger

        set_game_state = {'betting': {'Ger': 'check',
                                     'Player_0': 'ante'},
                         'betting_history': [('Player_0', [[('ante', 20000)]]),
                                             ('Ger',  [[('ante', 10000),('check', 10000)]]),
                                             ],
                         'blind_big': 'Player_0',
                         'blind_small': 'Ger',
                         'button': 'Ger',
                         'cards': {'Ger': ['4S', '2S'],
                                   'Player_0': ['AD', 'AH']
                                   },
                         'community_cards': [],
                         'current_bet': 20000,
                         'game_stage': 'pre-flop',
                         'player_cards': ['4S', '2S'],
                         'player_chips': {'Ger': 30000,
                                          'Player_0': 30000
                                          },
                        'players':players,
                        'pot': 40000}

        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = next(this_game.iter_step('Ger', debug=True))
        self.assertEqual(mock_player0.bet.call_args_list[0][0][0],
                            [('fold', 0), ('all-in', 30000), ('check', 0), ('raise', 20000)])

    def test_new_betting_round(self):
        players = get_default_players()
        players["Ger"] = mock.MagicMock()
        set_game_state = {'betting': {'Ger': 'check',
             'Player_0': 'fold',
             'Player_1': 'fold',
             'Player_2': 'check',
             'Player_3': 'fold',
             'Player_4': 'fold'},
         'betting_history': [('Ger', [[('check', 20000)]]),
                             ('Player_2', [[('ante', 20000), ('check', 0)]]),
                             ('Player_0', [[('fold', 0)]]),
                             ('Player_1', [[('ante', 10000), ('fold', 0)]]),
                             ('Player_3', [[('fold', 0)]]),
                             ('Player_4', [[('fold', 0)]])],
         'blind_big': 'Player_2',
         'blind_small': 'Player_1',
         'button': 'Player_0',
         'cards': {'Ger': ['KD', '7C'],
                   'Player_0': ['7D', '9D'],
                   'Player_1': ['6S', '5C'],
                   'Player_2': ['10S', '8C'],
                   'Player_3': ['QC', '3S'],
                   'Player_4': ['8S', '4C']},
         'community_cards': [],
         'current_bet': 0,
         'game_stage': 'pre-flop',
         'news': ["Player_4 ('fold', 0)",
                  "Ger ('check', 20000)",
                  "Player_0 ('fold', 0)",
                  "Player_1 ('fold', 0)",
                  "Player_2 ('check', 0)"],
         'player_cards': ['KD', '7C'],
         'player_chips': {'Ger': 30000,
                          'Player_0': 50000,
                          'Player_1': 40000,
                          'Player_2': 30000,
                          'Player_3': 50000,
                          'Player_4': 50000},
         'players': players,
         'pot': 50000}
        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = next(this_game.iter_step('Ger', debug=True))
        self.assertEqual(sorted(players["Ger"].bet.call_args_list[0][0][0]),
                         sorted([('fold', 0), ('all-in', 30000), ('raise',20000),('check', 0)]))

    def test_deal_flop(self):
        mock_Ger = mock.MagicMock()
        mock_Ger.bet.return_value = ('check', 0)

        mock_player0 = mock.MagicMock()
        mock_player0.bet.return_value = ('check', 0)


        players = collections.OrderedDict({})
        players["Player_0" ] = mock_player0
        players["Ger"] = mock_Ger

        set_game_state = {'betting': {'Ger': 'check',
                                     'Player_0': 'check'},
                         'betting_history': [ ('Ger',  [[('ante', 10000),('check', 10000)]]),
                                              ('Player_0', [[('ante', 20000),('check',0)]])
                                             ,
                                             ],
                         'blind_big': 'Player_0',
                         'blind_small': 'Ger',
                         'button': 'Ger',
                         'cards': {'Ger': ['4S', '2S'],
                                   'Player_0': ['AD', 'AH']
                                   },
                         'community_cards': [],
                         'current_bet': 0,
                         'game_stage': 'pre-flop',
                         'player_cards': ['4S', '2S'],
                         'player_chips': {'Ger': 30000,
                                          'Player_0': 30000
                                          },
                        'players':players,
                        'pot': 40000}

        this_game = game.CLI_Game()
        this_game.set_game_state(set_game_state)
        new_game_state = next(this_game.iter_step('Ger', debug=True))
        self.assertNotEqual(new_game_state['community_cards'], [])

    def test_first_round(self):
        my_game = game.CLI_Game()
        my_game.init_players()
        my_game.new_round()
        new_game_state = None
        for game_state in my_game.iter_step('Ger', debug=True):
            new_game_state = game_state
            break
        self.assertIn("pot", new_game_state)


    def test_deal_flop2(self):
        players = get_default_players()
        players['Ger'] = mock.MagicMock()
        new_game_state = {'betting': {'Ger': 'check',
                                     'Player_0': 'fold',
                                     'Player_1': 'fold',
                                     'Player_2': 'check',
                                     'Player_3': 'fold',
                                     'Player_4': 'fold'},
                        'betting_history': [('Ger', [[('check', 20000)]]),
                                             ('Player_2', [[('ante', 20000), ('check', 0)]]),
                                             ('Player_0', [[('fold', 0)]]),
                                             ('Player_1', [[('ante', 10000), ('fold', 0)]]),
                                             ('Player_3', [[('fold', 0)]]),
                                             ('Player_4', [[('fold', 0)]])],
                         'blind_big': 'Player_2',
                         'blind_small': 'Player_1',
                         'button': 'Player_0',
                         'community_cards': [],
                         'current_bet': 20000,
                         'game_stage': 'pre-flop',
                         'news': ["Player_4 ('fold', 0)",
                                  "Ger ('check', 20000)",
                                  "Player_0 ('fold', 0)",
                                  "Player_1 ('fold', 0)",
                                  "Player_2 ('check', 0)"],
                         'player_cards': ['QC', '9H'],
                         'player_chips': {'Ger': 30000,
                                          'Player_0': 50000,
                                          'Player_1': 40000,
                                          'Player_2': 30000,
                                          'Player_3': 50000,
                                          'Player_4': 50000},
                         'players': players,
                         'pot':50000}
        this_game = game.CLI_Game()
        this_game.set_game_state(new_game_state)
        new_game_state = next(this_game.iter_step('Ger', debug=True))
        self.assertNotEqual(new_game_state['community_cards'], [])
        self.assertNotEqual(players['Ger'].bet.call_args_list[0][0][1]['community_cards'], [])

    def test_bet(self):
        players = get_default_players()
        players['Player_3'] = mock.MagicMock()
        players['Player_3'].bet.return_value = ('fold', 0)

        new_game_state = {'betting': {'Ger': 'raise',
                                    'Player_0': 'fold',
                                     'Player_1': 'fold',
                                     'Player_2': 'fold',
                                     'Player_3': 'check',
                                     'Player_4': 'fold'},
                         'betting_history': [('Ger', [[('check', 20000)], [('raise', 20000)]]),
                                             ('Player_3',
                                              [[('ante', 20000), ('check', 0)], []]),
                                             ('Player_0', [[('fold', 0)]]),
                                             ('Player_1', [[('fold', 0)]]),
                                             ('Player_2', [[('ante', 10000), ('fold', 0)]]),
                                             ('Player_4', [[('fold', 0)]])],
                         'blind_big': 'Player_3',
                         'blind_small': 'Player_2',
                         'button': 'Player_1',
                         'cards': {'Ger': ['7S', '4S'],
                                   'Player_0': ['10D', '2S'],
                                   'Player_1': ['2C', 'AC'],
                                   'Player_2': ['JS', '7C'],
                                   'Player_3': ['3H', '2D'],
                                   'Player_4': ['9C', '6C']},
                         'community_cards': ['AD', 'KH', '7H'],
                         'current_bet': 0,
                         'game_stage': 'flop',
                         'news': ["Player_1 ('fold', 0)",
                                  "Player_2 ('fold', 0)",
                                  "Player_3 ('check', 0)",
                                  "Ger ('raise', 20000)"],
                         'player_cards': ['7S', '4S'],
                         'player_chips': {'Ger': 10000,
                                          'Player_0': 50000,
                                          'Player_1': 40000,
                                          'Player_2': 50000,
                                          'Player_3': 30000,
                                          'Player_4': 50000},
                         'players': players,
                         'pot': 70000}
        this_game = game.CLI_Game()
        this_game.set_game_state(new_game_state)
        new_game_state = next(this_game.iter_step('Ger', debug=True))
        self.assertEqual(players['Player_3'].bet.call_count, 1)
        self.assertItemsEqual(players['Player_3'].bet.call_args_list[0][0][0],
                         [('fold', 0), ('all-in', 30000), ('check', 20000)])

    def test_betting_after_allin(self):
        players = get_default_players()
        players['Ger'] = mock.MagicMock()
        players['Ger'].bet.side_effect = Exception()
        players['Player_2'] = mock.MagicMock()
        players['Player_2'].bet.return_value = ('fold', 0)

        new_game_state = {'betting': {'Ger': 'all-in',
                                         'Player_0': 'fold',
                                         'Player_1': 'fold',
                                         'Player_2': 'ante',
                                         'Player_3': 'fold',
                                         'Player_4': 'fold'},
                     'betting_history': [('Player_2', [[('ante', 20000)]]),
                                         ('Ger', [[('all-in', 50000)]]),
                                         ('Player_0', [[('fold', 0)]]),
                                         ('Player_1', [[('ante', 10000), ('fold', 0)]]),
                                         ('Player_3', [[('fold', 0)]]),
                                         ('Player_4', [[('fold', 0)]])],
                     'blind_big': 'Player_2',
                     'blind_small': 'Player_1',
                     'button': 'Player_0',
                     'cards': {'Ger': ['4S', '6C'],
                               'Player_0': ['AC', '3S'],
                               'Player_1': ['9H', '8H'],
                               'Player_2': ['AD', '10H'],
                               'Player_3': ['QC', 'JH'],
                               'Player_4': ['3C', '8S']},
                     'community_cards': [],
                     'current_bet': 20000,
                     'game_stage': 'pre-flop',
                     'news': ["Player_3 ('fold', 0)",
                              "Player_4 ('fold', 0)",
                              "Ger ('all-in', 50000)",
                              "Player_0 ('fold', 0)",
                              "Player_1 ('fold', 0)"],
                     'player_cards': ['4S', '6C'],
                     'player_chips': {'Ger': 0,
                                      'Player_0': 50000,
                                      'Player_1': 40000,
                                      'Player_2': 30000,
                                      'Player_3': 50000,
                                      'Player_4': 50000},
                     'players': players,
                     'pot':80000}

        this_game = game.CLI_Game()
        this_game.set_game_state(new_game_state)
        new_game_state = next(this_game.iter_step('Ger', debug=True))

        self.assertEqual(players['Ger'].bet.call_count, 0)
        new_game_state = next(this_game.iter_step('Ger', debug=True))

        self.assertEqual(players['Player_2'].bet.call_count, 1)
        self.assertItemsEqual(players['Player_2'].bet.call_args_list[0][0][0],
                         [('fold', 0), ('all-in', 30000)])

    def test_no_money_for_ante(self):
        players_int = collections.OrderedDict({})
        for i in xrange(3):
            players_int["Player_%d" % i] = AIPlayerInterface()
        players = []
        for i in xrange(3):
            name = "Player_%d" % i
            players.append(CLI_Player_State(name, players_int[name]))
            players[-1].chips = 10000
        new_game_state = {'players':players,
                        'betting': {
                            'Player_0': None,
                            'Player_1': None,
                            'Player_2': None},
                        'betting_history': [('Player_0', [[]]),
                        ('Player_1', [[]]),
                        ('Player_2', [[]])],
                     'blind_big': 'Player_2',
                     'blind_small': 'Player_1',
                     'button': 'Player_0',
     'cards': {'Player_0': [],
               'Player_1': [],
               'Player_2': []},
     'community_cards': [],
     'current_bet': 200000,
      'player_chips': {'Player_0': 200000,
                      'Player_1': 30000,
                      'Player_2': 20000}}

        this_game = game.CLI_Game()
        this_game.players = players
        this_game.new_round()
        new_game_state = this_game.get_game_state('Player_2', debug=True)
        pprint(new_game_state)
        self.assertEqual(new_game_state['betting_history'][-1], ('Player_2', [[('all-in', 10000)]]))

    # def test_cant_allin_when_more_money(self):
    #     players_int = collections.OrderedDict({})
    #     for i in xrange(3):
    #         if i==0:
    #             players_int["Player_%d" % i] = mock.MagicMock()
    #         else:
    #             players_int["Player_%d" % i] = AI_Player_Interface()
    #     players = []
    #     for i in xrange(3):
    #         name = "Player_%d" % i
    #         players.append(game.Player_State(name, players_int[name]))
    #         players[-1].chips = 10000
    #     new_game_state = {'players':players,
    #                     'betting': {
    #                         'Player_0': None,
    #                         'Player_1': None,
    #                         'Player_2': None},
    #                     'betting_history': [('Player_0', [[]]),
    #                     ('Player_1', [[]]),
    #                     ('Player_2', [[]])],
    #                  'blind_big': 'Player_2',
    #                  'blind_small': 'Player_1',
    #                  'button': 'Player_0',
    #  'cards': {'Player_0': [],
    #            'Player_1': [],
    #            'Player_2': []},
    #  'community_cards': [],
    #  'current_bet': 200000,
    #   'player_chips': {'Player_0':200000,
    #                   'Player_1':  30000,
    #                   'Player_2':  20000}}
    #
    #     this_game = game.Game()
    #     this_game.players = players
    #     this_game.new_round()
    #     new_game_state = this_game.get_game_state('Player_2', debug=True)
    #     pprint(new_game_state)
    #     self.assertEqual(new_game_state['betting_history'][-1], ('Player_2', [[('all-in', 10000)]]))
    #     new_game_state = next(this_game.iter_step('Player_0', debug=True))
    #     new_game_state = next(this_game.iter_step('Player_0', debug=True))
    #     self.assertTrue(players_int["Player_0"].bet.called)
    #     can_bet = players_int["Player_0"].bet.call_args_list[0][0][0]
    #     self.assertTrue(('fold', 0) in can_bet)
    #     self.assertIn(('check', 30000), can_bet)

if __name__ == '__main__':
    unittest.main()
