
class QueryGlobalRepport:
    def __init__(self) -> None:
        pass

    def join_2_table_by_id(self, db, model1, model2, user_id):
        all_amount = db.session.query(model1, model2).join(
            model2, model1.id == model2.user_id, isouter=True).filter(model1.id == user_id).first()
        return all_amount

    def get_all_joined_table_by_id(self, db, model1, model2, user_id):
        all_amount = db.session.query(model1, model2).join(
            model2, model1.id == model2.user_id, isouter=True).filter(model1.id == user_id).all()
        return all_amount

    def insert_data(self, db, table_data):
        db.session.add(table_data)
        db.session.commit()
        return

    def get_row(self, db,  model, user_id):
        # Checking for user 4 other mode except User model
        user = model.query.filter_by(user_id=user_id).first()
        return user

    def get_data(self, db,  model, user_id):
        # Checking for user 4 other mode except User model
        user = model.query.filter_by(user_id=user_id).all()
        return user
