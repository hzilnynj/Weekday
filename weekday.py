from datetime import datetime, timedelta
import unittest

def count_weekdays(start_date, end_date):
    """Count number of weekdays between start_date and end_date (inclusive)."""
    
    # Define index of Friday (0=Monday, 6=Sunday)
    fri = 4  # Friday is represented as 4

    # Adjust start_date if it falls on a weekend
    if start_date.weekday() > fri:
        start_date += timedelta(days=7 - start_date.weekday())

    # Adjust end_date if it falls on a weekend
    if end_date.weekday() > fri:
        end_date -= timedelta(days=end_date.weekday() - fri)

    # No weekdays if adjusted start_date is after adjusted end_date
    if start_date > end_date:
        return 0

    # Convert to epoch then divide by 86400 seconds in a day
    total_days = int((end_date.timestamp() - start_date.timestamp()) / 86400) + 1
    full_weeks = total_days // 7
    remaining_days = total_days % 7

    # Calculate weekdays in the remaining days
    start_day_of_week = start_date.weekday()
    remaining_weekdays = remaining_days if start_day_of_week + remaining_days <= 4 else max(0, 5 - start_day_of_week)

    return full_weeks * 5 + remaining_weekdays

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
        
    def test_long_range(self):
        start_date = datetime(2000, 1, 1)  
        end_date = datetime(2024, 6, 30)     
        self.assertEqual(count_weekdays(start_date, end_date), 6390)

if __name__ == '__main__':
    unittest.main()
