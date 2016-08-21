#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'gerardk'
__created__ = '06/11/13'

import unittest

import mock

from cli.players import CLIPlayer

class Test_CLI_Player(unittest.TestCase):
    @mock.patch("__builtin__.raw_input")
    def test_cli_player_bet_fold(self, mock_raw_input):
        mock_raw_input.return_value = "F"
        player = CLIPlayer()
        res = player.bet([('fold', 0), ('all-in', 50000), ('check', 20000), ('raise', 40000)])
        mock_raw_input.assert_called_once_with("f: Fold, c: Check 20000, r: Raise 40000+, a: All-in 50000\n")
        self.assertEqual(res, ('fold', 0))

    @mock.patch("__builtin__.raw_input")
    def test_cli_player_bet_all_in(self, mock_raw_input):
        mock_raw_input.return_value = "A"
        player = CLIPlayer()
        res = player.bet([('fold', 0), ('all-in', 50000), ('check', 20000), ('raise', 40000)])
        mock_raw_input.assert_called_once_with("f: Fold, c: Check 20000, r: Raise 40000+, a: All-in 50000\n")
        self.assertEqual(res, ('all-in', 50000))

    @mock.patch("__builtin__.raw_input")
    def test_cli_player_bet_check(self, mock_raw_input):
        mock_raw_input.return_value = "C"
        player = CLIPlayer()
        res = player.bet([('fold', 0), ('all-in', 50000), ('check', 20000), ('raise', 40000)])
        self.assertEqual(res, ('check', 20000))

    @mock.patch.object(CLIPlayer, "prompt_for_cash_amount")
    @mock.patch("__builtin__.raw_input")
    def test_cli_player_bet_raise(self, mock_raw_input, mock_prompt_cash):
        mock_prompt_cash.return_value = 80000
        mock_raw_input.return_value = 'r'
        player = CLIPlayer()
        res = player.bet([('fold', 0), ('all-in', 100000), ('check', 20000), ('raise', 40000)])
        self.assertEqual(res, ('raise', 80000))
        mock_prompt_cash.assert_called_once_with(40000, 100000)

    @mock.patch("__builtin__.raw_input")
    def test_prompt_for_cash_amount_correct(self, mock_raw_input):
        mock_raw_input.return_value = "80000"
        player = CLIPlayer()
        res = player.prompt_for_cash_amount(40000, 100000)
        mock_raw_input.assert_called_once_with("Please enter a cash amount between 40000 and 100000: ")
        self.assertEqual(res, 80000)

    @mock.patch("__builtin__.raw_input")
    def test_prompt_for_cash_amount(self, mock_raw_input):
        def side_effect(*args):
            def second_call(*args):
                return '80000'
            mock_raw_input.side_effect = second_call
            return "what"
        mock_raw_input.side_effect = side_effect

        player = CLIPlayer()
        res = player.prompt_for_cash_amount(40000, 100000)
        mock_raw_input.assert_called_with("Please enter a cash amount between 40000 and 100000: ")
        self.assertEqual(res, 80000)
        self.assertEqual(mock_raw_input.call_count, 2)

if __name__ == '__main__':
    unittest.main()
