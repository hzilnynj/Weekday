from datetime import datetime, timedelta
import unittest

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
def days_in_month(month, year):
    days_map = {
        1: 31, 3: 31, 5: 31, 7: 31, 8: 31, 10: 31, 12: 31,
        4: 30, 6: 30, 9: 30, 11: 30,
        2: 28
    }
    return days_map[month]
    
def count_leap_years_up_to(year, month):
    """ Return the number of leap years up to the given year based on the month """
    if month > 2:
        leap_years = year // 4 - year // 100 + year // 400
    else:
        leap_years = (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400
    
    return leap_years

def get_days_between_dates(start_date, end_date):
    """Count the number of days between two dates."""

    year1, month1, day1 = start_date.year, start_date.month, start_date.day
    year2, month2, day2 = end_date.year, end_date.month, end_date.day
    
    # Calculate the number of days before start_date and end_date
    days_before_date1 = year1 * 365 + day1 + count_leap_years_up_to(year1, month1)

    for m in range(1, month1):
        days_before_date1 += days_in_month(m, year1)

    days_before_date2 = year2 * 365 + day2 + count_leap_years_up_to(year2, month2)
    
    for m in range(1, month2):
        days_before_date2 += days_in_month(m, year2)
        
    return days_before_date2 - days_before_date1

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

    total_days = get_days_between_dates(start_date, end_date) + 1
    
    full_weeks = total_days // 7
    remaining_days = end_date.weekday() - start_date.weekday() + 1

    # Adjust remaining_days if end_date is earlier in the week than start_date
    if remaining_days != 0 and end_date.weekday() < start_date.weekday():
        remaining_days = 5 + remaining_days

    return full_weeks * 5 + remaining_days


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

    def test_leap_year_span(self):
        start_date = datetime(2020, 1, 1)  # Leap year start
        end_date = datetime(2024, 12, 31)  # Leap year end
        self.assertEqual(count_weekdays(start_date, end_date), 1305)  # Includes 4 leap years (2020, 2024)
        
    def test_weekend_span(self):
        start_date = datetime(2024, 6, 28)  # Friday
        end_date = datetime(2024, 7, 1)     # Monday
        self.assertEqual(count_weekdays(start_date, end_date), 2)  



if __name__ == '__main__':
    unittest.main()
