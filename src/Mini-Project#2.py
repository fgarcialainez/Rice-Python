# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

# initialize global variables used in your code
num_range = 100
num_remaining_guesses = 7
secret_number = 0


# initialize the game
def init_game():
    global num_range, num_remaining_guesses, secret_number
    
    #generate secret number
    secret_number = random.randrange(0, num_range)
    
    new_game_message = None;
    
    if num_range == 100:
        num_remaining_guesses = 7
        new_game_message = "New game. Range is from 0 to 100"     
    elif num_range == 1000:
        num_remaining_guesses = 10
        new_game_message = "New game. Range is from 0 to 1000"
      
    print new_game_message
    print "Number of remaining guesses is " + str(num_remaining_guesses)
    print ""
    
# define event handlers for control panel
    
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    num_range = 100
    init_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    num_range = 1000
    init_game()
    
def input_guess(guess):
    # main game logic goes here	
    
    #check if the input is a int
    if guess.isdigit():
        global num_remaining_guesses, secret_number
    
        #decrement remaining guesses
        num_remaining_guesses -= 1
    
        #convert the input to an int
        guess_number = int(guess)
    
        #print the result
        print "Guess was " + str(guess_number)
        print "Number of remaining guesses is " + str(num_remaining_guesses)
    
        if guess_number == secret_number:
            print "Correct!"
            print ""
            init_game()
        else:
            if guess_number < secret_number:
                print "Higher!"
            elif guess_number > secret_number:
                print "Lower!"
        
            if num_remaining_guesses == 0:
                print "You lost the game!"
                print ""
                init_game()     
            else:
                print ""
    else:
        print "The entered guess is not a valid integer"
        print "";
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

init_game();

# start frame
frame.start();

# always remember to check your completed program against the grading rubric
