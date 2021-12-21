import hashlib
import hmac
import secrets
import sys
from prettytable import PrettyTable
from random import choice
from sys import argv


class GameRules:

    def __init__(self, input_data):
        self.moves = input_data[1:]
        self.game_status = False
        self.losing_moves = []

    def check_input_data(self):
        if len(self.moves) < 3 or len(self.moves) % 2 == 0:
            print("Input data must be > 2 and be odd. Please try again like 'rock scissors paper'.")
        else:
            print("OK, let's play!")
            self.game_status = True

    def show_available_moves(self):
        print("Available moves:")
        for i in self.moves:
            print(str(self.moves.index(i) + 1) + " - " + i)
        print("0 - exit", "? - help", sep="\n")

    def find_losing_moves(self, player_move):
        self.losing_moves.clear()
        for i in range(1, int((len(self.moves) - 1) / 2) + 1):
            self.losing_moves.append(self.moves[player_move - i])


class GameHelp:

    def __init__(self):
        self.score = [0, 0, 0, 0]
        self.game_counter = 0

    def update_score(self, item):
        self.game_counter += 1
        self.score.append(self.game_counter)
        current_score = [0, 0, 0]
        current_score[item] = 1
        self.score.extend(current_score)

    def show_help(self):
        table_head = ["Game", "Draw", "Win", "Lose"]
        table_data = self.score[:]
        table = PrettyTable(table_head)
        while table_data:
            table.add_row(table_data[:4])
            table_data = table_data[4:]
        print(table)


class Security:
    def __init__(self):
        self.s_key = None
        self.hmac = None

    def generate_key(self):
        self.s_key = secrets.token_hex(32)

    def calc_hmac(self, comp_move):
        self.hmac = hmac.new(self.s_key.encode(), comp_move.encode(), hashlib.sha256).hexdigest()
        print(f"HMAC: {self.hmac}")


class Game(GameRules, GameHelp, Security):
    def __init__(self, input_data):
        GameRules.__init__(self, input_data)
        GameHelp.__init__(self)
        Security.__init__(self)
        self.player_move = None
        self.comp_move = None

    def get_player_move(self):
        self.player_move = input("Please choice your move: ")

    def analyze_player_move(self):
        self.player_move = int(self.player_move) - 1
        print(f"Your move - {self.moves[self.player_move]}")
        self.find_losing_moves(self.player_move)

    def get_comp_move(self):
        self.comp_move = choice(self.moves)

    def show_comp_move(self):
        print(f"Computer move - {self.comp_move}")

    def find_winner(self):
        if self.moves[self.player_move] == self.comp_move:
            print("DRAW")
            self.update_score(0)
        elif self.comp_move in self.losing_moves:
            print("YOU WIN!")
            self.update_score(1)
        else:
            print("YOU LOSE!")
            self.update_score(2)


if __name__ == '__main__':
    game = Game(argv)
    game.check_input_data()
    if game.game_status:
        while True:
            print("-" * 60)
            game.generate_key()
            game.get_comp_move()
            game.calc_hmac(game.comp_move)
            game.show_available_moves()
            game.get_player_move()
            try:
                if game.player_move == "0":
                    sys.exit()
                elif game.player_move == "?":
                    game.show_help()
                else:
                    game.analyze_player_move()
                    game.show_comp_move()
                    game.find_winner()
                    print(f"HMAC key: {game.s_key}")
            except TypeError:
                continue
            except IndexError:
                continue
            except ValueError:
                continue
