#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'gerardk'
__created__ = '29/10/13'

import logging
from pprint import pprint
import sys

from poker_core.players import PlayerInterface


class AIPlayerInterface(PlayerInterface):
    def __init__(self):
        PlayerInterface.__init__(self)

    def bet(self, betting_options, game_state=None):
        if ('check', 0) in betting_options:
            return ('check', 0)
        else:
            return ('fold', 0)


class CLIPlayer(PlayerInterface):
    opt_map = {'f':'fold',
               'a':'all-in',
               'c':'check',
               'r':'raise'
               }

    def __init__(self):
        PlayerInterface.__init__(self)

    #TODO: could be static
    def prompt_for_cash_amount(self, min_cash, max_cash):
        def is_correct(res):
            if not res:
                logging.debug("Not a value entered")
                return False
            res = res.strip()
            try:
                res = int(res)
            except ValueError:
                logging.debug("Not a number entered")
                return False
            return min_cash<=res and res<=max_cash
        res = None
        prompt_message = "Please enter a cash amount between 40000 and 100000: "
        while not is_correct(res):
            res = raw_input(prompt_message)
        res = int(res)
        return res

    def bet(self, betting_options, game_state=None):
        pprint(game_state)
        def in_options(opt):
            return opt in [o for o,_ in betting_options]
        def get_amount(opt):
            return {o:n for o,n in betting_options}[opt]
        #example [('fold', 0), ('all-in', 50000), ('check', 20000), ('raise', 40000)]
        print "Please select a betting option"
        prompt = ""
        if in_options('fold'):
            prompt += "f: Fold, "
        if in_options('check'):
            prompt += "c: Check %d, "% get_amount('check')
        if in_options('raise'):
            prompt += "r: Raise %d+, "% get_amount('raise')
        if in_options('all-in'):
            prompt += "a: All-in %d, "% get_amount('all-in')
        prompt = prompt.strip()
        prompt = prompt.strip(",")
        prompt += "\n"
        res = raw_input(prompt)
        res = res.lower()
        res = res.strip()
        while not res in self.opt_map and res!='q':
            print "Bad value '%s', please choose again" % res
            res = raw_input(prompt)
            res = res.lower()
            res = res.strip()
        if res.lower() == 'q':
            sys.exit()
        res = self.opt_map[res]
        if res=='raise':
            return res, self.prompt_for_cash_amount(get_amount(res), get_amount('all-in'))
        else:
            return res, get_amount(res)

