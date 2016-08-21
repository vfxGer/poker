#!/usr/bin/env python
# encoding: utf-8
"""
Created by gerardk on 07/01/2014.
"""


class PlayerInterface(object):
    def __init__(self):
        pass

    def bet(self, betting_options, game_state=None):
        raise NotImplementedError("Should be defined in derived class")
