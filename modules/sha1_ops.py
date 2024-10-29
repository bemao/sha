from modules.bitops import ROTL, ROTR, SHR


def get_message_schedule_sha1(M):
    """
    We assume that M is an array of 16 ints, which have been created from
      512 32-bit binary arrays
    """
    message_schedule = []

    for i in M:
        message_schedule.append(i)
    for i in range(16, 80):
        p1 = message_schedule[i-3]
        p2 = message_schedule[i-8]
        p3 = message_schedule[i-14]
        p4 = message_schedule[i-16]
        
        rot_input = p1 ^ p2 ^ p3 ^ p4
        rotated = ROTL(rot_input, 1)
        message_schedule.append(rotated) 

    return message_schedule


def get_const_sha1(i):
    # these are given in the paper
    if i <= 19:
        return int("5a827999", 16)
    if i <= 39:
        return int("6ed9eba1", 16)
    if i <= 59:
        return int("8f1bbcdc", 16)
    return int("ca62c1d6", 16)


def f(x, y, z, i):
    if i <= 19:
        return (x & y) ^ (~x&z)
    if i <= 39:
        return x^y^z
    if i <= 59: 
        return (x&y) ^ (x&z) ^ (y&z)
    return x^y^z
    

def spin_inputs(a, b, c, d, e, message_schedule):
    for i in range(80):
        T = (ROTL(a, 5) + f(b, c, d, i) + e + get_const_sha1(i) + message_schedule[i]) % 2**32
        e = d
        d = c
        c = ROTL(b, 30)
        b = a
        a = T

    return a,b,c,d,e


def _sha1(M):
    """
    We assume that M is an array of arrays of 16 ints, which have been created from
      512 32-bit binary arrays
    """

    # these are given in the paper
    H_0 = int("67452301", 16)
    H_1 = int("efcdab89", 16)
    H_2 = int("98badcfe", 16)
    H_3 = int("10325476", 16)
    H_4 = int("c3d2e1f0", 16)
    
    for M_i in M:
        message_schedule = get_message_schedule_sha1(M_i)
        
        a,b,c,d,e = H_0, H_1, H_2, H_3, H_4
        a,b,c,d,e = spin_inputs(a,b,c,d,e, message_schedule)
        
        H_0 = ( H_0 + a ) %2**32
        H_1 = ( H_1 + b ) %2**32
        H_2 = ( H_2 + c ) %2**32
        H_3 = ( H_3 + d ) %2**32
        H_4 = ( H_4 + e ) %2**32

    return "".join([format(H_0,"b").zfill(32),
                    format(H_1,"b").zfill(32),
                    format(H_2,"b").zfill(32),
                    format(H_3,"b").zfill(32),
                    format(H_4,"b").zfill(32)])

