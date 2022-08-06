import random


class ComputePaymentAmount:
    def __init__(self, request_amount: float = None, db_amount: list = None, updated_amount_db: list = None):
        self.request_amount = request_amount
        self.db_amount = db_amount
        self.new_dict: dict = dict()
        self.new_list: list = list()
        self.updated_amount_db = updated_amount_db

    def check_and_compute(self, amount_list=[], incoming_amount: float = None):
        initial_amount: float = 0.0
        amount_paid: float = 0.0
        new_list = []
        collected_data = []

        for amount in amount_list:
            if amount['amount'] <= float(incoming_amount):
                collected_data.append(amount)

        for amount in collected_data:
            initial_amount += amount['amount']
            if float(initial_amount) <= float(incoming_amount):
                amount_paid = initial_amount
                new_list.append(amount)

        return [
            {'amount_paid': amount_paid},
            {'data': new_list},
            {'incoming_amount': incoming_amount}
        ]

    def compute_db_amount(self) -> list:
        # Initials
        compute_sum = []
        for amount in self.db_amount:
            compute_sum.append(amount['amount'])
        amount_sum = sum(compute_sum)

        if self.request_amount <= amount_sum:
            new_data = self.check_and_compute(
                amount_list=self.db_amount,
                incoming_amount=self.request_amount)

            amount_paid = new_data[0]['amount_paid']
            data_list = new_data[1]['data']
            data_amount = new_data[2]['incoming_amount']

            sub = self.sub_amount(
                amount_paid=amount_paid,
                updated_amount_db=self.updated_amount_db)

            if data_amount == 0:
                return [{"Alert": f"You can not pay {data_amount} amount"}]

            if data_amount == self.request_amount and len(data_list) == 0:
                single_process = self.single_payment(
                    incoming_amount=data_amount,
                    amount_list=self.db_amount
                )

                return {
                    "with_remain_amount": single_process,
                    "without_remain_amount": new_data
                }

            if len(sub) > 0:
                amount_paid = sub[0]['amount_paid']

                sub_amount_incoming = sub[2]['incoming_amount']
                sub_list = sub[1]['data']

                if sub_amount_incoming == 0:
                    return [{"Alert": f"You can not pay {sub_amount_incoming } amount"}]

                if sub_amount_incoming != 0.0 and len(sub_list) == 0:
                    single_process = self.single_payment(
                        incoming_amount=sub_amount_incoming,
                        amount_list=self.db_amount
                    )
                    return {
                        "with_remain_amount": single_process,
                        "without_remain_amount": new_data
                    }

            return {
                "with_remain_amount": sub,
                "without_remain_amount": new_data
            }

        return [{'Alert': f"You entered {self.request_amount} witch is more than the dept, with is {amount_sum} "}]

    def single_payment(self, incoming_amount=None, amount_list=[]) -> dict:
        collect_data = []

        for amount in amount_list:
            if float(incoming_amount) <= float(amount['amount']):
                collect_data.append(amount)

        get_random_data = random.choice(collect_data)
        return {"id": get_random_data['id'], 'amount': incoming_amount}

    def sub_amount(self, amount_paid=None, updated_amount_db=None):
        empty_list = []
        amount_remain = self.request_amount - amount_paid

        if amount_remain == 0:
            return empty_list

        if amount_remain > 0:
            new_data = self.check_and_compute(
                amount_list=updated_amount_db,
                incoming_amount=amount_remain
            )
            return new_data
        return empty_list
