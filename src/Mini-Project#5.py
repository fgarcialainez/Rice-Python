# implementation of card game - Memory

import simplegui
import random

# helper function to calculate the card index for a position
def calculate_card_index(pos):
    return pos[0] // 50

# helper function to initialize globals
def init():
    global cards_list, exposed_list, state, first_card_exposed, second_card_exposed, moves
    
    # initialize game state
    state = 0
    first_card_exposed = -1
    second_card_exposed = -1
    moves = 0
    
    # initialize cards list and shuffle the content
    cards_list = range(0, 8) + range(0, 8)
    random.shuffle(cards_list)
    
    # initialize exposed list
    new_exposed_list = []
    
    for i in range(len(cards_list)):
        new_exposed_list.append(False)
        
    exposed_list = new_exposed_list
     
# define event handlers
def mouseclick(pos):
    global cards_list, exposed_list, state, first_card_exposed, second_card_exposed, moves
    
    # add game state logic here
    clicked_card = calculate_card_index(pos)
    
    # process only clicks of non exposed cards
    if exposed_list[clicked_card] == False:
        # check the state of the game
        if state == 0:
            state = 1
            first_card_exposed = clicked_card
        elif state == 1:
            moves += 1
            state = 2
            second_card_exposed = clicked_card
        elif state == 2:
            state = 1
            # check if the two cards exposed are the same, else reset
            if cards_list[first_card_exposed] != cards_list[second_card_exposed]:
                exposed_list[first_card_exposed] = False
                exposed_list[second_card_exposed] = False
            
            first_card_exposed = clicked_card

        # always expose the clicked card        
        exposed_list[clicked_card] = True 
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards_list, exposed_list
    
    # draw the cards list
    for i in range(len(cards_list)):
        if exposed_list[i] == True:
            canvas.draw_polygon([[(i * 50), 0], [(i + 1) * 50, 0], [(i + 1) * 50, 100], [i * 50, 100]], 1, "Red", "Black")
            canvas.draw_text(str(cards_list[i]), [(i * 50) + 14, 65], 45, "White")
        else:
            canvas.draw_polygon([[(i * 50), 0], [(i + 1) * 50, 0], [(i + 1) * 50, 100], [i * 50, 100]], 1, "Red", "Green")

    # draw the canvas border
    canvas.draw_polygon([[0, 0], [800, 0], [800, 100], [0, 100]], 1, "Red", "Transparent")
    
    # set the number of moves
    label.set_text("Moves = " + str(moves))   

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init, 75)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric