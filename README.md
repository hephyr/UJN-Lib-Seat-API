# 济南大学图书馆座位预约系统API
_UJN Library Seat API for Python_
### 说明
#### 基本
- api.py 为图书馆座位预约系统的API(非全部), 通过iOS客户端下抓包获得.
- ujnlib.py 基于API添加的一些功能
#### 服务端(可选)
- can_use.txt 用于预约的账号(未提供)
- seat.json 用于绑定座位
- reserve_seat.py 进行座位预约
- using.json 预约的座位信息
- flask_server.py 用于返回json数据以提供签到功能
- ci.html 签到网页, 获取flask_server提供的json数据, 用jQuery jsonp请求签到API