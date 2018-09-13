import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# global variables
in_play = False
outcome = ""
msg = ""
score = 0
playerStr = "PLAYER"
dealerStr = "DEALER"

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

    def draw_back(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0] , 
                                                                pos[1] + CARD_BACK_CENTER[1] ], CARD_BACK_SIZE)

        
# define hand class
class Hand:
    def __init__(self):
        """Create Hand Object"""
        self.cards = []  # a hand is a list of Card objects

    def __str__(self):
        """ return a string representation of a hand """
        hand_str = ""
        for card in self.cards:
            hand_str = hand_str + str(card) + " " 
        return "Hand contains " + hand_str.strip() 

    def add_card(self, card):
        """ add a card object to a hand """
        self.cards.append(card)
           

    def get_value(self):
        """ count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust """
        """ compute the value of the hand, see Blackjack video """
        points = 0
        hasAce = False
        for card in self.cards:
            rank = card.get_rank()
            points += VALUES[rank]
            if rank == 'A':
                hasAce = True
        
        if hasAce and points < 12:
            points += 10
           
        return points
   
    def draw(self, canvas, pos):
        """ draw a hand on the canvas, use the draw method for cards """
        for card in self.cards:
            pos[0] = pos[0] + CARD_SIZE[0] + 25
            card.draw(canvas, pos)

        
# define deck class 
class Deck:
    def __init__(self):
        """ create a Deck object """
        self.cards = [] # a decck is a list of card objects  
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """ shuffle the deck, use random.shuffle() """
        random.shuffle(self.cards)

    def deal_card(self):
        """ deal a card object from the deck """
        return self.cards.pop()
    
    def __str__(self):
        """ return a string representing the deck """
        deck_str = ""
        for card in self.cards:
            deck_str = deck_str + str(card) + " " 
        return "Deck contains " + deck_str.strip() 
           


#define event handlers for buttons
def deal():
    global msg, outcome, score, in_play, deck, playerHand, dealerHand
    
    if in_play:
        in_play = False
        score -= 1
        deal()
    else:
        playerHand = Hand()
        dealerHand = Hand()
        deck = Deck()
        deck.shuffle()
        playerHand.add_card(deck.deal_card())        
        dealerHand.add_card(deck.deal_card())
        playerHand.add_card(deck.deal_card())
        dealerHand.add_card(deck.deal_card())
        msg = "Hit or Stand?"
        
        in_play = True


def hit():
    """ if the hand is in play, hit the player """
    """ if busted, assign a message to outcome, update in_play and score """
    global msg, outcome, score, in_play, deck, playerHand
    
    if in_play:
        if playerHand.get_value() <= 21:
            playerHand.add_card(deck.deal_card())
            if playerHand.get_value > 21:
                outcome = "You have busted!"
                score -= 1
                msg = "New Deal?"
                in_play = False
       
def stand():
    """ if hand is in play, repeatedly hit dealer until his hand has value 17 or more """
    """ assign a message to outcome, update in_play and score """
    global msg, outcome, score, in_play, deck, playerHand, dealerHand
    if in_play:
        if playerHand.get_value() > 21:
            outcome = "You already busted!"
            score -= 1
        else:     
            while dealerHand.get_value() < 17:
                dealerHand.add_card(deck.deal_card())
            if dealerHand.get_value() > 21:
                outcome = "Dealer just busted!"
                score += 1
            elif playerHand.get_value() > dealerHand.get_value():
                outcome = "You win."
                score += 1
            else:
                outcome = "You loose."
                score -= 1
        msg = "New Deal?"
        in_play = False

# draw handler    
def draw(canvas):
    
    canvas.draw_text("BLACKJACK", (150, 70), 50, "Aqua")
    canvas.draw_text(dealerStr, (36, 185), 30, "Black")
    canvas.draw_text(playerStr, (36, 385), 30, "Black")
    canvas.draw_text(outcome, (235, 385), 30, "Blue")
    canvas.draw_text(msg, (235, 185), 30, "Red")
    canvas.draw_text("Score " + str(score), (450, 115), 30, "Black")
    dealerHand.draw(canvas, [-65, 200])
    playerHand.draw(canvas, [-65, 400])
    if in_play:
        dealerHand.cards[0].draw_back(canvas, [33, 199])
 

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
 