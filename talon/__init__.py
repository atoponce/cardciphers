import math
import random

class Talon:
    #cards = (
    #    'AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC',
    #    'AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD',
    #    'AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH',
    #    'AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS'
    #    )

    #faces = [None] * 52
    #deck = [i for i in xrange(52)]
    ##deck = shuffle_deck(deck)
    #rounds = 5

    #for i in xrange(rounds):
    #    deck = step_1(deck)
    #    deck = step_2(deck)
    #    deck = step_3(deck)
    #    out = step_4(deck)

    talon_1 = []
    talon_2 = []
    talon_3 = []
    talon_4 = []

    def shuffle_deck(self, deck):
        i = 52
        while i > 1:
            i = i - 1
            j = int(math.floor(random.SystemRandom().random()*i))
            deck[j], deck[i] = deck[i], deck[j]
        return deck

    def step_1(self, deck):
        ''' Create the 4 "talons" '''
        self.talon_1.append(deck[0])
        self.talon_2.append(deck[1])
        self.talon_3.append(deck[2])
        self.talon_4.append(deck[3])
        for i in xrange(4):
            deck[0:1] = []
        return deck

    def step_2(self, deck):
        ''' Populate the 4 "talons" '''
        top_card = self.talon_1[0]%13
        for i in xrange(top_card):
            self.talon_1.insert(0, deck[0])
            deck[0:1] = []
        top_card = self.talon_2[0]%13
        for i in xrange(top_card):
            self.talon_2.insert(0, deck[0])
            deck[0:1] = []
        top_card = self.talon_3[0]%13
        for i in xrange(top_card):
            self.talon_3.insert(0, deck[0])
            deck[0:1] = []
        top_card = self.talon_4[0]%13
        for i in xrange(top_card):
            self.talon_4.insert(0, deck[0])
            deck[0:1] = []
        return deck

    def step_3(self, deck):
        ''' Collect the 4 "talons" into the main deck '''
        for i in self.talon_2:
            self.talon_1.append(i)
        for i in self.talon_3:
            self.talon_1.append(i)
        for i in self.talon_4:
            self.talon_1.append(i)
        for i in self.talon_1:
            deck.append(i)
        return deck

    def step_4(self, deck):
        '''' Determine the output card '''
        top_card = deck[0]
        bottom_card = deck[51]
        card = deck[(top_card+bottom_card) % 52]
        return card

    def algorithm(self, deck):
        ''' One full round of the Talon algorithm. Outputs a single value. '''
        deck = self.step_1(deck)
        deck = self.step_2(deck)
        deck = self.step_3(deck)
        numb = self.step_4(deck)

        self.talon_1 = []
        self.talon_2 = []
        self.talon_3 = []
        self.talon_4 = []

        return numb

