import sys
import math
import random

class Cipher(object):
    """ """

    def __init__(self):
        """ """

        self.black_values = {
            'A':40,'B':41,'C':42,'D':43,'E':44,'F':45,'G':46,
            'H':47,'I':48,'J':49,'K':50,'L':51,'M':52,
            'N': 1,'O': 2,'P': 3,'Q': 4,'R': 5,'S': 6,'T': 7,
            'U': 8,'V': 9,'W':10,'X':11,'Y':12,'Z':13
        }

        self.red_values = {
            'A':27,'B':28,'C':29,'D':30,'E':31,'F':32,'G':33,
            'H':34,'I':35,'J':36,'K':37,'L':38,'M':39,
            'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,
            'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26
        }

        self.black_letters = {
            40:'A',41:'B',42:'C',43:'D',44:'E',45:'F',46:'G',
            47:'H',48:'I',49:'J',50:'K',51:'L',52:'M',
             1:'N', 2:'O', 3:'P', 4:'Q', 5:'R', 6:'S', 7:'T',
             8:'U', 9:'V',10:'W',11:'X',12:'Y',13:'Z'
        }

        self.red_letters = {
            27:'A',28:'B',29:'C',30:'D',31:'E',32:'F',33:'G',
            34:'H',35:'I',36:'J',37:'K',38:'L',39:'M',
            14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',
            21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'
        }

    def _prepare_deck(self, deck):
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

    def _find_black_card(self, deck, letter):
        """ Find the black card in the deck matching the supplied letter
        
        Args:
            deck (list): A full 52-card deck. State is maintained.
            letter (str): One character of the message.

        Returns:
            int: Deck location of the black card letter.
            
        """

        return deck.index(self.black_values[letter])

    def _find_red_card(self, deck, letter):
        """ Find the red card in the deck matching the supplied letter
        
        Args:
            deck (list): A full 52-card deck. State is maintained.
            letter (int): The integer representation of a character.

        Returns:
            int: Deck location of the red card letter.
            
        """

        return deck.index(self.black_values[letter])

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
        self._prepare_deck(deck)

    def prng(self, deck, letter):
        """ """

        called_method = sys._getframe().f_back.f_code.co_name

        black_1 = None
        black_2 = None
        red_1 = None
        red_2 = None

        if called_method == 'encrypt':
            black_1 = self._find_black_card(deck, letter)
            red_1 = deck[black_1 - 1]
            black_2 = self._find_black_card(deck, self.red_letters[red_1])
            red_2 = deck[black_2 - 1]
            deck[0], deck[black_2 - 1] = deck[black_2 - 1], deck[0]
            return self.red_letters[red_2]

        elif called_method == 'decrypt':
            red_1 = self._find_red_card(deck, letter)
            black_1 = deck[red_1 + 1]
            red_2 = self._find_red_card(deck, self.black_letters[black_1])
            black_2 = deck[red_2 + 1]
            deck[0], deck[red_2] = deck[red_2], deck[0]
            return self.black_letters[black_2]
