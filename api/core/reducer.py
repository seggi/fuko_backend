from types import new_class


class Reducer:
    def __init__(self, list_items=[]) -> None:
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

    def new_collection_data(self):
        collect_ids = []
        for elements in self.list_items:
            for element in elements:
                if elements[element] == elements['id']:
                    collect_ids.append(str(elements['id']))
        return collect_ids

    def group_same_value(self):
        new_list = []
        for item in list(set(self.new_collection_data())):
            new_list.append({"id": item, "amount": []})

        for items in self.list_items:
            for elements in new_list:
                if str(items['id']) in elements["id"]:
                    lists = []
                    elements['amount'].append(items["amount"])
                    for element in elements['amount']:
                        lists.append(element)
                    elements['total_amount'] = sum(lists)

        return new_list

    def compute_paid_unfinished_payment(self, unpaid_amounts=[]):
        new_list = []

        for unpaid in unpaid_amounts:
            if str(unpaid['id']) not in list(set(self.new_collection_data())):
                new_list.append(
                    {'id': unpaid['id'], 'amount': unpaid['amount']})

            for unfinished in self.group_same_value():
                if unpaid['id'] == int(unfinished['id']):
                    remaining_amount = unpaid['amount'] - \
                        unfinished['total_amount']
                    new_list.append(
                        {'id': unpaid['id'], 'amount': remaining_amount})

        return new_list
