from database import User, UserLogin, UserPosition, db

if __name__ == "__main__":
    print("基本情報を入力")
    user_number = input("従業員番号：")
    user_lname = input("苗字：")
    user_fname = input("名前：")
    password = input("パスワード：")

    print("詳細情報を入力")
    store_number = input("店番：")
    while(1):
        inp_cook = input("キッチン業務ができますか(y/n)")
        if(inp_cook == "y"):
            cook = True
            break
        elif(inp_cook == "n"):
            cook = False
            break
        else:
            print("yかnで入力してください")
    while(1):
        inp_front = input("フロント業務ができますか(y/n)")
        if(inp_front == "y"):
            front = True
            break
        elif(inp_front == "n"):
            front = False
            break
        else:
            print("yかnで入力してください")

    user = User(user_number, user_lname, user_fname, create="master")
    userlogin = UserLogin(user_number, password)
    userposition = UserPosition(user_number, store_number, cook, front)

    try:
        db.session.add(user)
        db.session.add(userlogin)
        db.session.add(userposition)
        db.session.commit()
    except:
        print("問題が発生しました。入力内容を見直してください。")
        print("連続して失敗する場合管理者に問い合わせてください。")
        exit()
    print("正常に終了しました。")
