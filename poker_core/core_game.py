#!/usr/bin/env python
# encoding: utf-8
"""
Created by gerardk on 02/01/2014.
"""

import logging
from math import floor
from copy import copy
from collections import deque, OrderedDict

import poker_core.cards as cards
from player_state import Player_State

from defaults import DEFAULT_NUM_PLAYERS

class PokerGameException(BaseException):
    pass

#TODO: move to core game
class Core_Game(object):
    def __init__(self):
        self.players = []
        self.button = 0
        self.pot = 0
        self.news = deque([], 5)
        self.card_pack = cards.Pack()
        self.community_cards = []
        self.game_stage = None
        self.betting_stage = None
        self._current_betters = None
        self.game_state = None
#        self.current_bet = None

    def set_players(self, players):
        self.players = []
        for name in players:
            self.players.append(Player_State(name, players[name]))

    def remove_losers(self):
        losers = []
        for player in self.players:
            if player.chips==0:
                losers.append(player)
        for loser in losers:
            msg = "%s has lost"%loser.name
            print(msg)
            self.news.append(msg)
            self.players.remove(loser)

    def get_blinds(self):
        self.pot += self.get_small_blind_player().ante(self.min_bet/2)
        self.pot += self.get_big_blind_player().ante(self.min_bet)
#        self.current_bet = self.min_bet

    def init_betters(self):
        self.button = (self.button)%len(self.players)
        self.get_blinds()
        self.game_stage = None

    @property
    def current_betters(self):
        if self._current_betters is None:
            try:
                current_better = (self.button+3)%len(self.players)
            except ZeroDivisionError:
                current_better = self.button
            self._current_betters = deque([])
            for player in self.players:
                if not player.betting_state == "fold":
                    self._current_betters.append(player)
            self._current_betters.rotate(-current_better)
        return self._current_betters

    def move_button(self):
        self.button = (self.button+1)%len(self.players)
        self._current_betters = None

    def new_round(self):
        first_round = True
        for p in self.players:
            if p.betting_state:
                first_round = False
            p.betting_state = None
            p.betting_hist = [[]]
        if first_round == False:
            self.move_button()
        logging.debug("Return cards")
        self.community_cards = []
        self.player_return_cards()
        self.card_pack.resetPack()
        logging.debug("Removing losers")
        self.remove_losers()
        logging.debug("Shuffling cards")
        self.card_pack.shuffle()
        if len(self.players)==1:
            print("*"*10)
            print("%s" % self.players[0].name)
            print("%s has WON the game" % self.players[0].name)
            print("*"*10)
            return False
        assert self.pot==0
        self.init_betters()
        logging.debug("Dealing cards")
        self.deal_cards()
        self.betting_stage = "betting"
        self.news.append("New round")
        return True

    def deal_flop(self):
        """
        Deal three community cards
        """
        self.community_cards.extend(self.card_pack.getCards(3))

    def get_player_chips(self):
        return {player.name:player.chips for player in self.players}

    def get_game_state(self, user=None, debug=False):
        self.game_state = {}
        self.game_state['game_stage'] = self.game_stage
        self.game_state['pot'] = self.pot
        self.update_betting_state()
        self.game_state['player_chips'] = self.get_player_chips()
        self.game_state['news']   = list(self.news)
        self.game_state['community_cards'] = [str(c) for c in self.community_cards]
        try:
            self.game_state['button'] = self.players[self.button].name
        except IndexError:
            logging.warning("No players")
            return self.game_state
        self.game_state['blind_small'] = self.get_small_blind_player().name
        self.game_state['blind_big']   = self.get_big_blind_player().name
        self.game_state['current_bet'] = self.current_bet
        #players
        self.game_state['players'] = OrderedDict({})
        self.game_state['player_chips'] = {}
        for p in self.players:
            # self.game_state['players'][p.name] = p.interface
            self.game_state['players'][p.name] = p.interface.__class__.__name__
            self.game_state['player_chips'][p.name] = p.chips
        #
        if user:
            self.game_state['player_cards'] = [str(c) for c in self.get_player_name_map()[user].cards]
        ####hidden state
        if debug:
            self.game_state['cards'] = self._get_cards_state()
        return self.game_state

    def set_game_state(self, new_state):
        self._current_betters = None
        self.game_state = {}
        self.game_stage = new_state.get('game_stage', None)
        self.community_cards = copy(new_state.get('community_cards', []))
        self.set_players(new_state['players'])
        for p in self.players:
            chips = new_state['player_chips'][p.name]
            p.chips = chips
        self.set_button(new_state)
        self.pot = new_state.get('pot',0)
        if 'betting' in new_state:
            for player in self.players:
                #happy if it is none
                player.betting_state = new_state['betting'].get(player.name)
                logging.debug(new_state['betting'].get(player.name))
        if 'betting_history' in new_state:
            betting_hist = dict(new_state['betting_history'])
            for player in self.players:
                bh = betting_hist.get(player.name, [[]])
                if len(bh)<1:
                    bh = [[]]
                player.betting_hist = bh
        if 'cards' in new_state:
            self._update_hands(new_state)
        self.update_betting_stage()
        logging.debug(self.current_betters)

    def _get_all_last_bet(self):
        res = []
        for bh in  (p.betting_hist for p in self.current_betters):
            last_bet = None
            if bh:
                try:
                    last_bet = bh[-1][-1][0]
                except IndexError:
                    last_bet = None
            res.append(last_bet)
        return res


    def update_betting_stage(self):
        if all(bet == "check" for bet in self._get_all_last_bet()):
            self.betting_stage = 'finished'
        else:
            self.betting_stage = 'betting'

    def _update_hands(self, new_state):
        player_map = self.get_player_name_map()
        for name in new_state['cards']:
            hand = []
            assert len(new_state['cards'][name])==2 or len(new_state['cards'][name])==0
            for c in new_state['cards'][name]:
                player_map[name].cards.append(self.card_pack.pickCard(c))

    def set_button(self, new_state):
        try:
            button_player = new_state['button']
        except IndexError:
            return
        for i, p in enumerate(self.players):
            if p.name==button_player:
                self.button = i
                break

    def new_betting_turn(self):
        for player in self.current_betters:
            player.betting_hist.append([])
        #self.current_bet = 0

    def iter_step(self, user=None, debug=False):
        while True:
            self.update_betting_stage()
            self.game_state = {}
            if self.game_stage is None:
                self.game_stage = "pre-flop"
                yield self.get_game_state(user, debug)
            elif self.game_stage== "pre-flop" and self.betting_stage == "finished":
                self.deal_flop()
                self.game_stage = "flop"
                self.new_betting_turn()
            elif self.game_stage== "flop" and self.betting_stage == "finished":
                #"the turn"
                self.community_cards.extend(self.card_pack.getCards(1))
                self.game_stage = "turn"
                self.new_betting_turn()
            elif self.game_stage== "turn" and self.betting_stage == "finished":
                #"the river"
                self.community_cards.extend(self.card_pack.getCards(1))
                self.game_stage = "river"
                self.new_betting_turn()
            elif self.game_stage== "river"  and self.betting_stage == "finished":
                self.game_stage = "payout"
            #deal cards
            if self.game_stage == "pre-flop" and all([p.cards==[] for p in self.players]):
                self.deal_cards()
            #betting
            logging.debug(self.game_stage)
            if self.game_stage!="payout":
                self.betting_round()
                self.update_betting_state()
            if len(self.current_betters)==1:
                self.game_stage = "payout"
            ####
            if self.game_stage=="payout":
                #TODO: clear betting history
                #####winner
                winners = self.get_winners()
                #TODO:warning hands returned here
                print("winners=", winners)
                #self.game_state['winners'] = {}
                #for name in winners:
                    #self.game_state['winners'][name] = [str(c) for c in winners[name]]
                #####
                self.pay_winners(winners)
                yield self.get_game_state(user, debug)
                return
            else:
                yield self.get_game_state(user, debug)

    @property
    def current_bet(self):
        betters_hist = []
        for player in self.current_betters:
            betters_hist.append(player.betting_hist)
        #any raises
        raises = []
        for h in betters_hist:
            try:
                if h[-1][-1][0]=='raise':
                    raises.append(h[-1][-1][-1])
            except IndexError:
                pass
        if raises:
            return max(raises)
        #any all-ins

        allin = []
        for h in betters_hist:
            try:
                if h[-1][-1][0]=='all-in':
                    allin.append(h[-1][-1][-1])
            except IndexError:
                pass
        if allin:
            return max(allin)
        #any antes
        antes = []
        for h in betters_hist:
            try:
                if h[-1][-1][0]=='ante':
                    antes.append(h[-1][-1][-1])
            except IndexError:
                pass
        if antes:
            return max(antes)
        return 0

    def betting_round(self):
        cur_better = self.current_betters[0]
        betting_options = self.get_current_betting_options()
        if betting_options:#all-in
            this_bet = cur_better.bet(betting_options, self.get_game_state(user=cur_better.name))
            self.pot = self.pot + this_bet[1]
            self.news.append("%s %s" % (cur_better.name, this_bet))
            logging.debug("current_betters->%s",self.current_betters)
        self.current_betters.rotate(-1)
        logging.debug("current_betters rot1->%s",self.current_betters)
        if self.current_betters[-1].betting_state == "fold":
            self.current_betters.pop()
        if len(self.current_betters)==1:
            self.betting_stage = "finished"
        elif all([p.betting_state=="bet" for p in self.current_betters]):
            self.betting_stage = "finished"

    def get_current_betting_options(self):
        cur_better = self.current_betters[0]
        if cur_better.betting_state in ['folded', 'all-in']:
            return []
        #if cur_better.betting_state=='betted' and self.betting_stage!='raising':
        #    return []
        opts = []
        opts.append(("fold", 0))
        opts.append(("all-in", cur_better.chips))
        current_bet = self.current_bet
        try:
            if cur_better.betting_hist[-1][-1][0]=='ante':
                current_bet = current_bet - cur_better.betting_hist[-1][-1][-1]
                if current_bet<0:
                    current_bet = 0
        except IndexError:
            pass
        if current_bet>=cur_better.chips:
            return opts
        else:
            opts.append(('check', current_bet))
            if current_bet==0:
                raise_amount = self.min_bet
            else:
                raise_amount = current_bet + current_bet
            if raise_amount <= cur_better.chips:
                opts.append(('raise', raise_amount))
            return opts

    def update_betting_history(self):
        def bet_hist(player):
            logging.debug(player.name)
            logging.debug(player.betting_hist)
            return (player.name, player.betting_hist)
        non_betters = []
        for player in self.players:
            if not player in self.current_betters:
                non_betters.append(bet_hist(player))
        logging.debug("Non betters=%s", non_betters)
        res = []
        for player in self.current_betters:
            res.append(bet_hist(player))
        res.extend(non_betters)
        self.game_state['betting_history'] = res
        return res


    def update_betting_state(self):
        self.game_state['current_bet'] = self.current_bet
        self.game_state['betting'] = {}
        for player in self.players:
            self.game_state['betting'][player.name] = player.betting_state
        self.update_betting_history()

        return self.game_state

    def pay_winners(self, winner_names):
        winners = [player for player in self.players if player.name in winner_names]
        #TODO: what happens if pot split is less then whole number
        num_winners = len(winners)
        winnings = int(floor(self.pot / num_winners))
        for winner in winners:
            self.news.append("%s won %d"%(winner.name, winnings))
            winner.chips += winnings
        self.pot = 0

    def get_player_name_map(self):
        return {player.name:player for player in self.players}

    def get_winners(self):
        #TODO: should be hidden from end user
        print(len(self.current_betters))
        if len(self.current_betters)==1:
            return {self.current_betters[0].name:self.current_betters[0].cards}
        else:
            print(self.get_player_cards_maps())
            return hands.get_best_hands_from_map(self.get_player_cards_maps())

    def player_return_cards(self):
        for player in self.players:
            player.cards = []

    def get_player_cards_maps(self):
        #should be hidden from end user
        res = {}
        for player in self.current_betters:
            these_cards = player.cards[:]
            these_cards.extend(self.community_cards)
            res[player.name] = these_cards
        return res

    def _get_cards_state(self):
        res = {}
        for player in self.players:
            res[player.name] = [str(c) for c in player.cards]
        return res

    def deal_cards(self):
        for _ in xrange(2):
            for player in self.players:
                player.cards.extend(self.card_pack.getCards(1))

    def get_small_blind_player(self):
        try:
            return self.players[(self.button+1)%len(self.players)]
        except ZeroDivisionError:
            return

    def get_big_blind_player(self):
        return self.players[(self.button+2)%len(self.players)]
