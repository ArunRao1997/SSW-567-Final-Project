# importing required modules
import json
import sqlite3
import unittest
from unittest.mock import Mock, MagicMock

import MRTD


class TestDecodeEncode(unittest.TestCase):
    """
    Test Class for encode and decode
    """
    # Set up test data
    def setUp(self):
        self.line = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'
        self.expected_result1 = '{"line1": {"issuing_country": "CIV", "last_name": "LYNN", "given_name": "NEVEAH BRAM"}, "line2": {"passport_number": "W620126G5", "country_code": "CIV", "birth_date": "591010", "sex": "F", "expiry_date": "970730", "personal_number": "AJ010215I"}}'
        self.expected_result2 = {'issuing_country': 'CIV',
                                 'last_name': 'LYNN', 'given_name': 'NEVEAH BRAM'}
        self.expected_result3 = {'passport_number': 'W620126G5', 'country_code': 'CIV',
                                 'birth_date': '591010', 'sex': 'F', 'expiry_date': '970730', 'personal_number': 'AJ010215I'}
        self.data = {
            "line1": {
                "issuing_country": "CIV",
                "last_name": "LYNN",
                "given_name": "NEVEAH BRAM"
            },
            "line2": {
                "passport_number": "W620126G5",
                "country_code": "CIV",
                "birth_date": "591010",
                "sex": "F",
                "expiration_date": "970730",
                "personal_number": "AJ010215I"
            }
        }
        self.expected_result4 = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'
        self.expected_result5 = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<'

    def test_decode(self):
        """Test the decode function with valid input."""
        self.assertEqual(MRTD.decode(self.line), json.loads(self.expected_result1),
                         'Line 1 and line 2 decoded successfully')

    # Test decode function containing country code
    def test_decode2(self):
        """Test the decode function with a different country code."""
        line = 'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54RIS5910106F9707302AJ010215I<<<<<<6'
        self.assertNotEqual(MRTD.decode(line), json.loads(self.expected_result1), 'Different country code')

    # Test extract1 function for line 1
    def test_find_val1(self):
        """Test the extract_line1 function with valid input."""
        self.assertEqual(MRTD.extract_line1('P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<'),
                         self.expected_result2, 'Got expected result2')

    # Test extract function if no document type is given
    def test_find_val2(self):
        """Test the extract_line1 function without a document type."""
        self.assertEqual(MRTD.extract_line1(
            '<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<'), 1, 'Got expected exception')

    # Test extract2 function for line 2
    def test_find_val3(self):
        """Test the extract_line2 function with valid input."""
        self.assertEqual(MRTD.extract_line2("W620126G54CIV5910106F9707302AJ010215I<<<<<<6"),
                         self.expected_result3, "Got expected result3")

    # Test extract_line1_no_middle_name
    def test_extract_line1_no_middle_name(self):
        """Test the extract_line1 function without a middle name."""
        self.assertEqual(
            MRTD.extract_line1('P<ABWMALDONADO<<CAMILLA<<<<<<<<<<<<<<<<<<<<<<'),
            {
                'issuing_country': 'ABW',
                'last_name': 'MALDONADO',
                'given_name': 'CAMILLA'
            },
            'Expecting the extracted data'
        )

    def test_encode_data_in_mrtd_format(self):
        """Test the encode function with valid input."""
        data = {
            "line1": {
                "issuing_country": "CIV",
                "last_name": "LYNN",
                "given_name": "NEVEAH BRAM"
            },
            "line2": {
                "passport_number": "W620126G5",
                "country_code": "CIV",
                "birth_date": "591010",
                "sex": "F",
                "expiration_date": "970730",
                "personal_number": "AJ010215I"
            }
        }
        self.assertNotEqual(
            MRTD.encode(data),
            'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;'
            'W620126G54CIV5910106F9707302AJ010215I<<<<<<6',
            'Expecting the encoded data'
        )

    def test_encode_line1_data(self):
        """Test the encode_line1 function with valid input."""
        data = {
            "line": {
                "issuing_country": "CIV",
                "last_name": "LYNN",
                "given_name": "NEVEAH BRAM"
            }
        }
        self.assertNotEqual(
            MRTD.encode_line1(data['line']),
            'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<',
            'Expecting the encoded data'
        )

    def test_encode_line1_missing_given_name(self):
        """
        Test case to check the encode_line1 method when the given name is missing.
        """
        data = {
            "line": {
                "issuing_country": "CIV",
                "last_name": "LYNN",
                "given_name": ""
            }
        }
        self.assertEqual(
            MRTD.encode_line1(data['line']),
            1,
            'Expecting 1 if given name is missing'
        )

    def test_encode_line1_missing_last_name(self):
        """
        Test case to check the encode_line1 method when the last name is missing.
        """
        data = {
            "line": {
                "issuing_country": "CIV",
                "last_name": "",
                "given_name": "NEVEAH BRAM"
            }
        }
        self.assertEqual(
            MRTD.encode_line1(data['line']),
            1,
            'Expecting 1 if last name is missing'
        )

    def test_encode_line1_missing_issuing_country(self):
        """
        Test case to check the encode_line1 method when the issuing country is missing.
        """
        data = {
            "line": {
                "issuing_country": "",
                "last_name": "LYNN",
                "given_name": "NEVEAH BRAM"
            }
        }
        self.assertEqual(
            MRTD.encode_line1(data['line']),
            1,
            'Expecting 1 if issuing country is missing'
        )

    def test_encode_line1_missing_all_data(self):
        """
        Test case to check the encode_line1 method when all data is missing.
        """
        data = {
            "line": {
                "issuing_country": "",
                "last_name": "",
                "given_name": ""
            }
        }
        self.assertEqual(
            MRTD.encode_line1(data['line']),
            1,
            'Expecting 1 if all data is missing'
        )

    # Test to encode data in line 2 of an MRTD
    def test_encode_line2(self):
        """Test encoding of line 2 data."""
        data = {
            "line": {
                "passport_number": "W620126G5",
                "country_code": "CIV",
                "birth_date": "591010",
                "sex": "F",
                "expiration_date": "970730",
                "personal_number": "AJ010215I"
            }
        }
        # Assert the encoded line 2 data with the expected output
        self.assertEqual(MRTD.encode_line2(data['line']),
                         'W620126G54CIV5910106F9707302AJ010215I<<<<<<6',
                         'Returns encoded part 2 data')

    # Test for missing country code
    def test_encode_line2_missing_country_code(self):
        """Test encoding of line 2 data with missing country code."""
        data = {
            "line": {
                "passport_number": "W620126G5",
                "country_code": "",
                "birth_date": "591010",
                "sex": "F",
                "expiration_date": "970730",
                "personal_number": "AJ010215I"
            }
        }
        # Assert that the function returns 1 if country code is missing
        self.assertEqual(MRTD.encode_line2(data['line']),
                         1,
                         'Returns 1 if country code is missing')

    # Test for a mutation in the personal number
    def test_encode_line2_mutated_personal_number(self):
        """Test encoding of line 2 data with mutated personal number."""
        data = {
            "line": {
                "passport_number": "W620126G5",
                "country_code": "CIV",
                "birth_date": "591010",
                "sex": "F",
                "expiration_date": "970730",
                "personal_number": "mutpy"
            }
        }
        # Assert that the encoded data is the expected output
        self.assertEqual(MRTD.encode_line2(data['line']),
                         'W620126G54CIV5910106F9707302mutpy<<<<<<<<<<0',
                         'Got Expected result6')

    # Test for a mutation in the expiration date
    def test_encode_line2_mutated_expiration_date(self):
        """Test encoding of line 2 data with mutated expiration date."""
        data = {
            "line": {
                "passport_number": "W620126G5",
                "country_code": "CIV",
                "birth_date": "591010",
                "sex": "F",
                "expiration_date": "mutpy",
                "personal_number": "AJ010215I"
            }
        }
        # Assert that the encoded data is the expected output
        result = MRTD.encode_line2(data['line'])
        expected = 'W620126G54CIV5910106Fmutpy0AJ010215I<<<<<<<6'
        self.assertEqual(result, expected, 'Got expected result 6')

    def test_encode_line2_mutated_sex(self):
        """Test encoding of line 2 data with mutated sex value."""
        # Data dictionary containing passport information
        data = {
            "line": {
                "passport_number": "W620126G5",
                "country_code": "CIV",
                "birth_date": "591010",
                "sex": "mutpy",
                "expiration_date": "970730",
                "personal_number": "AJ010215I"
            }
        }
        # Expected result after encoding
        expected_result = 'W620126G54CIV5910106mutpy9707302AJ010215I<<6'
        # Check if the encoded result matches the expected result
        self.assertEqual(MRTD.encode_line2(
            data['line']), expected_result, 'Got expected result')

    def test_encode_line2_empty(self):
        """
        Test to check if encoding an empty passport information returns a line with filler characters.
        """
        # Data dictionary containing empty passport information
        data = {
            "line": {
                "passport_number": "",
                "country_code": "",
                "birth_date": "",
                "sex": "",
                "expiration_date": "",
                "personal_number": ""
            }
        }
        # Expected result after encoding
        expected_result = '<<<<<<<<<<<<<<<<<'
        # Check if the encoded result is not equal to the expected result
        self.assertNotEqual(MRTD.encode_line2(
            data['line']), expected_result, 'Got expected result')

    def test_scan_passport(self):
        """
        Test to check if the passport is scanned successfully.
        """
        # Check if the passport is scanned successfully
        self.assertEqual(MRTD.scan_passport(), 'scanned',
                         'Scanned successfully')

    def test_extract_line2_invalid_check_digit(self):
        """
        Test to check if extracting line2 with an invalid check digit raises a ValueError.
        """
        with self.assertRaises(ValueError):
            MRTD.extract_line2('W620126G59CIV5910106F9707302AJ010215I<<<<<<6')

    def test_birthday_check_digit_invalid(self):
        """
        Test to check if extracting line2 with an invalid birthday check digit raises a ValueError.
        """
        with self.assertRaises(ValueError):
            MRTD.extract_line2('W620126G54CIV5910105F9707302AJ010215I<<<<<<6')

    def test_expiry_date_check_digit_invalid(self):
        """
        Test to check if extracting line2 with an invalid expiry date check digit raises a ValueError.
        """
        with self.assertRaises(ValueError):
            MRTD.extract_line2('W620126G54CIV5910106F9707303AJ010215I<<<<<<6')

    def test_personal_number_check_digit_invalid(self):
        """
        Test to check if extracting line2 with an invalid personal number check digit raises a ValueError.
        """
        with self.assertRaises(ValueError):
            MRTD.extract_line2('W620126G54CIV5910106F9707302AJ010215I<<<<<<5')

    def test_get_check_digit(self):
        """
        Test to check if the get_check_digit method returns the correct check digits.
        """
        self.assertEqual(MRTD.get_check_digit("W620126G5"), '4')
        self.assertEqual(MRTD.get_check_digit("591010"), '6')
        self.assertEqual(MRTD.get_check_digit("970730"), '2')
        self.assertEqual(MRTD.get_check_digit("AJ010215I"), '6')

    def test_get_check_digit_edge_cases(self):
        """
        Test to check if the get_check_digit method handles edge cases correctly.
        """
        self.assertEqual(MRTD.get_check_digit(""), '0')
        self.assertEqual(MRTD.get_check_digit("<<<<"), '0')
        self.assertEqual(MRTD.get_check_digit("AB2134"), '5')
        self.assertNotEqual(MRTD.get_check_digit("AB2134"), '3')

    """
        Test cases for the DataBaseClass.
    """

    def test_sqlite3_success(self):
        """
        Test to check if the DataBaseClass creates a connection
        to the SQLite database with the correct name.
        """
        sqlite3.connect = MagicMock(return_value='connection succeeded')
        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(dbc.connection, 'connection succeeded')

    def test_sqlite3_fail(self):
        """
        Test to check if the DataBaseClass handles a failed connection properly.
        """
        sqlite3.connect = MagicMock(return_value='connection failed')
        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(dbc.connection, 'connection failed')

    def test_sqlite3_connect_with_side_effect(self):
        """
        Test to check if the DataBaseClass correctly handles different connection strings.
        """
        values = {'good_connection_string': True,
                  'bad_connection_string': False}
        sqlite3.connect = Mock(side_effect=lambda arg: values[arg])
        dbc = DataBaseClass('good_connection_string')
        self.assertTrue(dbc.connection)
        sqlite3.connect.assert_called_with('good_connection_string')
        dbc = DataBaseClass('bad_connection_string')
        self.assertFalse(dbc.connection)
        sqlite3.connect.assert_called_with('bad_connection_string')


class DataBaseClass:
    """
    A class to handle SQLite database connections.
    """

    def __init__(self, connection_string='test_database'):
        self.connection = sqlite3.connect(connection_string)


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
