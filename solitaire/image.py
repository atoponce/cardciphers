import math
import Image
import pocket_rc4

size = 52*30
c = pocket_rc4.Cipher()
d = [i for i in xrange(1,53)]
c.prepare_deck(d)
for i in xrange(13):
    c.shuffle_deck(d)

pic = Image.new('RGB', (size, size))
for x in xrange(size):
    for y in xrange(size):
        n = c.prng(d)
        if n % 2 == 0:
            pic.putpixel((x,y), (255,255,255))

pic.save('random.png')
