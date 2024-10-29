# def get_bool_for_ch(ch):
#     code_point = ord(ch)
#     for h in range(8, 40, 8):
#         if code_point < 2**h:
#             return format(code_point, 'b').zfill(h)


# def text_to_binary(s, bitlen=64):
#     return [get_bool_for_ch(ch) for ch in s]


# def get_message(m):
#     """
#     takes in string. returns binary representation of string using 8-bits per char
#     """
#     return "".join(text_to_binary(m,8))


# def pad_message(message_bin):
#     """
#     This should work for sha1, sha224, sha256
#     """
#     l = len(message_bin)

#     k = (448-l-1)%512

#     message_bin += "1"
#     message_bin += k*"0"
#     message_bin += bin(l)[2:].zfill(64)

#     return message_bin

# def padded_message_to_ints(message):
#     outputs = []
#     for i in range(0, len(message), 512):
#         m = message[i:i+512]
#         outputs.append([int(m[i:i+32], 2) for i in range(0, 512, 32)])

#     return outputs


def get_message(m):
    return m.encode().hex()


def pad_message(m):
    l = len(m)

    k = (448//4 - l - 1) % 128 
    m += "8"
    m += k*"0"
    m += hex(l*4)[2:].zfill(64//4)  # length of message in bits is l*4

    return m
    
    
def padded_message_to_ints(m):
    outputs = []
    for i in range(0, len(m), 128):
        msg = m[i:i+128]
        outputs.append([int(msg[j:j+8], 16) for j in range(0, 128, 8)])
    return outputs


def to_hexword(bits):
    if bits.startswith("0b"):
        bits = bits[2:]
    if len(bits) % 4:
        print("WARN: len of bitstring not divisible by 4")
        
    output = ""
    for idx in range(0,len(bits),4):
        output += hex(int(bits[idx:idx+4], 2))[-1]
    return output