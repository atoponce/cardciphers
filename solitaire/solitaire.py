import math
import random

class Cipher(object):
    """ The full algorithm for the Solitare playing card cipher.

    Attributes:
        j (int): A running total in the RC4 algorithm
        red_values (dict): Red letters-to-values
        red_letters (dict): Red values-to-letters
        black_values (dict): Black letters-to-values
        black_letters (dict): Black values-to-letters

    """

    def __init__(self):
        """ Initialize the lookup dictionaries for the algorithm."""

    def shuffle_deck(self, deck):
        """ Shuffle the deck randomly with a Fisher-Yates shuffle

        Args:
            deck (list): A full 54-card deck with jokers. State is maintained.

        """

        i = 54
        while i > 1:
            i = i - 1
            j = int(math.floor(random.SystemRandom().random()*i))
            deck[j], deck[i] = deck[i], deck[j]

    def _step_one(self, deck):
        """ Find Joker A (value '53'), and move it down one card in the deck.
        
        Args:
            deck (list): A full 54-card deck with jokers. State is maintained.

        """

        l = deck.index(53)

        if l == 53: # it's on the bottom
            deck.insert(1, deck[l]) # insert beneath top card
            deck.pop(54)
        else:
            deck[l], deck[l+1] = deck[l+1], deck[l]

    def _step_two(self, deck):
        """ Find Joker B (value '54'), and move it down two cards in the deck.
        
        Args:
            deck (list): A full 54-card deck with jokers. State is maintained.

        """

        l = deck.index(54)

        if l == 53: # it's on the bottom
            deck.insert(2, deck[l]) # insert beneath top card + 1
            deck.pop(54)
        elif l == 52: # it's second from the bottom
            deck.insert(1, deck[l]) # insert beneath top card
            deck.pop(53)
        else:
            deck[l], deck[l+1], deck[l+2] = deck[l+1], deck[l+2], deck[l]

    def _step_three(self, deck):
        """ Perform a triple cut.

        Cut the cards above the top-most joker with the cards belowe the
        bottom-most joker.
        
        Args:
            deck (list): A full 54-card deck with jokers. State is maintained.

        """

        joker_a = deck.index(53)
        joker_b = deck.index(54)

        if joker_a < joker_b:
            top = deck[:joker_a]
            mid = deck[joker_a:joker_b+1]
            bot = deck[joker_b+1:]
        else:
            top = deck[:joker_b]
            mid = deck[joker_b:joker_a+1]
            bot = deck[joker_a+1:]

        tmp = bot + mid + top

        for i in xrange(54):
            deck[i] = tmp[i]

    def _step_four(self, deck):
        """ Perform a count cut
        
        Args:
            deck (list): A full 54-card deck with jokers. State is maintained.

        """

        count = deck[53]

        if count == 53 or count == 54:
            return True

        cut = deck[:count]
        tmp = deck[count:53] + deck[:count] + [deck[53]]

        for i in xrange(54):
            deck[i] = tmp[i]

    def mix_deck(self, deck):
        """ Swap the red card corresponding to the message with the top card

        Args:
            deck (list): A full 52-card deck. State is maintained.
            location (int): The location in the deck for IV card swapping.
            iv (bool): Mix the deck with the IV. Default: False.
        
        """

        self._step_one(deck)
        self._step_two(deck)
        self._step_three(deck)
        self._step_four(deck)

    def prng(self, deck, iv=False):
        """ Mix the deck with the standard algorithm, output an integer.

        Args:
            deck (list): A full 52-card deck. State is maintained.
            iv (bool): Mix the deck with the IV. Default: False

        Returns:
            char: Either the ciphertext or plaintext character.
        
        """

        self.mix_deck(deck)
        top = deck[0]
        out = deck[top-1]

        while out == 53 or out == 54:
            self.mix_deck(deck)
            top = deck[0]
            out = deck[top-1]

        return out
