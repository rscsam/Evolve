import random


def mix_colors(a, b):
    nrx = format(int((int('0x' + a[1:3], 16) + int('0x' + b[1:3], 16)) / 2), '02x')
    ngx = format(int((int('0x' + a[3:5], 16) + int('0x' + b[3:5], 16)) / 2), '02x')
    nbx = format(int((int('0x' + a[5:7], 16) + int('0x' + b[5:7], 16)) / 2), '02x')
    return "#" + str(nrx) + str(ngx) + str(nbx)


def random_color():
    nrx = format(int(random.random()*256), '02x')
    ngx = format(int(random.random()*256), '02x')
    nbx = format(int(random.random()*256), '02x')
    return "#" + str(nrx) + str(ngx) + str(nbx)
