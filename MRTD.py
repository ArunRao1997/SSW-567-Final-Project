import json

CHAR_DICT = {
    '<': 0,
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15,
    'g': 16,
    'h': 17,
    'i': 18,
    'j': 19,
    'k': 20,
    'l': 21,
    'm': 22,
    'n': 23,
    'o': 24,
    'p': 25,
    'q': 26,
    'r': 27,
    's': 28,
    't': 29,
    'u': 30,
    'v': 31,
    'w': 22,
    'x': 33,
    'y': 34,
    'z': 35,
}


def char_to_value(char):
    # Returns numeric value for input char used in check digit algorithm
    char = char.lower()
    return CHAR_DICT[char]


def get_check_digit(input):
    # Takes string of alphanumeric characters and returns check digit
    weights = [7, 3, 1]
    sum_ = sum(char_to_value(char) * weights[idx % 3]
               for idx, char in enumerate(input))
    return str(sum_ % 10)

def scan_passport():
    #empty method
    return 'scanned'

def extract_line1(line):
    # Extracts data from the first line of the passport string
    val = line.split('<')
    res = [i for i in val if i.strip()]
    if res[0] != "P":
        return 1
    country_code = res[1][:3]
    last_name = res[1][3:]
    first_name = res[2]
    middle_name = res[3] if len(res) == 4 else None
    given_name = f"{first_name} {middle_name}" if middle_name else first_name
    return {
        "issuing_country": country_code,
        "last_name": last_name,
        "given_name": given_name
    }