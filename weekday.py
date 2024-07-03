from datetime import datetime, timedelta
import unittest

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def days_in_month(month, year):
    days_map = {
        1: 31, 3: 31, 5: 31, 7: 31, 8: 31, 10: 31, 12: 31,
        4: 30, 6: 30, 9: 30, 11: 30,
        2: 29 if is_leap_year(year) else 28
    }
    return days_map[month]

def get_days_between_dates(start_date, end_date):
    """Count the number of days between two dates."""
    
    year1, month1, day1 = start_date.year, start_date.month, start_date.day
    year2, month2, day2 = end_date.year, end_date.month, end_date.day

    days = 0

    
    if year1 == year2:
        
        # When dates are in the same year
        if month1 == month2:
            days += day2 - day1
        else:
            days += days_in_month(month1, year1) - day1
            month1 += 1
            while month1 < month2:
                days += days_in_month(month1, year1)
                month1 += 1
            days += day2
            
    else:
        # Calculate number of days within start and end year
        days += days_in_month(month1, year1) - day1
        month1 += 1
        while month1 <= 12:
            days += days_in_month(month1, year1)
            month1 += 1
        month2 -= 1
        while month2 >= 1:
            days += days_in_month(month2, year2)
            month2 -= 1
        days += day2
        
        # Calculate number of years
        year1 += 1
        while year1 < year2:
            if is_leap_year(year1):
                days += 366
            else:
                days += 365
            year1 += 1

    return days

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
    total_days = get_days_between_dates(start_date, end_date) + 1
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
