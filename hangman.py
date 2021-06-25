import random
import re
print("H A N G M A N")
word_list = ["python", "java", "kotlin", "javascript"]
set_word = random.choice(word_list)
blank = "-"
characters = len(set_word)
display_string = blank * characters


def make_guess():
    global display_string
    turns = 1
    guesses = set()
    play = ""
    while play != "play" and play != "exit":
        play = input("""Type "play" to play the game, "exit" to quit: """)
    while turns < 9:
        print()
        print(display_string)
        guess = input("Input a letter: ")
        if len(guess) != 1:
            print("You should input a single letter")
        elif not guess.islower():
            print("Please enter a lowercase English letter")
        elif guess in guesses:
            print("You've already guessed this letter")
        else:
            guesses.add(guess)
            if set_word.find(guess) == -1:
                print("That letter doesn't appear in the word")
                turns += 1
            else:
                matches = re.finditer(guess, set_word)
                positions = [match.start() for match in matches]
                display_list = []
                for ele in display_string:
                    display_list.append(ele)
                for element in positions:
                    display_list[int(element)] = guess
                display_string = ""
                for ele in display_list:
                    display_string += ele
                if set_word == display_string:
                    print("You guessed the word!\nYou survived!")
                    exit()


make_guess()
print("You lost!")
