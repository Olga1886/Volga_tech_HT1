from datetime import datetime
import re


def parse_date(date_str: str) -> datetime:
    # Define a regular expression pattern for different date formats
    patterns = [
        r'(\d{1,2})\s([A-Za-z]+)\s(\d{4}),\s(\d{1,2}):(\d{2})',
        r'(\d{1,2})\s([A-Za-z]+)\s(\d{4})',
        r'(\d{1,2})\/(\d{1,2})\/(\d{4})'
    ]

    for pattern in patterns:
        match = re.match(pattern, date_str)
        if match:
            try:
                if len(match.groups()) == 5:
                    day, month, year, hour, minute = match.groups()
                month_num = datetime.strptime(month, '%B').month if month.isalpha() else datetime.strptime(month,
                                                                                                           '%b').month
                return datetime(int(year), month_num, int(day), int(hour), int(minute))
                elif len(match.groups()) == 3 and date_str.replace('/', '').isdigit():
                day, month, year = match.groups()
                return datetime(int(year), int(month), int(day))
            elif len(match.groups()) == 3:
            day, month, year = match.groups()
            month_num = datetime.strptime(month, '%B').month if month.isalpha() else datetime.strptime(month,
                                                                                                       '%b').month
            return datetime(int(year), month_num, int(day))
    except ValueError:
    continue


raise ValueError(f"Unable to parse date from string: {date_str}")
