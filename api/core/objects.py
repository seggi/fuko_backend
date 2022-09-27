
NEW_LIST = []
# Retrieve dictionary according to


class GlobalAmount:
    tbl_names = ['expenses', 'loans', 'savings', 'dept',
                 'recorded-dept-paid', 'person_paid_loan', 'pub_paid_loan', 'pub_paid_dept', 'person_paid_dept', ]

    def __init__(self, tbl1, tbl2, tbl3, tbl4, tbl5, tbl6, tbl7, tbl8, tbl9) -> None:
        self.tbl1 = tbl1
        self.tbl2 = tbl2
        self.tbl3 = tbl3
        self.tbl4 = tbl4
        self.tbl5 = tbl5
        self.tbl6 = tbl6
        self.tbl7 = tbl7
        self.tbl8 = tbl8
        self.tbl9 = tbl9

    def out_put(self) -> dict[str, dict]:
        return {
            self.tbl_names[0]: self.tbl1,
            self.tbl_names[1]: self.tbl2,
            self.tbl_names[2]: self.tbl3,
            self.tbl_names[3]: self.tbl4,
            self.tbl_names[4]: self.tbl5,
            self.tbl_names[5]: self.tbl6,
            self.tbl_names[6]: self.tbl7,
            self.tbl_names[7]: self.tbl8,
            self.tbl_names[8]: self.tbl9,
        }

    # Retrieve && calculate all amount by category ,
    '''Expenses, Savings, Dept ans  Loans'''

    def computer_amount(self, item_list):
        lists = []
        lists1 = []
        lists2 = []
        lists3 = []
        lists4 = []
        lists5 = []
        lists6 = []
        lists7 = []
        lists8 = []
        for item in item_list[self.tbl_names[0]]:
            lists.append(item['amount'])

        for item in item_list[self.tbl_names[1]]:
            lists1.append(item['amount'])

        for item in item_list[self.tbl_names[2]]:
            lists2.append(item['amount'])

        for item in item_list[self.tbl_names[3]]:
            lists3.append(item['amount'])

        for item in item_list[self.tbl_names[4]]:
            lists4.append(item['amount'])

        for item in item_list[self.tbl_names[5]]:
            lists5.append(item['amount'])

        for item in item_list[self.tbl_names[6]]:
            lists5.append(item['amount'])

        for item in item_list[self.tbl_names[7]]:
            print(item['amount'])
            lists7.append(item['amount'])

        for item in item_list[self.tbl_names[8]]:
            lists8.append(item['amount'])

        data = {
            self.tbl_names[0]:  sum(lists),
            self.tbl_names[1]:  sum(lists1),
            self.tbl_names[2]:  sum(lists2),
            self.tbl_names[3]:  sum(lists3),
            self.tbl_names[4]:  sum(lists4),
            self.tbl_names[5]:  sum(lists5),
            self.tbl_names[6]:  sum(lists6),
            self.tbl_names[7]:  sum(lists7),
            self.tbl_names[8]:  sum(lists8),
        }

        negative_values = sum(lists + lists3)
        positive_values = sum(lists1 + lists2 + lists4 +
                              lists5 + lists6 + lists7 + lists8)

        calculate_all_amount = positive_values - negative_values
        collect_paid_loan = sum(lists5 + lists6)
        total_loan = sum(lists1) - collect_paid_loan

        collect_paid_dept = sum(lists7 + lists8)
        total_dept = sum(lists3) - collect_paid_dept

        return {
            "global_amount_details": data,
            "global_amount": calculate_all_amount,
            "total_loans": total_loan,
            "total_depts": total_dept,
            "total_expenses": sum(lists),
            "total_savings": sum(lists2)
        }


class ManageQuery:
    def serialize_schema(self, query_list, schema):
        for item in query_list:
            NEW_LIST.append(schema.dump(item))
            break
        return NEW_LIST

    def generate_total_amount(self, amount_list):
        lists = []
        save_amount = []
        for item in amount_list:
            lists.append(item)

        for item in lists:
            save_amount.append(item['amount'])

        return sum(save_amount)
