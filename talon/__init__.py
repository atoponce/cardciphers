import math
import random

class Cipher:
    index_set = False
    secret_index = -1

    def __init__(self):
        self.talon_1 = []
        self.talon_2 = []
        self.talon_3 = []
        self.talon_4 = []

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

    def step_2(self, deck):
        ''' Populate the 4 "talons" '''
        top_card = self.talon_1[0]%13
        if top_card == 0:
            top_card = 13
        for i in xrange(top_card-1):
            self.talon_1.insert(0, deck[0])
            deck[0:1] = []

        top_card = self.talon_2[0]%13
        if top_card == 0:
            top_card = 13
        for i in xrange(top_card-1):
            self.talon_2.insert(0, deck[0])
            deck[0:1] = []

        top_card = self.talon_3[0]%13
        if top_card == 0:
            top_card = 13
        for i in xrange(top_card-1):
            self.talon_3.insert(0, deck[0])
            deck[0:1] = []

        top_card = self.talon_4[0]%13
        if top_card == 0:
            top_card = 13
        for i in xrange(top_card-1):
            self.talon_4.insert(0, deck[0])
            deck[0:1] = []

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

    def step_4(self, deck):
        '''' Determine the output card '''
        if not self.index_set:
            self.secret_index = deck[0]-1
            self.index_set = True
        return deck[self.secret_index]

    def mix_deck(self, deck):
        ''' Execute steps 1-3 without the PRNG '''
        self.step_1(deck)
        self.step_2(deck)
        self.step_3(deck)
        self.__init__()

    def count_cut(self, deck, index):
        ''' For keys and IVs only, do a count cut on the deck '''
        cut = (deck[0] + index) % 52
        return deck[cut:] + deck[:cut]

    def prng(self, deck):
        ''' One full round of the Talon algorithm. Outputs a single value. '''
        self.mix_deck(deck)
        return self.step_4(deck)
