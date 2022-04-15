
NEW_LIST = []
# Retrieve dictionary according to 
class GlobalAmount:
    tbl_names = ['expenses', 'loans', 'savings', 'dept']

    def __init__(self, tbl1, tbl2, tbl3, tbl4) -> None:
        self.tbl1 = tbl1
        self.tbl2 = tbl2
        self.tbl3 = tbl3
        self.tbl4 = tbl4

    def out_put(self) -> dict[str, dict]:
        return {
            self.tbl_names[0]: self.tbl1,
            self.tbl_names[1]: self.tbl2,
            self.tbl_names[2]: self.tbl3,
            self.tbl_names[3]: self.tbl4,
        }

    # Retrieve && calculate all amount by category ,
    '''Expenses, Savings, Dept ans  Loans'''

    def computer_amount(self, item_list):
        lists = []
        lists1 = []
        lists2 = []
        lists3 = []
        for item in item_list[self.tbl_names[0]]:
            lists.append(item['amount'])

        for item in item_list[self.tbl_names[1]]:
            lists1.append(item['amount'])

        for item in item_list[self.tbl_names[2]]:
            lists2.append(item['amount'])

        for item in item_list[self.tbl_names[3]]:
            lists3.append(item['amount'])

        data = {
            self.tbl_names[0]:  sum(lists),
            self.tbl_names[1]:  sum(lists1),
            self.tbl_names[2]:  sum(lists2),
            self.tbl_names[3]:  sum(lists3),
        }

        negative_values = sum(lists + lists3)
        positive_values = sum(lists1 + lists2)

        calculate_all_amount = positive_values - negative_values

        return {
            "global_amount_details": data,
            "global_amount": calculate_all_amount
        }

class ManageQuery:
    def serialize_schema(self, query_list, schema):
        for item in query_list:
            NEW_LIST.append(schema.dump(item))
        return NEW_LIST
    
    def generate_total_amount(self, amount_list):
        for item in amount_list:
            NEW_LIST.append(item['amount'])
        return sum(NEW_LIST)