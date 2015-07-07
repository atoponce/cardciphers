import math
import random

class Cipher(object):
    """ The full algorithm for the Card-Chameleon playing card cipher.
    
    Attributes:
        left_values (dict): Left letters-to-values
        left_letters (dict): Left values-to-letters
        right_values (dict): Right letters-to-values
        right_letters (dict): Right values-to-letters

    """

    def __init__(self):
        """ Initialize the lookup dictionaries for the algorithm."""

        self.left_values = {
            'A':27,'B':28,'C':29,'D':30,'E':31,'F':32,'G':33,
            'H':34,'I':35,'J':36,'K':37,'L':38,'M':39,
            'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,
            'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26
        }

        self.left_letters = {
            27:'A',28:'B',29:'C',30:'D',31:'E',32:'F',33:'G',
            34:'H',35:'I',36:'J',37:'K',38:'L',39:'M',
            14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',
            21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'
        }
        self.right_values = {
            'A':40,'B':41,'C':42,'D':43,'E':44,'F':45,'G':46,
            'H':47,'I':48,'J':49,'K':50,'L':51,'M':52,
            'N': 1,'O': 2,'P': 3,'Q': 4,'R': 5,'S': 6,'T': 7,
            'U': 8,'V': 9,'W':10,'X':11,'Y':12,'Z':13
        }

        self.right_letters = {
            40:'A',41:'B',42:'C',43:'D',44:'E',45:'F',46:'G',
            47:'H',48:'I',49:'J',50:'K',51:'L',52:'M',
             1:'N', 2:'O', 3:'P', 4:'Q', 5:'R', 6:'S', 7:'T',
             8:'U', 9:'V',10:'W',11:'X',12:'Y',13:'Z'
        }

    def _find_plaintext_char(self, deck, char=None, loc=None):
        """ Find the plaintext character or location in the right pile

        Args:
            deck (list): A full 52-card deck. State is maintained.
            char (char): A single character to find. Defaults to None.
            loc (int): A location in the deck. Defaults to None.

        Returns:
            char: The plaintext character.
            int: The location in the deck of the plainetxt character.

        """

        right = deck[26:]

        if loc is not None:
            return self.right_letters[right[loc]]
        else:
            return right.index(self.right_values[char])

    def _find_ciphertext_char(self, deck, char=None, loc=None):
        """ Find the ciphertext character or location in the left pile

        Args:
            deck (list): A full 52-card deck. State is maintained.
            char (char): A single character to find. Defaults to None.
            loc (int): A location in the deck. Defaults to None.

        Returns:
            char: The ciphertext character.
            int: The location in the deck of the ciphertext character.

        """

        left = deck[:26]
        
        if loc is not None:
            return self.left_letters[left[loc]]
        else:
            return left.index(self.left_values[char])

    def prepare_deck(self, deck):
        """ Prepares the right and left piles

        Args:
            deck (list): A full 52-card deck. State is maintained.

        Returns:
            tuple: The left and right alphabets (deck piles of 26-cards).

        """

        left = []
        right = []

        for card in deck:
            if 14 <= card <= 39:
                left.insert(0, card)
            else:
                right.insert(0, card)

        for i in xrange(26):
            deck.insert(0, right[i])
            deck.pop(52)

        for i in xrange(26):
            deck.insert(0, left[i])
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

    def mix_deck(self, deck, cut):
        """ The difussion/permutation steps of the Chaocipher algorithm.

        Deck mixing happens by first identifying the left (ciphertext) and
        right (plaintext) alphabets. First, the plaintext or ciphertext
        character is identified.

        The left deck is mixed by:
            * cutting the deck at the ciphertext card putting it on the zenith.
            * inserting the zenith + 1 card into the nadir

        The right deck is mixed by:
            * cutting the deck at the plaintext card putting it on the zenith.
            * moving the zenith to the bottom of the deck
            * inserting the new zenith + 2 card into the nadir

        Args:
            deck (list): A full 52-card deck. State is maintained.
            cut (int): The location in either pile to cut the pile at.

        Returns:
            list: A full 52-card deck with the left pile on top of the right.

        """

        left = deck[:26]
        right = deck[26:]

        left = left[cut:] + left[:cut]
        left.insert(14, left[1])
        left.pop(1)

        right = right[cut:] + right[:cut]
        right.append(right[0])
        right.pop(0)
        right.insert(14, right[2])
        right.pop(2)

        for char in left:
            deck.append(char)
            deck.pop(0)

        for char in right:
            deck.append(char)
            deck.pop(0)

    def prng(self, deck, letter, method='encrypt'):
        """ Find the ciphertext or plaintext while also mixing the deck.

        Two separate algorithms are needed:

            If encrypting: find the right plaintext card first.
            If decrypting: find the left ciphertext  card first.

        Args:
            deck (list): A full 52-card deck. State is maintained.
            letter (char): A single character to be encrypted/decrypted.
            method (str): Either method='encrypt' or method='decrypt'.

        Returns:
            char: Either the ciphertext or plaintext character.
        
        """

        if method == 'encrypt':
            l = self._find_plaintext_char(deck, char=letter)
            char = self._find_ciphertext_char(deck, loc=l)
            self.mix_deck(deck, l)

        elif method == 'decrypt':
            l = self._find_ciphertext_char(deck, char=letter)
            char = self._find_plaintext_char(deck, loc=l)
            self.mix_deck(deck, l)

        return char
