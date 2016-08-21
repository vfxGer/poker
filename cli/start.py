#!/usr/bin/env python
__created__ = '10/10/13'
import sys
from pprint import pprint
import cli.game as game

def main():
    my_game = game.CLI_Game()
    my_game.init_players()
    while True:
        cont = my_game.new_round()
        if cont==False:
            print "Starting new Game"
            my_game = game.CLI_Game()
            my_game.init_players()
            my_game.new_round()
        for game_state in my_game.iter_step('Ger', debug=True):
            pprint(game_state)
            ans = raw_input("Press Q to quit: \n")
            if ans:
                if ans.lower()[0]=="q":
                    sys.exit(0)

if __name__=="__main__":
    main()
