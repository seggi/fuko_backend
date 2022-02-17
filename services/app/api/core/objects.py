
class GlobalAmount:
    tbl_names = ['expenses', 'loans', 'savings', 'depts']

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
            lists2.append(item['amount'])

        data = {
            self.tbl_names[0]:  sum(lists),
            self.tbl_names[1]:  sum(lists1),
            self.tbl_names[2]:  sum(lists2),
            self.tbl_names[3]:  sum(lists3)
        }

        return data
