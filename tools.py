def mix_colors(a, b):
    argb = int('0x' + a[1:], 16)
    brgb = int('0x' + b[1:], 16)
    nrgb = hex(int((argb + brgb)/2))
    return "#" + str(nrgb)[2:]

def add_colors(a, offset):
    argb = int('0x' + a[1:], 16)
    orgb = int('0x' + offset[1:], 16)
    nr = min(argb[1:3], 255)
    ng = min(argb[3:5], 255)
    nb = min(argb[5:], 255)