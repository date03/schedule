import datetime
import calendar


def settoday():
    # return datetime.date(2021, 9, 18)
    return datetime.date.today()


def std_date():
    today = settoday()
    date = today - datetime.timedelta(days=today.day-1)
    if(today.month != (today - datetime.timedelta(days=today.weekday() - 6)).month):
        date += datetime.timedelta(days=calendar.monthrange(date.year,
                                                            date.month)[1])
    thismonth_num = date

    date += datetime.timedelta(days=calendar.monthrange(date.year,
                                                        date.month)[1])
    nextmonth_num = date

    date += datetime.timedelta(days=calendar.monthrange(date.year,
                                                        date.month)[1])
    aftermonth_nume = date

    # 今月の開始日　来月の開始日　再来月の開始日　
    return thismonth_num, nextmonth_num, aftermonth_nume


def check_date(a=14):  # 何日前までスケジュールの登録を受け付けるか
    today = settoday()
    date = today - datetime.timedelta(days=today.day-1)
    if(today.month != (today - datetime.timedelta(days=today.weekday() - 6 - a)).month):
        date += datetime.timedelta(days=calendar.monthrange(date.year,
                                                            date.month)[1])
    date += datetime.timedelta(days=calendar.monthrange(date.year,
                                                        date.month)[1])
    date -= datetime.timedelta(days=date.weekday())
    date -= datetime.timedelta(days=a+1)

    month = date + \
        datetime.timedelta(days=calendar.monthrange(date.year, date.month)[1])

    return month.month, date-today


def create_date(date):
    month1 = date - datetime.timedelta(days=date.weekday())
    date += datetime.timedelta(days=calendar.monthrange(date.year,
                                                        date.month)[1])
    month2 = date - datetime.timedelta(days=date.weekday())
    month = []
    while(month1 < month2):
        month.append(month1)
        month1 += datetime.timedelta(days=1)
    return month


def start_date(date):
    return date - datetime.timedelta(days=date.weekday())


def form_date(days, std=7):  # 変更可能な日付を抽出
    std_day = settoday() + datetime.timedelta(days=std)
    sub_day = days[-1]-std_day
    if std_day <= days[0]:
        return [(i, i.strftime("%m/%d")) for i in days]
    elif sub_day.days <= 0:
        return [(datetime.date(2000, 1, 1), "変更することはできません")]
    else:
        days = [std_day+datetime.timedelta(days=i)
                for i in range(sub_day.days+1)]
        return [(i, i.strftime("%m/%d")) for i in days]


def che_date(str_date):
    spdate = str_date.split("-")
    return datetime.date(int(spdate[0]), int(spdate[1]), int(spdate[2]))


def errorday():
    return datetime.date(2000, 1, 1)
