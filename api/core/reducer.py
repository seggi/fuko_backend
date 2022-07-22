class Reducer:
    def __init__(self, list_items) -> None:
        self.list_items: list = list_items
        self.row_dicts: list = []

    def collect_data(self):
        for elements in self.list_items:
            for element in elements:
                self.row_dicts.append(element)
        return self.row_dicts

    def reduce_list(self) -> list:
        new_list: list = []
        for key in list(set(self.collect_data())):
            new_list.append({"month": key, "data": []})

        for items in self.list_items:
            for item in items:
                for elements in new_list:
                    if item in elements["month"]:
                        lists = []
                        elements['data'].append(items[item])
                        for element in elements['data']:
                            lists.append(element["amount"])
                        elements['total_amount'] = sum(lists)
                break
        return new_list
