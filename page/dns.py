"""デニーズ関連のページ"""

from form.dayscheduleform import DayScheduleForm
from form.createuserform import CreateUserForm
from database import DaySchedule, DnsNews, StdSchedule, StoreSchedule, UserLogin, UserPosition, UserSchedule, db, User
from flask import Blueprint, render_template, request, redirect, abort
import flask_login
from module import num_name_set, trans_date, create_password
from form import *

dns_app = Blueprint("dns", __name__)


@dns_app.route("/dns", methods=['GET'])  # デニーズ関連のトップページ
@flask_login.login_required
def dns():
    thismonth_num, nextmonth_num, _ = trans_date.std_date()
    news = DnsNews.query.filter_by(
        store_number=UserPosition.query.filter_by(user_number=flask_login.current_user.user_number).one_or_none().store_number).order_by(DnsNews.id.desc()).all()
    return render_template("dns/dns.html", all_news=news, deadline=trans_date.check_date(), thismonth_num=thismonth_num.month, nextmonth_num=nextmonth_num.month)


@dns_app.route("/dns/news/<news_id>", methods=['GET'])  # 店舗別ニュースの詳細ページ
@flask_login.login_required
def dns_news(news_id=None):
    news = DnsNews.query.filter_by(id=news_id).first()
    if news_id == None or news == None:
        abort(404)
    create_user = User.query.filter_by(
        user_number=news.user_number).first()
    return render_template('dns/news.html', news=news, create_user=create_user.user_lname+create_user.user_fname)


@dns_app.route("/dns/schedule", methods=['GET', 'POST'])  # スケジュール登録ページ
@flask_login.login_required
def dns_schedule():
    deadline = trans_date.check_date()
    userschedule = UserSchedule.query.filter_by(
        user_number=flask_login.current_user.user_number, month=deadline[0])
    form = MonthScheduleForm(request.form)
    if form.validate_on_submit():
        userschedule_m = UserSchedule.query.filter_by(  # 既に登録してあるデータがあれば入手
            user_number=flask_login.current_user.user_number, month=deadline[0], w_m='m', week=form.week.data).one_or_none()
        userschedule_w = UserSchedule.query.filter_by(
            user_number=flask_login.current_user.user_number, month=deadline[0], w_m='w', week=form.week.data).one_or_none()

        if userschedule_m == None:
            userschedule_m = UserSchedule(flask_login.current_user.user_number,
                                          deadline[0], 'm', form.week.data, form.m_s_h.data, form.m_s_m.data, form.m_e_h.data, form.m_e_m.data)
        else:
            userschedule_m.commit_t(
                form.m_s_h.data, form.m_s_m.data, form.m_e_h.data, form.m_e_m.data)

        if userschedule_w == None:
            userschedule_w = UserSchedule(flask_login.current_user.user_number,
                                          deadline[0], 'w', form.week.data, form.w_s_h.data, form.w_s_m.data, form.w_e_h.data, form.w_e_m.data)
        else:
            userschedule_w.commit_t(
                form.w_s_h.data, form.w_s_m.data, form.w_e_h.data, form.w_e_m.data)

        try:  # スケジュールをDBに登録
            db.session.add(userschedule_m)
            db.session.add(userschedule_w)
            db.session.commit()
        except:
            return redirect("/redirect?status=monthschedulefailure")
        return redirect("/redirect?status=monthschedulesuccess")

    return render_template("dns/schedule.html", deadline=deadline, form=form, userschedule=userschedule)


@dns_app.route("/dns/month/<th_ne>", methods=['GET', 'POST'])  # スケジュール出力
@flask_login.login_required
def dns_month(th_ne):
    form = DayScheduleForm(request.form)
    delform = DeleteDayScheduleForm(request.form)
    thismonth_num, nextmonth_num, _ = trans_date.std_date()
    if th_ne == "th":
        month_num = thismonth_num
    elif th_ne == "ne":
        month_num = nextmonth_num
    else:
        abort(404)
    month = trans_date.create_date(month_num)
    form.day.choices = trans_date.form_date(month)
    stdschedule = StdSchedule.query.filter_by(month=month_num.month).filter_by(
        user_number=flask_login.current_user.user_number)
    storeschedule = StoreSchedule.query.filter(db.and_(month[0] <= StoreSchedule.day, StoreSchedule.day <= month[-1])).filter_by(
        user_number=flask_login.current_user.user_number).order_by(StoreSchedule.s_hour)
    dayschedule = DaySchedule.query.filter_by(user_number=flask_login.current_user.user_number).filter(
        db.and_(max(month[0], trans_date.settoday()) <= DaySchedule.day, DaySchedule.day <= month[-1])).order_by(DaySchedule.day).all()
    if form.validate_on_submit():
        newdayschedule = DaySchedule(flask_login.current_user.user_number, trans_date.che_date(form.day.data),
                                     form.s_h.data, form.s_m.data, form.e_h.data, form.e_m.data)
        try:
            db.session.add(newdayschedule)
            db.session.commit()
        except:
            return redirect("/redirect?status=dayschedulefailure&next="+th_ne)
        return redirect("/redirect?status=dayschedulesuccess&next="+th_ne)
    elif delform.validate_on_submit():
        deldayschedule = DaySchedule.query.filter_by(
            id=delform.delid.data).one_or_none()
        try:
            db.session.delete(deldayschedule)
            db.session.commit()
        except:
            return redirect("/redirect?status=deldayschedulefailure&next="+th_ne)
        return redirect("/redirect?status=deldayschedulesuccess&next="+th_ne)

    return render_template("dns/tempmonth.html", stdschedule=stdschedule, storeschedule=storeschedule, dayschedule=dayschedule, month_num=month_num, month=month, form=form, delform=delform)


@dns_app.route("/dns/day/<month>/<day>", methods=['GET', 'POST'])  # スケジュール出力
@flask_login.login_required
def dns_day(month, day):
    return month+"/"+day


"""管理者専用ページ"""


@dns_app.route("/dns/admin", methods=['GET'])  # 管理者画面の一覧ページ
@flask_login.login_required
def dns_admin():
    if flask_login.current_user.dns_admin:  # 管理者権限のあるアカウント以外見れないように
        return render_template("dns/admin.html", deadline_admin=trans_date.check_date(7), deadline=trans_date.check_date())
    else:
        abort(404)  # 権限がなければエラーページへ


# 日別のスケジュールの管理・登録ページ
@dns_app.route("/dns/admin/dayschedule", methods=['GET', 'POST'])
@flask_login.login_required
def dns_admin_dayschedule():
    if flask_login.current_user.dns_admin:
        # フォーム類の読み込み
        form = SetDayScheduleForm(request.form)
        confform = ConfDayScheduleForm(request.form)
        delform = DeleteDayScheduleForm(request.form)
        # 基準日の読み込み
        thismonth_num, nextmonth_num, aftermonth_num = trans_date.std_date()
        # 選択できる日付一覧の生成
        month = trans_date.create_date(thismonth_num)
        month += trans_date.create_date(nextmonth_num)
        form.day.choices = trans_date.form_date(month, 1)
        # 従業員の一覧を取得
        form.user_number.choices = num_name_set.member_list(
            flask_login.current_user.user_number)
        store_member = [i[0] for i in num_name_set.store_member(
            flask_login.current_user.user_number).all()]
        # 従業員番号に該当する氏名を入手
        username = User.query.filter(User.user_number.in_(
            store_member)).with_entities(User.user_lname, User.user_fname)
        # DBから必要な部分の抽出
        dayschedule = DaySchedule.query.filter(DaySchedule.user_number.in_(store_member)).order_by(
            DaySchedule.day).filter(trans_date.settoday() <= DaySchedule.day).all()
        storeschedule = StoreSchedule.query.filter(db.and_(thismonth_num <= StoreSchedule.day, StoreSchedule.day < aftermonth_num)).filter(
            StoreSchedule.user_number.in_(store_member)).order_by(StoreSchedule.day)
        # 登録フォームのデフォルト値
        id = request.args.get("id")
        if id is not None:
            defadayschedule = DaySchedule.query.filter_by(
                id=id).filter(DaySchedule.user_number.in_(store_member)).one_or_none()
            if defadayschedule is not None:
                form.day.choices = [(defadayschedule.day, defadayschedule.day.strftime(
                    "%m/%d")), (trans_date.errorday, "------")] + form.day.choices
                form.user_number.data = defadayschedule.user_number
                form.s_h.data = defadayschedule.s_hour
                form.s_m.data = defadayschedule.s_minute
                form.e_h.data = defadayschedule.e_hour
                form.e_m.data = defadayschedule.e_minute
        # 登録のsubmitボタンが押されたとき
        if form.validate_on_submit():
            newstoreschdule = StoreSchedule(
                form.user_number.data, trans_date.che_date(form.day.data), form.s_h.data, form.s_m.data, form.e_h.data, form.e_m.data)
            try:
                db.session.add(newstoreschdule)
                db.session.commit()
            except:
                return redirect("/redirect?status=setdayschedulefailure")
            return redirect("/redirect?status=setdayschedulesuccess")
        # 確認のsubmitボタンが押されたとき
        elif confform.validate_on_submit() and confform.confid.data:
            confdayschedule = DaySchedule.query.filter_by(
                id=confform.confid.data).one_or_none()
            confdayschedule.configu()
            try:
                db.session.add(confdayschedule)
                db.session.commit()
            except:
                return redirect("/redirect?status=confsetdayschedulefailure")
            return redirect("/redirect?status=confsetdayschedulesuccess&next="+confform.confid.data)
        # 削除のsubmitボタンが押されたとき
        elif delform.validate_on_submit() and delform.delid.data:
            delstoreschedule = StoreSchedule.query.filter_by(
                id=delform.delid.data).one_or_none()
            try:
                db.session.delete(delstoreschedule)
                db.session.commit()
            except:
                return redirect("/redirect?status=delsetdayschedulefailure")
            return redirect("/redirect?status=delsetdayschedulesuccess")
        return render_template("dns/admin/dayschedule.html", dayschedule=dayschedule, storeschedule=storeschedule, username=username, form=form, confform=confform, delform=delform)
    else:
        abort(404)


# 月間の基本スケジュールの登録ページ
@ dns_app.route("/dns/admin/monthschedule", methods=['GET', 'POST'])
@ flask_login.login_required
def dns_admin_monthschedule():
    if flask_login.current_user.dns_admin:
        month = trans_date.check_date(7)[0]

        form = SetMonthScheduleForm(request.form)
        weekdayform = WeekDayForm(request.form)
        delform = DeleteMonthScheduleForm(request.form)
        form.user_number.choices = num_name_set.member_list(
            flask_login.current_user.user_number)
        if request.args.get("week") is not None:
            week = int(request.args.get("week"))
            choices = [weekdayform.week.choices[i]
                       for i in range(week, 7)]
            choices += [weekdayform.week.choices[i]
                        for i in range(0, week)]
            weekdayform.week.choices = choices
        else:
            week = 0

        store_member = num_name_set.store_member(
            flask_login.current_user.user_number)  # 現在ログインしている店舗のメンバー一覧を取得
        store_member = [i[0] for i in store_member.all()]  # そのうち従業員番号のみを抽出
        username = User.query.filter(User.user_number.in_(
            store_member)).with_entities(User.user_lname, User.user_fname)  # 従業員番号に該当する氏名を入手
        userposition = UserPosition.query.filter(
            UserPosition.user_number.in_(store_member))
        if form.validate_on_submit():
            new_schedule = StdSchedule(
                form.user_number.data, month, form.week.data, form.s_h.data, form.s_m.data, form.e_h.data, form.e_m.data)
            try:
                db.session.add(new_schedule)
                db.session.commit()
            except:
                return redirect("/redirect?status=setmonthschedulefailure&next="+str(form.week.data))
            return redirect("/redirect?status=setmonthschedulesuccess&next="+str(form.week.data))
        elif delform.validate_on_submit and delform.delid.data:
            delstdschedule = StdSchedule.query.filter_by(
                id=delform.delid.data).one_or_none()
            try:
                db.session.delete(delstdschedule)
                db.session.commit()
            except:
                return redirect("/redirect?status=delstdschedulefailure&next="+str(week))
            return redirect("/redirect?status=delstdschedulesuccess&next="+str(week))
        elif weekdayform.validate_on_submit and weekdayform.week.data:
            return redirect("/dns/admin/monthschedule?week="+str(weekdayform.week.data))
        monthschedule = StdSchedule.query.filter_by(week=week, month=month).filter(StdSchedule.user_number.in_(
            store_member)).filter(db.and_(StdSchedule.s_hour != "--", StdSchedule.e_hour != "--")).order_by(StdSchedule.s_hour)
        return render_template("dns/admin/monthschedule.html", form=form, weekdayform=weekdayform, delform=delform, username=username, userposition=userposition, monthschedule=monthschedule)
    else:
        abort(404)


# 月間の基本スケジュールの確認ページ
@ dns_app.route("/dns/admin/getmonthschedule", methods=['GET', 'POST'])
@ flask_login.login_required
def dns_admin_getmonthschedule():
    if flask_login.current_user.dns_admin:
        form = GetMonthScheduleForm(request.form)
        deadline_admin = trans_date.check_date(7)
        form.month.choices.append(
            (deadline_admin[0], deadline_admin[0]))  # 選択肢のデフォルト値に今月をセット
        form.month.choices.append((None, "--"))  # 分かりやすいように横線を追加(選んでも何も出ない)
        thismonth_num, nextmonth_num, aftermonth_nume = trans_date.std_date()
        for i in [thismonth_num, nextmonth_num, aftermonth_nume]:
            form.month.choices.append((i.month, i.month))  # 他の曜日も選択できるように
        store_member = num_name_set.store_member(  # 特定の店番の従業員番号をすべて取得
            flask_login.current_user.user_number)
        if form.validate_on_submit():
            if form.position.data == 'cook':  # 役職で絞り込み
                store_member = store_member.filter_by(cook=True)
            if form.position.data == 'front':
                store_member = store_member.filter_by(front=True)
        store_member = [i[0] for i in store_member.all()]  # 従業員番号のみ抽出
        username = User.query.filter(User.user_number.in_(
            store_member)).with_entities(User.user_lname, User.user_fname)  # 該当する氏名を入手
        userposition = UserPosition.query.filter(
            UserPosition.user_number.in_(store_member))
        monthschedule = UserSchedule.query.filter(
            UserSchedule.user_number.in_(store_member)).filter(db.and_(UserSchedule.s_hour != "--", UserSchedule.e_hour != "--")).order_by(UserSchedule.s_hour)
        if form.validate_on_submit():
            monthschedule = monthschedule.filter_by(
                month=form.month.data, week=form.week.data)
            if form.time.data != "all":  # 特定の時間を含むスケジュールの入手
                monthschedule = monthschedule.filter(db.and_(
                    UserSchedule.s_hour <= form.time.data, form.time.data < UserSchedule.e_hour))
        else:
            monthschedule = monthschedule.filter_by(
                month=deadline_admin[0], week=0)  # 月曜日をデフォルトに設定
        return render_template("dns/admin/getmonthschedule.html", form=form, monthschedule=monthschedule, username=username, userposition=userposition)
    else:
        abort(404)


@ dns_app.route("/dns/admin/createnews", methods=['GET', 'POST'])  # ニュースの作成ページ
@ flask_login.login_required
def dns_admin_createnews():
    if flask_login.current_user.dns_admin:
        form = CreateNewsForm(request.form)
        if form.validate_on_submit():
            store_number = UserPosition.query.filter_by(
                user_number=flask_login.current_user.user_number).one_or_none().store_number
            dns_news = DnsNews(store_number, flask_login.current_user.user_number,
                               form.news_title.data, form.news_body.data)
            try:
                db.session.add(dns_news)
                db.session.commit()
            except:
                return redirect("/redirect?status=createnewsfailure")
            return redirect("/redirect?status=createnewssuccess")
        return render_template("dns/admin/createnews.html", form=form)
    else:
        abort(404)


@ dns_app.route("/dns/admin/createuser", methods=['GET', 'POST'])  # ユーザの作成ページ
@ flask_login.login_required
def dns_admin_createuser():
    if flask_login.current_user.dns_admin:
        form = CreateUserForm(request.form)
        store_number = UserPosition.query.filter_by(
            user_number=flask_login.current_user.user_number).one_or_none().store_number
        if form.validate_on_submit():  # 作成に必要な3種類のDBの作成
            new_user_u = User(form.user_number.data, form.user_lname.data,
                              form.user_fname.data, flask_login.current_user.user_number, form.dns_admin.data)
            new_user_p = UserPosition(
                form.user_number.data, store_number, form.cook.data, form.front.data)
            new_user_l = UserLogin(form.user_number.data, form.password.data)
            try:
                db.session.add(new_user_u)
                db.session.add(new_user_p)
                db.session.add(new_user_l)
                db.session.commit()
            except:
                return redirect("/redirect?status=createuserfailure")
            return redirect("/redirect?status=createusersuccess")
        form.password.data = create_password.pass_gen()  # パスワードのハッシュ化
        return render_template("dns/admin/createuser.html", form=form, store_number=store_number)
    else:
        abort(404)


@ dns_app.route("/dns/admin/employees", methods=['GET'])  # 従業員の一覧・変更ページ
@ flask_login.login_required
def dns_admin_employees():
    if flask_login.current_user.dns_admin:
        return render_template("dns/admin/employees.html")
    else:
        abort(404)
