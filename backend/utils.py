ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)

def encode_id(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    encoded = ""
    while num > 0:
        encoded = ALPHABET[num % BASE] + encoded
        num //= BASE
    return encoded