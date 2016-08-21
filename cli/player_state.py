#!/usr/bin/env python
# encoding: utf-8
"""
Created by gerardk on 04/01/2014.
"""
import poker_core.player_state

class CLI_Player_State(poker_core.player_state.Player_State):
    def __init__(self, name, interface):
        super(CLI_Player_State, self).__init__(name, interface)