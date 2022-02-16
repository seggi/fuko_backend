
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

    def global_computation(self, item_data):
        data = item_data['data']
        pass
