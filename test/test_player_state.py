#!/usr/bin/env python
# encoding: utf-8
"""
Created by gerardk on 13/01/2014.
"""

import unittest

import json

import poker_core.player_state
from cli.players import AIPlayerInterface

class Test_Case(unittest.TestCase):
    def test_jsonify(self):
        p = poker_core.player_state.Player_State('Gerard', AIPlayerInterface())
        p.get_dict()

if __name__ == '__main__':
    unittest.main()
