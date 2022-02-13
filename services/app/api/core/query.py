
class QueryGlobalRepport:
    def __init__(self) -> None:
        pass

    def join_2_table_by_id(self, db, model1, model2, user_id):
        all_amount = db.session.query(model1, model2).join(
            model2, model1.id == model2.user_id, isouter=True).filter(model1.id == user_id).first()
        return all_amount
