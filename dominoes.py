import itertools
import random
import sys


class Domino:

    # Create domino set and initialize variables.
    def __init__(self):
        self.dominoes = list(map(list, itertools.combinations_with_replacement([0, 1, 2, 3, 4, 5, 6], 2)))
        self. player_d = []
        self.cpu_d = []
        self.snake = []
        self.status = ''
        self.player_range = []
        self.cpu_range = [0]
        self.deal()

    # Shuffle and randomly select cpu/player dominoes.
    # After each player has been dealt 7 dominoes the remaining 14 dominoes are placed in stock.
    def deal(self):
        random.shuffle(self.dominoes)
        for _ in range(7):
            pick = random.choice(self.dominoes)
            self.cpu_d.append(pick)
            self.dominoes.remove(pick)
            pick = random.choice(self.dominoes)
            self.player_d.append(pick)
            self.dominoes.remove(pick)
        self.first_move()

    # First move is player with highest double domino(Domino snake).
    # Domino snake is automatically the first played piece.
    # Game status will be displayed after first move is decided..
    # If no doubles in either hand deal() will repeat until a first move can be made.
    def first_move(self):
        # Initialize local variables
        player_max = -1
        player_max_idx = int()
        cpu_max = -1
        cpu_max_idx = int()

        # Find highest double domino in each hand(if exists).
        for i in range(0, 7):
            if self.cpu_d[i][0] == self.cpu_d[i][1] and self.cpu_d[i][0] > cpu_max:
                cpu_max = self.cpu_d[i][0]
                cpu_max_idx = i
            if self.player_d[i][0] == self.player_d[i][1] and self.player_d[i][0] > player_max:
                player_max = self.player_d[i][0]
                player_max_idx = i

        # No double dominoes in either hand. Re-deal.
        if cpu_max == -1 and player_max == -1:
            self.__init__()
        if cpu_max > player_max:
            self.status = 'player'
            self.snake.append(self.cpu_d[cpu_max_idx])
            self.cpu_d.remove(self.cpu_d[cpu_max_idx])
        else:
            self.status = 'computer'
            self.snake.append(self.player_d[player_max_idx])
            self.player_d.remove(self.player_d[player_max_idx])
        self.current_state()

    # Displays current game state.
    def current_state(self):
        print('=' * 70)
        print(f'Stock size: {len(self.dominoes)}')
        print(f'Computer pieces: {len(self.cpu_d)}\n')
        snake_string = ''
        # Show full snake only if there are 6 tiles or less in snake.
        if len(self.snake) < 7:
            for domino in self.snake:
                snake_string += str(domino)
        else:
            # Show only first three tiles and last three tiles of snake separated by ...
            snake = list(str(x) for x in self.snake)
            snake_string += ''.join(snake[0:3]) + '...' + ''.join(snake[-3:])
        print(f'\n{snake_string}')
        print('\nYour pieces:')
        self.player_range = [0]
        # Calculate player move range and print player hand.
        for idx, piece in enumerate(self.player_d, 1):
            self.player_range.insert(0, -idx)
            self.player_range.append(idx)
            print(f'{idx}: {piece}')
        self.cpu_range = [0]
        # calculate computer move range.
        for idx, piece in enumerate(self.cpu_d, 1):
            self.cpu_range.insert(0, -idx)
            self.cpu_range.append(idx)
        self.check_win()
        if self.status == 'player':
            print("Status: It's your turn to make a move. Enter your command.")
            self.player_move()
        else:
            print("Status: Computer is about to make a move. Press Enter to continue...")
            self.cpu_move_ai()

    # Computer weights moves by frequency of appearance of numbers in hand and snake.
    # Computer will only pass if no available moves are valid.
    def cpu_move_ai(self):
        move = input()
        count_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        move_dict = {}
        sorted_moves = {}
        for item in self.cpu_d:
            count_dict[item[0]] += 1
            count_dict[item[1]] += 1
        for item in self.snake:
            count_dict[item[0]] += 1
            count_dict[item[1]] += 1
        count_list = []
        for item in self.cpu_d:
            count_list.append(count_dict[item[0]] + count_dict[item[1]])
        for k, v in enumerate(count_list):
            move_dict[k] = v
        sorted_keys = sorted(move_dict, key=move_dict.get, reverse=True)
        for k in sorted_keys:
            sorted_moves[k] = move_dict[k]
        marker = len(self.cpu_d)
        for item in sorted_moves:
            move = item
            if self.validate_move(move, direction='left') is True:
                if self.cpu_d[move][1] != self.snake[0][0]:
                    self.cpu_d[move] = self.cpu_d[move][::-1]
                self.snake.insert(0, self.cpu_d[move])
                self.cpu_d.remove(self.cpu_d[move])
                break
            if self.validate_move(move, direction='right') is True:
                if self.cpu_d[move][0] != self.snake[-1][1]:
                    self.cpu_d[move] = self.cpu_d[move][::-1]
                self.snake.append(self.cpu_d[move])
                self.cpu_d.remove(self.cpu_d[move])
                break
        if marker == len(self.cpu_d):
            if len(self.dominoes) == 0:
                pass
            else:
                pick = random.choice(self.dominoes)
                self.cpu_d.append(pick)
                self.dominoes.remove(pick)
        self.status = 'player'
        self.current_state()

    # Entering a move index will attempt to pace the domino to the right of the snake.
    # entering a negative index will attempt to place the domino to the left of the snake.
    # entering 0 will draw a tile from stock. If no tiles are left in stock the turn will pass.
    # If alpha characters are entered or move index entered is out of range an error message will display
    # and user must input a valid move.
    def player_move(self):
        while True:
            try:
                move = int(input())
                if move not in self.player_range:
                    print("Invalid input. Please try again.")
                else:
                    if move == 0:
                        if len(self.dominoes) == 0:
                            break
                        pick = random.choice(self.dominoes)
                        self.player_d.append(pick)
                        self.dominoes.remove(pick)
                        break
                    if move < 0:
                        direction = 'left'
                        move = (move * -1) - 1
                        if self.validate_move(move, direction) is True:
                            if self.player_d[move][1] != self.snake[0][0]:
                                self.player_d[move] = self.player_d[move][::-1]
                            self.snake.insert(0, self.player_d[move])
                            self.player_d.remove(self.player_d[move])
                            break
                    if move > 0:
                        direction = 'right'
                        move = move - 1
                        if self.validate_move(move, direction) is True:
                            if self.player_d[move][0] != self.snake[-1][1]:
                                self.player_d[move] = self.player_d[move][::-1]
                            self.snake.append(self.player_d[move])
                            self.player_d.remove(self.player_d[move])
                            break
                    print("Illegal move. Please try again.")
            except ValueError:
                print('Invalid input. Please try again.')
        self.status = 'computer'
        self.current_state()

    # Checks for winner or draw
    # The first player to run out of tiles is the winner.
    # Draw will be called if the end numbers match and appear 8 times throughout the snake.
    def check_win(self):
        if len(self.cpu_d) == 0:
            print("\nStatus: The game is over. The computer won!")
            sys.exit()
        elif len(self.player_d) == 0:
            print("\nStatus: The game is over. You won!")
            sys.exit()
        elif self.snake[0][0] == self.snake[-1][1]:
            count = 0
            for item in self.snake:
                if item[0] == self.snake[0][0]:
                    count += 1
                if item[1] == self.snake[0][0]:
                    count += 1
            if count == 8:
                print("\nStatus: The game is over. It's a draw!")
                sys.exit()
        else:
            return

    # Checks legality of selected move.
    def validate_move(self, move, direction):
        if self.status == 'computer':
            if direction == 'left':
                if self.cpu_d[move][0] == self.snake[0][0] or self.cpu_d[move][1] == self.snake[0][0]:
                    return True
                else:
                    return False
            if direction == 'right':
                if self.cpu_d[move][0] == self.snake[-1][1] or self.cpu_d[move][1] == self.snake[-1][1]:
                    return True
                else:
                    return False
        else:
            if direction == 'left':
                if self.player_d[move][0] == self.snake[0][0] or self.player_d[move][1] == self.snake[0][0]:
                    return True
                else:
                    return False
            else:
                if self.player_d[move][0] == self.snake[-1][1] or self.player_d[move][1] == self.snake[-1][1]:
                    return True
                else:
                    return False


if __name__ == "__main__":
    game = Domino()
