import math
import random

class Cipher(object):
    """ """

    def __init__(self):
        """ """
        return None

    def prepare_deck(self, deck):
        """ Prepares the deck for strictly alternating red/black cards

        Args:
            deck (list): A full 52-card deck. State is maintained.

        """

        black_pile = []
        red_pile = []

        for card in deck:
            if 14 <= card <= 39: # diamonds through hearts
                red_pile.insert(0, card)
            else: # clubs and spades
                black_pile.insert(0, card)

        for i in xrange(26):
            deck.insert(0, black_pile[i])
            deck.insert(0, red_pile[i])
            deck.pop(53)
            deck.pop(52)

    def shuffle_deck(self, deck):
        """ Shuffle the deck randomly with a Fisher-Yates shuffle

        Args:
            deck (list): A full 52-card deck. State is maintained.

        """

        i = 52
        while i > 1:
            i = i - 1
            j = int(math.floor(random.SystemRandom().random()*i))
            deck[j], deck[i] = deck[i], deck[j]
        self.prepare_deck(deck)

    def step_1(self, deck, letter):
        """ Find the black card in the deck matching the supplied letter
        
        Args:
            deck (list): A full 52-card deck. State is maintained.
            letter (str): A character from the plaintext.
        """

        return True

    def step_2(self, deck):
        """ """
        return True

    def step_3(self, deck):
        """ """
        return True

    def step_4(self, deck):
        """ """
        return True

    def mix_deck(self, deck):
        """ """
        return True

    def count_cut(self, deck, index):
        """ """
        return True

    def prng(self, deck):
        """ """
        return True
