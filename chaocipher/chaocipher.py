#deck = [i for i in xrange(1,53)]
deck = [34, 24, 21, 29, 26, 22, 27, 39, 30, 19, 38, 37, 16, 31, 32, 36, 18, 35, 33, 20, 23, 15, 28, 14, 25, 17, 3, 7, 51, 1, 41, 4, 43, 44, 2, 12, 6, 45, 40, 9, 13, 50, 46, 49, 5, 48, 47, 10, 11, 8, 52, 42]
keyphrase = 'WELLDONEISBETTERTHANWELLSAID'
r_alph = ""
l_alph = ""
ct = ""
pt = ""

left_values = {
    'A':27,'B':28,'C':29,'D':30,'E':31,'F':32,'G':33,
    'H':34,'I':35,'J':36,'K':37,'L':38,'M':39,
    'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,
    'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26
}

left_letters = {
    27:'A',28:'B',29:'C',30:'D',31:'E',32:'F',33:'G',
    34:'H',35:'I',36:'J',37:'K',38:'L',39:'M',
    14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',
    21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'
}

right_values = {
    'A':40,'B':41,'C':42,'D':43,'E':44,'F':45,'G':46,
    'H':47,'I':48,'J':49,'K':50,'L':51,'M':52,
    'N': 1,'O': 2,'P': 3,'Q': 4,'R': 5,'S': 6,'T': 7,
    'U': 8,'V': 9,'W':10,'X':11,'Y':12,'Z':13
}

right_letters = {
    40:'A',41:'B',42:'C',43:'D',44:'E',45:'F',46:'G',
    47:'H',48:'I',49:'J',50:'K',51:'L',52:'M',
     1:'N', 2:'O', 3:'P', 4:'Q', 5:'R', 6:'S', 7:'T',
     8:'U', 9:'V',10:'W',11:'X',12:'Y',13:'Z'
}

def create_piles(deck):
    left = []
    right = []

    for card in deck:
        if 14 <= card <= 39:
            left.append(card)
        else:
            right.append(card)
    return left, right

def permute_piles(deck, cut):
    left = create_piles(deck)[0]
    right = create_piles(deck)[1]

    # permute the left pile
    left = left[cut:] + left[:cut] # cut the pile at the ciphertext card
    left.insert(14, left[1]) # insert the nadir + 1 card at the nadir of the pile
    left.pop(1) # remove the new zenith + 1 card from the pile

    # permute the right pile
    right = right[cut:] + right[:cut]
    right.append(right[0]) # move the card at the zenith to the bottom of the pile
    right.pop(0)
    right.insert(14, right[2]) # insert the zenith + 2 card at the nadir of the pile
    right.pop(2) # remove the new zenith + 2 card from the pile

    return left + right

def find_plaintext_char(deck, char=None, loc=None):
    right = create_piles(deck)[1]
    if loc is not None:
        return right_letters[right[loc]]
    else:
        return right.index(right_values[char])

def find_ciphertext_char(deck, char=None, loc=None):
    left = create_piles(deck)[0]
    if loc is not None:
        return left_letters[left[loc]]
    else:
        return left.index(left_values[char])

for c in list(keyphrase):
    l = find_plaintext_char(deck, char=c)
    ct += find_ciphertext_char(deck, loc=l)
    deck = permute_piles(deck, l)

left = create_piles(deck)[0]
right = create_piles(deck)[1]

for card in right:
    r_alph += right_letters[card]

for card in left:
    l_alph += left_letters[card]

deck = [34, 24, 21, 29, 26, 22, 27, 39, 30, 19, 38, 37, 16, 31, 32, 36, 18, 35, 33, 20, 23, 15, 28, 14, 25, 17, 3, 7, 51, 1, 41, 4, 43, 44, 2, 12, 6, 45, 40, 9, 13, 50, 46, 49, 5, 48, 47, 10, 11, 8, 52, 42]

for c in list(ct):
    l = find_ciphertext_char(deck, char=c)
    pt += find_plaintext_char(deck, loc=l)
    deck = permute_piles(deck, l)

print pt
print ct
