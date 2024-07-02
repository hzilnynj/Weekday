from datetime import datetime, timedelta
import unittest

def is_weekday(dt):
    """ Check if a date is weekday """
    return dt.weekday() < 5

def count_weekdays(start_date, end_date):
    """Count number of weekdays between start_date and end_date (inclusive)."""
    count = 0
    dt = start_date
    
    while dt <= end_date:
        if is_weekday(dt):
            count += 1
        dt += timedelta(days=1)
    
    return count

class TestWeekdays(unittest.TestCase):

    def test_same_day(self):
        start_date = datetime(2024, 7, 1)
        end_date = datetime(2024, 7, 1)
        self.assertEqual(count_weekdays(start_date, end_date), 1)

    def test_single_month(self):
        start_date = datetime(2024, 6, 1)
        end_date = datetime(2024, 6, 30)
        self.assertEqual(count_weekdays(start_date, end_date), 20)

    def test_crossing_month(self):
        start_date = datetime(2024, 6, 20)
        end_date = datetime(2024, 7, 5)
        self.assertEqual(count_weekdays(start_date, end_date), 12)

    def test_crossing_year(self):
        start_date = datetime(2023, 12, 31)
        end_date = datetime(2024, 1, 1)
        self.assertEqual(count_weekdays(start_date, end_date), 1)
        
    def test_only_weekends(self):
        start_date = datetime(2024, 6, 29)  # Saturday
        end_date = datetime(2024, 6, 30)     # Sunday
        self.assertEqual(count_weekdays(start_date, end_date), 0)

if __name__ == '__main__':
    unittest.main()
