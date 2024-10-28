import datetime

def is_start_date_greater_than_end_date(start_date, end_date):

    if(end_date is not None):
        return start_date > end_date
    else:
        return False