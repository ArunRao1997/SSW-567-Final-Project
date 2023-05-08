"""
Module for parsing and generating Machine Readable Travel Documents (MRTD).
"""
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
    """Returns numeric value for input char used in check digit algorithm."""
    char = char.lower()
    return CHAR_DICT[char]


def get_check_digit(input_str):
    """Takes string of alphanumeric characters and returns check digit."""
    weights = [7, 3, 1]
    sum_ = sum(char_to_value(char) * weights[idx % 3]
               for idx, char in enumerate(input_str))
    return str(sum_ % 10)


def scan_passport():
    """Scans a passport."""
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


def extract_line2(line):
    # Extracts data from the second line of the passport string
    val = line.split('<')
    res = [i for i in val if i.strip()]
    passport_number = res[0][:9]
    passport_number_check_digit = res[0][9]
    country_code = res[0][10:13]
    birth_date = res[0][13:19]
    birth_date_check_digit = res[0][19]
    sex = res[0][20]
    expiry_date = res[0][21:27]
    expiry_date_check_digit = res[0][27]
    personal_number = res[0][28:]
    personal_number_check = res[1]
    if (
            get_check_digit(passport_number) != passport_number_check_digit or
            get_check_digit(birth_date) != birth_date_check_digit or
            get_check_digit(expiry_date) != expiry_date_check_digit or
            get_check_digit(personal_number) != personal_number_check
    ):
        raise ValueError("Passport Error")
    return {
        "passport_number": passport_number,
        "country_code": country_code,
        "birth_date": birth_date,
        "sex": sex,
        "expiry_date": expiry_date,
        "personal_number": personal_number
    }


def decode(string):
    """
    Takes in a string and parses it to extract MRZ data.
    Returns data in the same format as 'records_decoded' if the string is valid,
    prints an error and returns False if there is an issue.
    """
    lines = string.split(";")
    line1 = extract_line1(lines[0])
    line2 = extract_line2(lines[1])
    if line1["issuing_country"] != line2['country_code']:
        # Invalid MRZ data
        print("Error: invalid MRZ data")
        return False
    result = {"line1": line1, "line2": line2}
    result = json.dumps(result)
    # print("records_decoded: " + result)
    return result


def encode(data):
    """
    Takes in a JSON object and generates a string for the MRZ.
    """
    line1 = encode_line1(data.get('line1', {}))
    line2 = encode_line2(data.get('line2', {}))
    result = line1 + ";" + line2
    # print("records_encoded: " + result)
    return result


def encode_line1(data):
    # accepts dict of line1 data and generates a string
    issuing_country = data.get('issuing_country')
    last_name = data.get('last_name')
    given_name = data.get('given_name')
    if not (issuing_country and last_name and given_name):
        return 1
    given_name = given_name.replace(" ", "<")
    line = f'{issuing_country}{last_name}<<{given_name}'
    line_length = 44
    line += '<' * (line_length - len(line))
    line += get_check_digit(issuing_country + last_name + given_name)
    return line


def encode_line2(data):
    """
    Accepts a dictionary of line2 data and generates a MRZ string.

    :param data: A dictionary containing the following keys:
                 - passport_number: A string representing the passport number.
                 - country_code: A string representing the country code.
                 - birth_date: A string representing the birth date in the format YYMMDD.
                 - expiration_date: A string representing the expiration date in the format YYMMDD.
                 - sex: A string representing the sex of the passport holder.
                 - personal_number: A string representing the personal_number.
                  :return: A string representing the MRZ line.
    """
    passport_number = data.get('passport_number')
    passport_number_check = get_check_digit(passport_number)
    country_code = data.get('country_code')
    birth_date = data.get('birth_date')
    birth_date_check = get_check_digit(birth_date)
    expiration_date = data.get('expiration_date')
    expiration_date_check = get_check_digit(expiration_date)
    sex = data.get('sex')
    personal_number = data.get('personal_number')
    personal_number_check = get_check_digit(personal_number)
    if not (passport_number and passport_number_check and country_code and birth_date and birth_date_check and
            sex and expiration_date and expiration_date_check and personal_number and personal_number_check):
        return 1
    line = (f'{passport_number}{passport_number_check}{country_code}{birth_date}{birth_date_check}{sex}'
            f'{expiration_date}{expiration_date_check}{personal_number}')
    line += '<' * (43 - len(line))
    line += personal_number_check
    return line
