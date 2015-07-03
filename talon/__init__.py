import math
import random

class Cipher(object):
    """ The full algorithm for the Talon playing card cipher PRNG.

    Attributes:
        secret_index (int): The value of the static secret index of the PRNG.
        talon_1 (list): The first discard pile
        talon_2 (list): The second discard pile
        talon_3 (list): The third discard pile
        talon_4 (list): The fourth discard pile

    """

    secret_index = 0

    def __init__(self):
        """ Initialize the talons (discard piles) to empty strings """

        self.talon_1 = []
        self.talon_2 = []
        self.talon_3 = []
        self.talon_4 = []

    def _step_1(self, deck):
        """ Create the 4 talons (piles) for deck mixing, but do not populate.

        The top card off the deck will create the first talon; the second card
        will create the second talon; the third card, the third talon; the
        fourth card, the fourth talon.

        Args:
            deck (list): A full 52-card deck. State is maintained.

        """

        self.talon_1.append(deck[0])
        self.talon_2.append(deck[1])
        self.talon_3.append(deck[2])
        self.talon_4.append(deck[3])
        for i in xrange(4):
            deck[0:1] = []

    def _step_2(self, deck):
        """ Populate the 4 talons (piles).

        The first card in each talon determines the size of the talon itself.
        The value is calculated by taking the face value for that suit. Ace=1
        and King=13. No more than 13 cards can exist in each of the 4 talons.

        Args:
            deck (list): A full 52-card deck. State is maintained.

        """

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

    def _step_3(self, deck):
        """ Collect the four talons on top of each other in numerical order.

        Args:
            deck (list): A full 52-card deck. State is maintained.

        """

        for i in self.talon_2:
            self.talon_1.append(i)
        for i in self.talon_3:
            self.talon_1.append(i)
        for i in self.talon_4:
            self.talon_1.append(i)
        for i in self.talon_1:
            deck.append(i)

    def _step_4(self, deck):
        """ Determine the output card of the generator round.

        For each round required, a pseudorandom number is output, one number
        per round. The range of the PRNG is [1,52]. The output number is found
        be reading the value of "self.secret_index". This is found by reading
        the top card.

        Args:
            deck (list): A full 52-card deck. State is maintained.

        Returns:
            int: The deck card value at a static deterministic deck location.

        """

        if not self.secret_index:
            self.secret_index = deck[0]
        return deck[self.secret_index-1]

    def shuffle_deck(self, deck):
        """ Shuffle the deck randomly with a Fisher-Yates shuffle

        Args:
            deck (list): A full 52-card deck. State is maintained.

        Returns:
            list: A randomly shuffled 52-card deck.

        """

        i = 52
        while i > 1:
            i = i - 1
            j = int(math.floor(random.SystemRandom().random()*i))
            deck[j], deck[i] = deck[i], deck[j]

    def mix_deck(self, deck):
        """ Execute the first three steps of the Talon card-cipher algorithm.

        First initialize the talons, then populate the talons, then collect the
        talons. After which, initialize the talons back to empty lists for the
        next round.

        Args:
            deck (list): A full 52-card deck. State is maintained.

        """

        self._step_1(deck)
        self._step_2(deck)
        self._step_3(deck)
        self.__init__()

    def count_cut(self, deck, index):
        """ For additional mixing of the deck for keys and IVs only.

        Do a count cut on the deck instead of generating an integer output.
        This is only useful for further mixing of the deck before generating
        the keystream.

        Args:
            deck (list): A full 52-card deck. State is maintained.
            index (int): A location in the deck to perform a standard cut.

        Returns:
            list: A cut 52-card deck.

        """

        cut = (deck[0] + index) % 52
        return deck[cut:] + deck[:cut]

    def prng(self, deck):
        """ Mix the deck with the standard algorithm steps, output an integer.

        Mix the deck using steps 1 through 4 of the Talon algorithm. Assume the
        deck has been keyed and the initialization vector processed already.
        Output one integer in the range [1,52] for the keystream.

        Args:
            deck (list): A full 52-card deck. State is maintained.

        Returns:
            int: One number for the keystream.

        """

        self.mix_deck(deck)
        return self._step_4(deck)
