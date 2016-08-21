#!/usr/bin/env python
# encoding: utf-8
"""
Created by gerardk on 02/01/2014.
"""
from defaults import DEFAULT_INITIAL_CHIPS


class Player_State(object):
    def __init__(self, name, interface):
        self.interface = interface
        self.name = name
        self.chips = DEFAULT_INITIAL_CHIPS
        self.cards = []
        self.betting_state = None
        self.betting_hist = [[]]

    def get_dict(self):
        return {'name':self.name}

    def __repr__(self):
        return "Player(%s, interface=%s)" % (self.name, self.interface)

    def ante(self, amount):
        if self.chips<=amount:
            #TODO: set to all-in
            #all in = True
            bet = self.chips
            self.chips = 0
            self.betting_state = 'all-in'
            self.betting_hist[-1].append((self.betting_state, bet))
            return bet
        else:
            self.chips = self.chips-amount
            self.betting_state = 'ante'
            self.betting_hist[-1].append((self.betting_state, amount))
            return amount

    def bet(self, betting_options, game_state=None):
        res = self.interface.bet(betting_options, game_state)
        self.betting_hist[-1].append(res)
        self.betting_state = res[0]
        self.chips = self.chips - res[1]
        assert self.chips>=0

        return res