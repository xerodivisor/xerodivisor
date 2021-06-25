import random


class Game:
    def __init__(self):
        self.tokens = ["X", "O"]
        self.result = None
        self.level = None
        self.choices = ["user", "easy", "medium", "hard"]
        self.players = self.menu()
        self.current_state = [[' ', ' ', ' '],
                              [' ', ' ', ' '],
                              [' ', ' ', ' ']]

        self.player_turn = 'X'
        self.main()

    # Resets game
    def initialize_game(self):
        self.players = self.menu()
        self.current_state = [[' ', ' ', ' '],
                              [' ', ' ', ' '],
                              [' ', ' ', ' ']]
        self.player_turn = 'X'

    # gameplay options (start + user|easy|medium|hard OR exit
    # 2 users can play against each other one user can play against any ai
    # or any 2 ai can play against each other
    def menu(self):
        while True:
            choice = input("Input command:").split()
            if choice[0] == "exit":
                quit()
            else:
                if len(choice) != 3 or choice[0] != "start" or (choice[1] or choice[2]) not in self.choices:
                    print("Bad parameters!")
                else:
                    return choice[1:]

    # Displays game board
    def display(self):
        print("_________")
        for i in range(0, 3):
            print(f"| {self.current_state[i][0]} {self.current_state[i][1]} {self.current_state[i][2]} |")
        print("---------")

    # Returns opponent token
    def get_opponent_token(self):
        if self.player_turn == "X":
            return "O"
        return "X"

    # Controls gameplay by looping until exit
    def main(self):
        self.display()
        while True:
            # X move
            if self.players[0] == "user":
                self.user_move()
            else:
                self.bot_move(self.players[0])
            self.display()
            self.result = self.is_end()
            # Check for end of game
            if self.result:
                self.show_result()
            # O move
            elif self.players[1] == "user":
                self.user_move()
            else:
                self.bot_move(self.players[1])
            self.display()
            # check for end of game
            self.result = self.is_end()
            if self.result:
                self.show_result()

    # Prints result and restarts game if current game has ended
    def show_result(self):
        if self.result == 'X':
            print('X wins\n')
            main()
        elif self.result == 'O':
            print('O wins\n')
            main()
        elif self.result == ' ':
            print("Draw\n")
            main()
        return

    # Human player input
    # integer coordinates between 1 and 3 inclusive separated by a space
    def user_move(self):
        valid = [0, 1, 2]
        while True:
            try:
                px, py = [int(i) - 1 for i in input("Enter the coordinates:").split()]
            except ValueError:
                print("You should enter numbers!")
            else:
                if px in valid and py in valid:
                    if self.current_state[px][py] != " ":
                        print("This cell is occupied! Choose another one!")
                    else:
                        self.current_state[px][py] = self.player_turn
                        (qx, qy) = (px, py)
                        if self.player_turn == "X":
                            self.player_turn = 'O'
                        else:
                            self.player_turn = "X"
                        break
                else:
                    print("Coordinates should be 1 to 3!")

    # Initialize ai turn
    def bot_move(self, level):
        if level == "easy":
            self.ai_easy()
        elif level == "medium":
            self.ai_medium()
        elif level == "hard":
            self.ai_hard()

    # Determines if the made move is a legal move
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return ""
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        # Vertical win
        for i in range(0, 3):
            if (self.current_state[0][i] != ' ' and
                    self.current_state[0][i] == self.current_state[1][i] and
                    self.current_state[1][i] == self.current_state[2][i]):
                return self.current_state[0][i]

        # Horizontal win
        for i in range(0, 3):
            if self.current_state[i] == ['X', 'X', 'X']:
                return 'X'
            elif self.current_state[i] == ['O', 'O', 'O']:
                return 'O'

        # Main diagonal win
        if (self.current_state[0][0] != ' ' and
                self.current_state[0][0] == self.current_state[1][1] and
                self.current_state[0][0] == self.current_state[2][2]):
            return self.current_state[0][0]

        # Second diagonal win
        if (self.current_state[0][2] != ' ' and
                self.current_state[0][2] == self.current_state[1][1] and
                self.current_state[0][2] == self.current_state[2][0]):
            return self.current_state[0][2]

        # Is whole board full?
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, we continue the game
                if self.current_state[i][j] == ' ':
                    return None

        # Draw
        return ' '

    # Makes random move
    def random(self):
        while True:
            px = random.randint(0, 2)
            py = random.randint(0, 2)
            if self.current_state[px][py] == " ":
                self.current_state[px][py] = self.player_turn
                if self.player_turn == "X":
                    self.player_turn = 'O'
                else:
                    self.player_turn = "X"
                break

    # Easy ai makes only random moves
    def ai_easy(self):
        print('Making move level "Easy"')
        self.random()

    # Medium ai will try to win or block opponent every move
    def ai_medium(self):
        print('Making move level "medium"')
        # try for win cycling through empty spaces
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == " ":
                    # Testing empty space for win
                    self.current_state[i][j] = self.player_turn
                    if self.is_end() == self.player_turn:
                        return
                    else:
                        # Set space back to empty if no win
                        self.current_state[i][j] = " "
        # try for block cycling through empty spaces
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == " ":
                    # Testing empty space for block
                    self.current_state[i][j] = self.get_opponent_token()
                    if self.is_end() == self.get_opponent_token():
                        self.current_state[i][j] = self.player_turn
                        if self.player_turn == "X":
                            self.player_turn = 'O'
                        else:
                            self.player_turn = "X"
                        return
                    else:
                        # Set space back to empty if no block
                        self.current_state[i][j] = " "
        # make random move
        self.random()

    # Hard ai cannot be beaten using minimax algorithm
    def ai_hard(self):
        print('Making move level "hard"')
        if self.player_turn == 'X':
            (m, px, py) = self.min()
            self.current_state[px][py] = 'X'
            self.player_turn = 'O'
        else:
            (m, px, py) = self.max()
            self.current_state[px][py] = 'O'
            self.player_turn = 'X'
    # Max is O
    def max(self):

        # Possible values for maxv are:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        # We're initially setting it to -2 as worse than the worst case:
        maxv = -2

        px = None
        py = None

        result = self.is_end()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win
        if result == 'X':
            # print(f'win {self.get_opponent_token()} max')
            return -1, 0, 0
        elif result == 'O':
            # print(f'win {self.get_opponent_token()} max')
            return 1, 0, 0
        elif result == ' ':
            # print('draw max')
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == ' ':
                    # On the empty field  current player makes a move and calls Min
                    # That's one branch of the game tree.
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j) = self.min()
                    # Fixing the maxv value if needed
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    # Setting back the field to empty
                    self.current_state[i][j] = ' '
        return maxv, px, py

    # Min is X
    def min(self):

        # Possible values for minv are:
        # -1 - win
        # 0  - a tie
        # 1  - loss

        # We're initially setting it to 2 as worse than the worst case:
        minv = 2

        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            # print(f'win {self.player_turn} min')
            return -1, 0, 0
        elif result == 'O':
            # print(f'win {self.get_opponent_token()} min')
            return 1, 0, 0
        elif result == ' ':
            # print('draw min')
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == ' ':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max()
                    if m < minv:
                        minv = m
                        px = i
                        py = j
                    self.current_state[i][j] = ' '

        return minv, px, py


def main():
    Game()


if __name__ == "__main__":
    main()
