# Blackjack

import simplegui
import random

# Globalus kintamieji

CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

in_play = False
outcome = ""
score = 0
prompt = ''
stand = False

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}



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
        

class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        s = ''
        for i in self.cards:
            s += str(i) + ' '
        return 'Hand contains ' + s
            
    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        self.value = 0
        A = False
        for i in self.cards:
            self.value += VALUES[i.get_rank()]
            if i.get_rank() in 'A':
                A = True
        if self.value <= 11 and A:
            return self.value + 10
        else:
            return self.value
   
    def draw(self, canvas, pos):
        i = 0
        for a in self.cards:
            a.draw(canvas, [pos[0] + i * 100, pos[1]])
            i += 1
 

class Deck:
    def __init__(self):
        self.deck = [Card(i, j) for i in SUITS for j in RANKS]
        
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(random.randrange(len(self.deck)))
        
    
    def __str__(self):
        s = ''
        for i in self.deck:
            s += str(i) + ' '
        return 'Deck contains ' + s           


player = Hand()
dealer = Hand()
deck = Deck()

# Mygtukai
def deal():
    global outcome, in_play, player, dealer, deck, score, prompt, stand, player_value
    if in_play == True:
        score -= 1
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
           
    in_play = True
    prompt = 'Imsi ar pasuosi?'
    outcome = ''
    stand = False
    
def hit():
    global in_play, score, outcome, player, prompt, stand
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            outcome = 'Sudegei! Dealeris laimejo!'
            in_play = False
            stand = True
            score = score - 1
            prompt = 'Zaisi dar karta?'
                    
def stand():
    global in_play, score, dealer, outcome, prompt, player, stand
    stand = True
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
            if dealer.get_value() > 21:
                break
        if dealer.get_value() > 21:
                outcome = 'Dealeris sudege! Laimejai!'
                in_play = False
                score += 1
                prompt = 'Zaisi dar karta?'
                
                
        elif 21 >= dealer.get_value() >= player.get_value():
            outcome = 'Dealeris laimejo!'
            score -= 1
            
        else:
            outcome = 'Laimejai!'
            score += 1
        in_play = False
        prompt = 'Zaisi dar karta?'
      
# draw handler    
def draw(canvas):
    player_value = player.get_value()
    dealer_value = dealer.get_value()
    canvas.draw_text('Black Jack', [30, 70], 60, 'Black', 'serif')
    canvas.draw_text('Rezultatas: ' + str(score), [400, 60], 28, 'Black', 'serif')
    canvas.draw_text('Dealeris', [20, 260], 28, 'Black', 'serif')
    canvas.draw_text('Tu', [50, 500], 28, 'Black', 'serif')
    canvas.draw_text(prompt, [110, 580], 28, 'Black', 'serif')
    canvas.draw_text(outcome, [120, 360], 40, 'Black', 'serif')
    canvas.draw_text(str(player_value), [53, 470], 25, 'Black', 'serif')
    dealer.draw(canvas, [120, 200])
    player.draw(canvas, [120, 440])
    
    if not stand:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [120 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_BACK_SIZE)
    if stand:
        canvas.draw_text(str(dealer_value), [53, 232], 25, 'Black', 'serif')
       

     
   

    



frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

frame.add_button("Dalinti", deal, 200)
frame.add_button("Imti",  hit, 200)
frame.add_button("Sustoti", stand, 200)
frame.set_draw_handler(draw)

frame.start()
deal()

