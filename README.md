# 济南大学图书馆座位预约系统API
_UJN Library Seat API for Python_

## 新版说明
新版服务器后端采用 HMAC 进行 API 认证，本人能力有限无法进行破解。目前采用复用 HMAC 的方式进行绕过（[参考 issue](https://github.com/iozephyr/UJN-Lib-Seat-API/issues/19#issuecomment-493819900)），建议使用本项目时替换源码 HTTP Header 的 HMAC 内容。

签到功能仍然可以使用。

## 说明
Python 版在 libapi 目录下

支持 Python 2 3 蛋疼的编码问题建议 Python 3

本人未参与任何金钱(PY)交易，项目仅供学习交流使用

这是个还不错的 `Python` `爬虫` `HTTP` `RESTful`（RESTful 其实也不正规） **学习**项目

我觉得你们还需要学习一个

本身专业是计算机的你们要是想占座可以开 issue 我教你们，但要是一点代码也不懂还是算了

收钱帮别人抢座太无耻了吧

### 想抢座位的戳[这里](https://github.com/iozephyr/UJN-Lib-Seat-API/issues/9)


### 用例
``` Python
$ cd path-to-UJN-Lib-Seat-API
$ python3
Python 3.7.0 (default, Jul 15 2018, 10:44:58) 
[GCC 8.1.1 20180531] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from libapi import *
>>> p = libapi("帐号", "密码")
```

# API

| API                                                 | 功能                           |
|-----------------------------------------------------|--------------------------------|
| getToken()                                          | 获取 token                     |
| reservations()                                      | 查看预约                       |
| user()                                              | 用户信息                       |
| filters()                                           | 图书馆信息                     |
| roomStats(building_id)                              | 楼层信息                       |
| seatStartTime(seat_id, date)                        | 座位开始时间                   |
| seatEndTime(seat_id, date, start_time)              | 根据座位开始时间得到的结束时间 |
| freeBook(start_time, end_time, seat_id, date)       | 预约座位                       |
| layoutByDate(room_id, date)                         | 查看阅览室信息                 |
| checkIn()                                           | 签到                           |
| history(page=1, count=10)                           | 查看历史                     |
| cancelRes(res_id)                                   | 取消预约                       |
| dates()                                             | 可预约日期列表                 |
| rooms()                                             | 阅览室信息                     |
| getSeatIDbyNum(room_id, seat_num)                   | 通过阅览室ID和座位号获取座位ID |
| getRoomIDbyName(room_name)                          | 通过阅览室名获取阅览室ID       |
| getRoomNamebyID(room_id)                            | 通过阅览室ID获取阅览室名       |
| seatInfo(room_id, seat_num)                         | 查看座位信息                   |
| book(start_time, end_time, room_id, seat_num, date) | 预约座位                       |
| isInUse()                                           | 查看帐号是否正在使用           |

### reservations()
``` Python
>>> p.reservations()
{'status': 'success', 'data': [{'id': 1234567, 'receipt': '2001-702-7', 'onDate': '2018-09-16', 'seatId': 12345, 'status': 'RESERVE', 'location': '西校区2层213室区第一阅览室，座位号001', 'begin': '12:00', 'end': '16:00', 'actualBegin': None, 'awayBegin': None, 'awayEnd': None, 'userEnded': False, 'message': '请在 09月16日11点15分 至 12点15分 之间前往场馆签到'}], 'message': '', 'code': '0'}

也可以调用 print
>>> print(p.reservations())
{
  "status": "success",
  "data": [
    {
      "id": 1234567,
      "receipt": "2001-111-1",
      "onDate": "2018-08-08",
      "seatId": 12345,
      "status": "RESERVE",
      "location": "西校区2层213室区第一阅览室，座位号001",
      "begin": "12:00",
      "end": "16:00",
      "actualBegin": null,
      "awayBegin": null,
      "awayEnd": null,
      "userEnded": false,
      "message": "请在 08月08日11点15分 至 12点15分 之间前往场馆签到"
    }
  ],
  "message": "",
  "code": "0"
}

想获得某个数据，比如 location
>>> p.reservations().data[0].location
'西校区2层213室区第一阅览室，座位号001'
```

### user()
``` Python
>>> p.user()
{'status': 'success', 'data': {'id': 1234, 'enabled': True, 'name': '某人', 'username': '220141222999', 'username2': None, 'status': 'NORMAL', 'lastLogin': '2018-08-08T16:35:15.000', 'checkedIn': False, 'lastIn': None, 'lastOut': None, 'lastInBuildingId': None, 'lastInBuildingName': None, 'violationCount': 0}, 'message': '', 'code': '0'}
```

### filters()
``` Python
>>> p.filters()
{'status': 'success', 'data': {'buildings': [[1, '东校区', 5], [2, '西校区', 8]], 'rooms': [[8, '第五阅览室北区', 2, 6], [9, '第八阅览室北区', 2, 6], [11, '第二阅览室北区', 2, 3], [12, '第二阅览室中区', 2, 3], [13, '第二阅览室南区', 2, 3], [14, '第十一阅览室北区', 2, 3], [15, '第十一阅览室中区', 2, 3], [16, '第十一阅览室南区', 2, 3], [17, '第三阅览室北区', 2, 4], [18, '第三阅览室中区', 2, 4], [19, '第三阅览室南区', 2, 4], [21, '第十阅览室中区', 2, 4], [22, '第十阅览室南区', 2, 4], [23, '第六阅览室北区', 2, 7], [24, '第六阅览室中区', 2, 7], [25, '第六阅览室南区', 2, 7], [27, '第七阅览室中区', 2, 7], [28, '第七阅览室南区', 2, 7], [31, '第四阅览室北区', 2, 5], [32, '第四阅览室中区', 2, 5], [33, '第四阅览室南区', 2, 5], [34, '第九阅览室北区', 2, 5], [35, '第九阅览室中区', 2, 5], [36, '第九阅览室南区', 2, 5], [37, '第五阅览室南区', 2, 6], [38, '第五阅览室中区', 2, 6], [40, '第八阅览室南区', 2, 6], [41, '第一阅览室', 2, 2], [46, '第七阅览室北区', 2, 7], [47, '第八阅览室中区', 2, 6], [49, '商科特色阅览室（诺奖图书 五楼南）', 1, 5], [51, '第一期刊阅览室（现刊 四楼北）', 1, 4], [52, '商科专业书库（二楼南）', 1, 2], [53, '外文、工具书库（二楼北）', 1, 2], [54, '二楼大厅', 1, 2], [55, '人文书库（三楼南）', 1, 3], [56, '综合书库（三楼北）', 1, 3], [57, '第二期刊阅览室（过刊 四楼南）', 1, 4], [58, '第三期刊阅览室（赠刊 五楼北）', 1, 5], [59, '五楼走廊', 1, 5], [60, '信息共享空间（一楼南）', 1, 1], [62, '文化展厅（一楼北）', 1, 1]], 'hours': 15, 'dates': ['2018-09-16', '2018-09-17']}, 'message': '', 'code': '0'}
```

### roomStats(building_id)
参数为 filters() 中的图书馆 id
``` Python
>>> p.roomStats(2)  # p.roomstats(p.filters().data.buildings.[1][0])
{'status': 'success', 'data': [{'roomId': 41, 'room': '第一阅览室', 'floor': 2, 'maxHour': 4, 'reserved': 0, 'inUse': 107, 'away': 0, 'totalSeats': 136, 'free': 28},...省略...,{'roomId': 25, 'room': '第六阅览室南区', 'floor': 7, 'maxHour': 15, 'reserved': 0, 'inUse': 97, 'away': 0, 'totalSeats': 108, 'free': 9}], 'message': '', 'code': '0'}
```

### seatStartTime(seat_id, date)
``` Python
>>> p.seatStartTime(1234, "2018-08-08")
{'status': 'success', 'data': {'startTimes': [{'id': '1140', 'value': '19:00'}, {'id': '1200', 'value': '20:00'}, {'id': '1260', 'value': '21:00'}]}, 'message': '', 'code': '0'}
```
详细解释一下，Seat id 为每个座位对应的 ID 编号，如果你不知道座位 ID 为多少，可以通过 getSeatIDbyNum 来获取。Room id 则为filters().data.rooms[n][0] ，你也可以通过 getRoomIDbyName 来获取Room ID。另外参数 date 以 filters() 方法返回的 dates 数据为准。

### freeBook(start_time, end_time, seat_id, date)
start_time, end_time 为开始结束时间，可以是整数、小数（7点就填7），也可以是 seatStartTime 返回的 data.startTimes[n].id，但预约总时常不能超过 roomStats 中返回的 maxHour 。返回结果自行分析。你也可以使用 book 方法来进行预约

``` Python
>>> p.freeBook(7, 20, 1234, "2018-08-08")
{'status': 'fail', 'data': None, 'message': '已有1个有效预约，请在使用结束后再次进行选择', 'code': '1'}
```

### checkIn()
签到应提前45分钟内签到

### cancelRes(res_id)
参数在可以在 history() 或者 reservations() 中查看
``` Python
>>> p.cancelRes(1234567)
{'status': 'success', 'data': None, 'message': '', 'code': '0'}
```

### dates()
``` Python
>>> p.dates()
['2018-08-08', '2018-08-09']
```

### rooms()
``` Python
>>> p.rooms()
{'buildings': [{'buildingID': 1, 'buildingName': '东校区'}, {'buildingID': 2, 'buildingName': '西校区'}], 'rooms': [{'buildingID': 2, 'roomName': '第五阅览室北区', 'roomID': 8, 'floor': 6}, ...省略..., {'buildingID': 1, 'roomName': '文化展厅（一楼北）', 'roomID': 62, 'floor': 1}]}
```

### getSeatIDbyNum(room_id, seat_num)
``` Python
>>> p.getSeatIDbyNum(19, 299)
9419
```

### getRoomIDbyName(room_name)
``` Python
>>> p.getRoomIDbyName('第一阅览室')
41
```

### getRoomNamebyID(room_id)
``` Python
>>> p.getRoomNamebyID("41")
'第一阅览室'
```

### seatInfo(room_id, seat_num)
``` Python
>>> print(p.seatInfo(19, 299))
{
  "roomName": "第三阅览室南区",
  "roomID": 19,
  "seatNum": 299,
  "seatID": 9419,
  "times": [
    {
      "date": "2018-08-08",
      "startTimes": [
        {
          "id": "780",
          "value": "13:00"
        },
        {
            ...
        }
        {
          "id": "1260",
          "value": "21:00"
        }
      ]
    },
    {
      "date": "2018-08-09",
      "startTimes": [
        {
          "id": "420",
          "value": "07:00"
        },
        {
          ...
        },
        {
          "id": "1260",
          "value": "21:00"
        }
      ]
    }
  ]
}
```

### book(start_time, end_time, room_id, seat_num, date)
``` Python
>>> p.book(19, 20, 19, 299, '2018-08-08')
{'status': 'success', 'data': {'id': 1234567, 'receipt': '2222-222-2', 'onDate': '2018 年 08 月 08 日', 'begin': '19 : 00', 'end': '20 : 00', 'location': '西校区4层407室区第三阅览室南区，座位号299', 'checkedIn': False, 'checkInMsg': '当前没有可用预约'}, 'message': '', 'code': '0'}
```
