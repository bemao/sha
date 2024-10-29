from modules.bitops import ROTR, ROTL, SHR


# a list of constants given in the paper
SHA256_CONST = """428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967
27b70a85 2e1b2138 4d2c6dfc 53380d13 650a7354 766a0abb 81c2c92e 92722c85
a2bfe8a1 a81a664b c24b8b70 c76c51a3 d192e819 d6990624 f40e3585 106aa070
19a4c116 1e376c08 2748774c 34b0bcb5 391c0cb3 4ed8aa4a 5b9cca4f 682e6ff3
748f82ee 78a5636f 84c87814 8cc70208 90befffa a4506ceb bef9a3f7 c67178f2"""


sha256_const_list = SHA256_CONST.split()


def sigma0(w):
    return ROTR(w,7) ^ ROTR(w,18) ^ SHR(w,3)


def sigma1(w):
    return ROTR(w,17) ^ ROTR(w,19) ^ SHR(w,10)


def big_sig0(w):
    return ROTR(w,2) ^ ROTR(w,13) ^ ROTR(w,22)


def big_sig1(w):
    return ROTR(w,6) ^ ROTR(w,11) ^ ROTR(w,25)


def Ch_256(x,y,z):
    return (x & y) ^ (~x & z)


def Maj(x,y,z):
    return (x & y) ^ (x & z) ^ (y&z)


def get_const_256(i):
    return int(sha256_const_list[i], 16)


def get_message_schedule_256(M_i):
    """
    We assume that M is an array of 16 ints, which have been created from
      512 32-bit binary arrays
    """
    message_schedule = []

    for i in M_i:
        message_schedule.append(i)
    for i in range(16, 64):
        w = (
            sigma1(message_schedule[i-2])
            + message_schedule[i-7]
            + sigma0(message_schedule[i-15])
            + message_schedule[i-16]
        )
        message_schedule.append(w % 2**32)

    return message_schedule


def spin_inputs_256(a,b,c,d,e,f,g,h, message_schedule):
    for i in range(64):
        T_1 = ( h + big_sig1(e) + Ch_256(e,f,g) + get_const_256(i) + message_schedule[i] ) % 2**32
        T_2 = ( big_sig0(a) + Maj(a,b,c) ) % 2**32
        h = g
        g = f
        f = e
        e = ( d + T_1 ) % 2**32
        d = c
        c = b
        b = a
        a =( T_1 + T_2 ) % 2**32

    return a,b,c,d,e,f,g,h


def _sha256(M):
    # these are given in the paper
    H_0 = int("6a09e667", 16)
    H_1 = int("bb67ae85", 16)
    H_2 = int("3c6ef372", 16)
    H_3 = int("a54ff53a", 16)
    H_4 = int("510e527f", 16)
    H_5 = int("9b05688c", 16)
    H_6 = int("1f83d9ab", 16)
    H_7 = int("5be0cd19", 16)
    
    for M_i in M:
        message_schedule = get_message_schedule_256(M_i)
        
        a,b,c,d,e,f,g,h = H_0, H_1, H_2, H_3, H_4, H_5, H_6, H_7
        a,b,c,d,e,f,g,h = spin_inputs_256(a,b,c,d,e,f,g,h, message_schedule)
        
        H_0 = ( H_0 + a ) %2**32
        H_1 = ( H_1 + b ) %2**32
        H_2 = ( H_2 + c ) %2**32
        H_3 = ( H_3 + d ) %2**32
        H_4 = ( H_4 + e ) %2**32
        H_5 = ( H_5 + f ) %2**32
        H_6 = ( H_6 + g ) %2**32
        H_7 = ( H_7 + h ) %2**32

    return "".join([format(H_0,"b").zfill(32),
                    format(H_1,"b").zfill(32),
                    format(H_2,"b").zfill(32),
                    format(H_3,"b").zfill(32),
                    format(H_4,"b").zfill(32),
                    format(H_5,"b").zfill(32),
                    format(H_6,"b").zfill(32),
                    format(H_7,"b").zfill(32)])
