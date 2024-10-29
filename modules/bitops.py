def ROTL(x, n, num_bits=32):
    # rotate left (circular)
    return ((x << n) | (x >> num_bits-n)) %2**num_bits


def ROTR(x, n, num_bits=32):
    # rotate right (circular)
    return ((x >> n) | (x << num_bits-n)) %2**num_bits


def SHR(x,n):
    # shift right (not circular)
    return x>>n
