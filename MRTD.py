"""MRTD.py"""
from string import ascii_uppercase, digits

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

printable = digits + ascii_uppercase + "<"+";"

def algorithm(string: str) -> str:
    """Function for weights"""
    string = string.upper().replace("<", "0")
    weight = [7, 3, 1]
    summation = 0
    for i in range(len(string)):
        c = string[i]
        summation += printable.index(c) * weight[i % 3]
    summation %=10
    return summation

def verify (string0: str) -> str:
    """function to verify"""
    for i in range(len(string0)):
        c = string0[i]
        if c not in printable:
            return "contains invalid characters"
    string1 = string0[45:]
    passport = string1[0:9]
    passport_verify_code = int(string1[9])
    birth = string1[13:19]
    birth_verify_code = int(string1[19])
    validity = string1[21:27]
    validity_verify_code = int(string1[27])
    personal_code = string1[28:43]
    personal_verify_code = int(string1[43])

    if algorithm(passport) != passport_verify_code:
        return "passport info error"
    elif algorithm(birth) != birth_verify_code:
        return "birth date info error"
    elif algorithm(validity) != validity_verify_code:
        return "validity info error"
    elif algorithm(personal_code) != personal_verify_code:
        return "personal code error"
    else:
        return "passed"

def char_to_value(char):
    """Returns numeric value for input char used in check digit algorithm"""
    # Returns numeric value for input char used in check digit algorithm
    char = char.lower()
    return CHAR_DICT[char]


def get_check_digit(input):
    """Takes string of alphanumeric characters and returns check digit"""
    # Takes string of alphanumeric characters and returns check digit
    weights = [7, 3, 1]
    sum_ = sum(char_to_value(char) * weights[idx % 3]
               for idx, char in enumerate(input))
    return str(sum_ % 10)

def scan_passport():
    """Function to scan passport"""
    #empty method
    return 'scanned'

def extract_line1(line):
    """Function to extract line 1"""
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

def encode(string0: str) -> str:
    """Function to encode"""
    string1 = string0[45:]
    passport_number = string1[0:9]
    country_code = string1[10:13]
    birth_date = string1[13:19]
    sex = string1[20]
    expiration_date = string1[21:27]
    personal_number = string1[28:37]

    d= {}
    k={}
    d['line2'] =  k
    k['passport_number'] = passport_number
    k['country_code'] = country_code
    k['birth_date'] = birth_date
    k['sex'] = sex
    k['expiration_date'] = expiration_date
    k['personal_number'] = personal_number

    return d

def decode(dict):
    """Functtion to decode"""
    dict1 = dict["line1"]
    dict2 = dict["line2"]
    issc = dict1["issuing_country"]
    lastname = dict1["last_name"]
    givenname = dict1["given_name"]
    passport = dict2["passport_number"]
    country = dict2["country_code"]
    birth = dict2["birth_date"]
    sex = dict2["sex"]
    exd = dict2["expiration_date"]
    pn = dict2["personal_number"]
    line1decode = "P<" + issc + lastname + "<<" + givenname.replace(' ','<')
    line1decoded1 = line1decode.ljust(44,'<')
    line2decode = passport + str(algorithm(passport)) + country + birth + str(algorithm(birth))
    line2decode = line2decode + sex +exd + str(algorithm(exd)) + pn + "<<<<<<" + str(algorithm(pn))
    decoded = line1decoded1 +";"+line2decode
    return decoded
