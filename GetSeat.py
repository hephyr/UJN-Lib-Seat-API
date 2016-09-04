# -*- coding: utf-8 -*-

import json
import datetime
import requests



def getToken():
    while True:
        # std_num = 220141222001
        # std_pass = 220141222001
        std_num = raw_input('账号:')
        std_pass = raw_input('密码:')
        url = 'http://seat.ujn.edu.cn/rest/auth?username=%s&password=%s' % (std_num, std_pass)
        r = requests.get(url)
        page_json = json.loads(r.text)
        if page_json['status'] == 'success':
            return page_json['data']['token']
        else :
            print '登录错误'


def checkToken(token):
    url = 'http://seat.ujn.edu.cn/rest/v2/user/reservations?token=%s' % token
    r = requests.get(url)
    page = r.text
    if page.find('success') == -1:
        return False
    else :
        return True

def getBuildingsInfo(token):
    url = 'http://seat.ujn.edu.cn/rest/v2/room/stats2/2?token=%s' % token
    r = requests.get(url)
    page_json = json.loads(r.text)
    if page_json['status'] == 'success':
        for value in page_json['data']:
            print 'id:', value['roomId'], value['room'], '楼层:', value['floor'], ' 剩余:', value['free']
    else:
        print '获取信息失败'

def getSeatInfo(token, seat, date):
    to21clock = False

    begtimeurl = 'http://seat.ujn.edu.cn/rest/v2/startTimesForSeat/%s/%s?token=%s' % (seat, date, token)
    begpage = requests.get(begtimeurl)
    page_json = json.loads(begpage.text)
    startlist = page_json['data']['startTimes']

    hour = '480'

    if date == datetime.date.today():
        hour = (datetime.datetime.today() + datetime.timedelta(hours=1)).hour
        hour = str(hour * 60)
    endtime = 1260
    if startlist:
        try :
            time = startlist[1]['id']
        except BaseException:
            return False

        if time == hour:
            for data in startlist[:0:-1]:
                time = data['id']
                if time != str(endtime):
                    break
                else:
                    endtime -= 60
            else:
                to21clock = True
    else:
        print '○',
    return to21clock


def layoutByDate(token, roomId, date):
    url = 'http://seat.ujn.edu.cn/rest/v2/room/layoutByDate/%s/%s/?token=%s' % (roomId, date, token)
    r = requests.get(url)
    page_json = json.loads(r.text)
    if page_json['status'] != 'success':
        return False
    data = page_json['data']
    print data['name']
    layout = data['layout']

    l = [layout[x] for x in layout if layout[x]['type'] == 'seat']
    l = sorted(l, key=lambda x:x['name'])

    d = {}
    for i in l:
        print '座位号:', i['name'], '是否可预约到21点:',
        d[i['name']] = i['id']
        if getSeatInfo(token, i['id'],date):
            print '✓'
        else:
            print ''
    
    return d

def getMaxTime(token):
    url = 'http://seat.ujn.edu.cn/rest/v2/allowedHours?token=%s' % token
    r = requests.get(url)
    page = r.text
    print page

def getHistory(token):
    #1是页数从1开始 10为每页显示个数
    url = 'http://seat.ujn.edu.cn/rest/v2/history/1/10?token=%s' % token
    r = requests.get(url)
    page = r.text
    print page

def quickBook(token):
    hour = raw_input('预约时长:')
    post_data = {
        "token" : token,
        "building" : "2",
        "hour" : hour
    }
    url = 'http://seat.ujn.edu.cn/rest/v2/quickBook'
    r = requests.post(url, post_data)
    page_json = json.loads(r.text)
    if page_json['status'] != 'success':
        print '预约失败', page_json['message']
    else:
        print '日期: ', page_json['data']['reservation']['onDate']
        print '开始时间: ', page_json['data']['reservation']['begin']
        print '结束时间: ', page_json['data']['reservation']['end']
        print '地点: ', page_json['data']['reservation']['location']
        print '!!!请及时签到!!!'

def getSeat(token):
    date = datetime.date.today()
    strdate = date.strftime('%Y-%m-%d')
    getBuildingsInfo(token)
    roomId = raw_input('room id :')
    while True:
        print '1. 今天'
        print '2. 明天'
        a = raw_input()
        if a == '1':
            break
        elif a == '2':
            date += datetime.timedelta(days=1)
            strdate = date.strftime('%Y-%m-%d')
            break
        else:
            print '输入错误'
    seat_dict = layoutByDate(token, roomId, date)
    while True:
        seat = raw_input('输入座位号:')
        if len(seat) < 3:
            zero = (3 - len(seat)) * '0'
            seat = zero + seat
        if seat not in seat_dict.keys():
            print '座位号错误'
        else:
            break
    while True:
        startTime = int(raw_input('输入开始时间 (7:00输入7    20:00输入20   最晚22)'))
        
        if date == datetime.date.today():
            hour = datetime.datetime.today()
            hour = int(hour.strftime('%H'))
            if startTime < hour or hour > 22:
                print '输入错误'
            else:
                break
        else :
            if startTime < 7 or startTime > 22:
                print '输入错误'
            else:
                break

    startTime *= 60
    startTime = str(startTime)
    post_data = {
        'token': token,
        'startTime' : startTime,
        'endTime' : '1320',
        'seat' : seat_dict[seat],
        'date' : date
    }
    # print post_data

    url = 'http://seat.ujn.edu.cn/rest/v2/freeBook'
    r = requests.post(url, post_data)
    page_json = json.loads(r.text)
    if page_json['status'] != 'success':
        print page_json['message']
    else:
        print '预约成功'

def checkIn(token):
    url = 'http://seat.ujn.edu.cn/rest/v2/checkIn?token=%s' % token
    r = requests.get(url)
    page_json = json.loads(r.text)
    print page_json
    if page_json['status'] != 'success':
        print page_json['message']
    else:
        print '签到成功', page_json['message']

def stop(token):
    url = 'http://seat.ujn.edu.cn/rest/v2/stop?token=%s' % token
    r = requests.get(url)
    print r.text

def menu():
    menu = '''
1. 快速预约
2. 自选座位
3. 结束使用
4. 签到
5. 查看楼层信息
9. 退出登录
0. 退出程序

请输入编号
    '''
    return menu

if __name__ == '__main__':
    need_login = True
    token = 'null'
    while True:
        if need_login:
            token = getToken()
            need_login = False

        if not checkToken(token):
            print 'token error, 请重新登录'
            need_login = True
            continue

        a = raw_input(menu())
        if a == '0':
            exit()
        elif a == '9':
            need_login = True
        elif a == '1':
            quickBook(token)
        elif a == '2':
            getSeat(token)
        elif a == '3':
            stop(token)
        elif a == '4':
            checkIn(token);
        elif a == '5':
            getBuildingsInfo(token)
        else:
            print '输入错误, 请重新输入'

