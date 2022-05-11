from database import User, UserPosition, db


def store_member(user_number):  # 引数に関連するすべての従業員番号を取得
    return UserPosition.query.filter_by(store_number=UserPosition.query.filter_by(user_number=user_number).one_or_none().store_number).with_entities(UserPosition.user_number).filter(db.or_(UserPosition.cook == True, UserPosition.front == True)).order_by(UserPosition.user_number)


def member_list(user_number):  # 従業員番号とその使命をセットで出力
    return_obj = [(None, "選択してください")]
    for user_number in [i[0] for i in store_member(user_number).all()]:
        user_name = User.query.filter_by(user_number=user_number).one_or_none()
        return_obj.append((user_number, user_number+" " +
                           user_name.user_lname+user_name.user_fname))
    return return_obj
