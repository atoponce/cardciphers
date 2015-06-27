import talon
import Image

size = 52*80
t = talon.Cipher()
d = [i for i in xrange(1,53)]

pic = Image.new('RGB', (size, size))
for x in xrange(size):
    for y in xrange(size):
        n = t.prng(d)
        if n % 2 == 0:
            pic.putpixel((x,y), (255,255,255))

pic.save('/var/www/talon.png')
