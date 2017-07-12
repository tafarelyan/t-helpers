import sys
import unittest
import datetime

sys.path.append('.')
import helpers.time_functions as htf


class TimeFunctionsTests(unittest.TestCase):

    def test_str_to_datetime(self):
        time = htf.str_to_datetime('11:45')
        self.assertEqual(time.time(), datetime.time(11, 45))

    def test_time_difference(self):
        self.assertEqual(htf.time_difference('11:45', '23:45'), '12:00')
        self.assertEqual(htf.time_difference('11:30', '23:45'), '12:15')

    def test_time_to_str(self): 
        time = htf.datetime_to_str(datetime.time(11, 45))
        self.assertEqual(time, '11:45')
