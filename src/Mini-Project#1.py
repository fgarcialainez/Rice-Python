# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions

def number_to_name(number):
    # fill in your code below
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    name = None
    
    if number == 0:
        name = 'rock'
    elif number == 1:
        name = 'Spock'
    elif number == 2:
        name = 'paper'
    elif number == 3:
        name = 'lizard' 
    elif number == 4:
        name = 'scissors'
    else:
        print 'The number is not the in the correct range'
        
    return name;

    
def name_to_number(name):
    # fill in your code below

    # convert name to number using if/elif/else
    # don't forget to return the result!
    number = None
    
    if name == 'rock':
        number = 0
    elif name == 'Spock':
        number = 1
    elif name == 'paper':
        number = 2
    elif name == 'lizard':
        number = 3 
    elif name == 'scissors':
        number = 4
    else:
        print 'The name does not match any of the five correct input strings'
        
    return number;


def rpsls(player_guess): 
    # fill in your code below

    # convert player_guess to player_number using name_to_number
    player_number = name_to_number(player_guess)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)
    
    # compute difference of player_number and comp_number modulo five
    difference = (player_number - comp_number) % 5
    
    # use if/elif/else to determine winner
    result = None
    
    if difference == 0:
        result = 'Player and computer tie!'
    elif difference <= 2:
        result = 'Player wins!'
    elif difference > 2:
        result = 'Computer wins!'

    # convert comp_number to name using number_to_name
    computer_guess = number_to_name(comp_number)
    
    # print results
    print 'Player chooses ' + player_guess
    print 'Computer chooses ' + computer_guess
    print result
    print ''
    
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


