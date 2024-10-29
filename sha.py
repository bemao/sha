import sys
from modules.data_ops import (
    pad_message,
    padded_message_to_ints,
    to_hexword
)
from modules.sha1_ops import _sha1
from modules.sha256_ops import _sha256


def hash_message(msg, hash_type='sha256', return_hex=True):
    """
    Expected input: msg should be hex digits

    hash_type: sha1 or sha256
    return_hex: whether or not to return the hash a hash digits (else binary string)    
    """
    
    if hash_type not in ["sha1", "sha256"]:
        print(
            f"ERROR: Hash type '{hash_type}' not recognized. "
            "Implemented types: 'sha1', 'sha256'"
            )
        return ""

    m = pad_message(msg)
    M = padded_message_to_ints(m)

    digest = _sha1(M) if hash_type == 'sha1' else _sha256(M)

    return to_hexword(digest) if return_hex else digest


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(
            """Usage: python sha.py <input_file> <OPTIONAL: sha1 or sha256>"""
            )
        quit()

    with open(sys.argv[1], "rb") as f:
        input = f.read().hex()

    hash_type = "sha256"
    if len(sys.argv) >= 3:
        hash_type = sys.argv[2].lower()
    print(f"Using hash type: {hash_type}")

    print(hash_message(input, hash_type=hash_type))
