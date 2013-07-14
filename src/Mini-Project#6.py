# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
player_msg = ""
deal_result = ""
score_dealer = 0
score_player = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create a Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        hand_str = '#Hand contains '
   
        for card in self.cards:
            hand_str += (str(card) + ' ')
            
        return hand_str
        
    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)
        
    def get_value(self):
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        contains_ace = False
      
        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
            
            if(card.get_rank() == 'A'):
                contains_ace = True
        
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust        
        if contains_ace and hand_value + 10 <= 21:
            hand_value += 10
            
        return hand_value
            
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 90
            
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
 
    def shuffle(self):
        # add cards back to deck and shuffle
        # use random.shuffle() to shuffle the deck
        self.cards = []
        
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
        
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        if len(self.cards) > 0:
            return self.cards.pop(len(self.cards) - 1)
        else:
            return None
    
    def __str__(self):
        # return a string representing the deck        
        deck_str = '#Deck contains '
   
        for card in self.cards:
            deck_str += (str(card) + ' ')
            
        return deck_str

#define event handlers for buttons
def deal():
    global score_dealer, player_msg, deal_result, in_play, deck, player_hand, dealer_hand

    if in_play:
        deal_result = "You lose. You pressed Deal during a round."
        score_dealer += 1
    else:
        deal_result = ""
    
    # initialize and shuffle the deck
    deck = Deck()
    deck.shuffle()
    
    # create player and dealer hand
    player_hand = Hand()
    dealer_hand = Hand()
    
    # transfer two cards from the deck to each hand
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    player_msg = "Hit or stand?"
    in_play = True

def hit():
    global player_msg, deal_result, in_play, deck, player_hand, score_dealer
    
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
    
        # if busted, assign a message to deal_result, update in_play and scores
        if player_hand.get_value() > 21:
            score_dealer += 1
            in_play = False
            deal_result = "You went bust and lose."
            player_msg = "New deal?"
        else:
            #reset message
            deal_result = ""
        
def stand():
    global player_msg, deal_result, in_play, deck, dealer_hand, score_dealer, score_player
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(deck.deal_card()) 
            
        # assign a message to deal_result, update in_play and score
        if dealer_hand.get_value() > 21:
            deal_result = "Dealer went bust and you win."
            score_player += 1
        else:
            if dealer_hand.get_value() >= player_hand.get_value(): 
                deal_result = "You lose."
                score_dealer += 1
            else:
                deal_result = "You win."
                score_player += 1
                
        in_play = False
        player_msg = "New deal?"

# draw handler    
def draw(canvas):
    global player_msg, deal_result, in_play, player_hand, dealer_hand, score_dealer, score_player
    
    canvas.draw_text("Blackjack", (200, 60), 34, "Navy")
    
    canvas.draw_text(deal_result, (50, 120), 24, "Maroon")
    
    canvas.draw_text("Dealer (Score: " + str(score_dealer) + ")", (50, 178), 24, "Black")
    
    canvas.draw_text("Player (Score: " + str(score_player) + ")", (50, 378), 24, "Black")
    canvas.draw_text(player_msg, (285, 378), 24, "Black")
    
    dealer_hand.draw(canvas, [50, 200])
    player_hand.draw(canvas, [50, 400])   
    
    # draw back of a card to cover the first card of the dealer hand
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [51 + CARD_BACK_CENTER[0], 201 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 500, 550)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# start a new deal by default
deal()

# get things rolling
frame.start()


# remember to review the gradic rubric