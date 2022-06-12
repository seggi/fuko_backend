import pandas as pd
from datetime import datetime


class ComputeRentPayment:
    def __init__(self, amount=None, payment_option=None, date=None, month=None, year=None):
        self.amount = amount
        self.payment_option = payment_option
        self.today = datetime.now()
        self.last_paid_date = date
        self.last_month = self.get_month_year_paid(month=month, year=year)

    def get_last_paid_date(self, date) -> datetime:
        date_list = list.append(date)
        new_date = pd.DatetimeIndex(date_list).date.tolist()
        return new_date[0]

    def get_month_year_paid(self, month=None,  year=None) -> dict:
        month_year = {"month": month, "year": year}
        return month_year

    def generate_date(self, year=None, month=None, date=None) -> datetime:
        receive_year: int = year
        receive_month: int = month
        receive_date: int = date
        today_date: datetime = datetime.datetime(
            receive_year, receive_month, receive_date)

        return today_date

    def count_unpaid_months(self) -> int:
        today = self.generate_date(year=int(self.today.strftime("%Y")), month=int(
            self.today.strftime("%m")), date=int(self.today.strftime("%m")))
        last_date_paid = self.get_last_paid_date(date=self.last_paid_date)

        num_months = (today.year - last_date_paid.year) * \
            12 + (today.month - last_date_paid.month)

        return num_months
