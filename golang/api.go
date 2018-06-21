package LeosysLibSystemAPI

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
	"github.com/bitly/go-simplejson"
	"strconv"
)

type User struct {
	account  string
	password string
	token    string
	client   *http.Client
}

func NewLibUser(account string, password string) *User {
	return &User{
		account:  account,
		password: password,
		client: &http.Client{},
	}
}

func request_call(client *http.Client, method string, request_url string, data url.Values, header http.Header) ([]byte, error) {
	req, err := http.NewRequest(method, request_url, strings.NewReader(data.Encode()))
	if err != nil {
		return nil, err
	}
	req.Header = header
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Add("Content-Type", "charset=UTF-8")
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	return body, nil
}

func (u *User) request(method string, request_url string, data url.Values) ([]byte, error) {
	header := http.Header{}
	header.Set("token", u.token)
	return request_call(u.client, method, request_url, data, header)
}

/* Login JSON
{
	"status": "success",
	"data": {
	"token": "CD3ODWMACU06201024"
	},
	"code": "0",
	"message": ""
}*/
func (u *User) Login() ([]byte, error) {
	body, err := u.request("GET", fmt.Sprintf(GET_TOKEN_URL, u.account, u.password), nil)
	if err != nil {
		return nil, err
	}
	resp_json, err:= simplejson.NewJson(body)
	if err != nil {
		return nil, err
	}
	u.token, err = resp_json.Get("data").Get("token").String()
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* CheckToken JSON
{
	"status": "success",
	"data": null,
	"message": "",
	"code": "0"
}*/
func (u *User) CheckToken() ([]byte, error) {
	body, err := u.request("GET", CHECK_TOKEN_URL, nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* User JSON
{
	"status": "success",
	"data": {
		"id": 7074,
		"enabled": true,
		"name": "我的名字",
		"username": "我的学号",
		"username2": null,
		"status": "NORMAL",
		"lastLogin": "2018-06-20T09:22:34.000",
		"checkedIn": false,
		"lastIn": null,
		"lastOut": null,
		"lastInBuildingId": null,
		"lastInBuildingName": null,
		"violationCount": 0
	},
	"message": "",
	"code": "0"
}*/
func (u *User) User() ([]byte, error) {
	body, err := u.request("GET", USER_URL, nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* Filters JSON
{
	"status": "success",
	"data": {
		"buildings": [
			[1, "东校区", 5],
			[2, "主校区", 8]
		],
		"rooms": [
			[8, "第五阅览室北区", 2, 6],
			[9, "第八阅览室北区", 2, 6],
			[11, "第二阅览室北区", 2, 3],
			[12, "第二阅览室中区", 2, 3],
			[13, "第二阅览室南区", 2, 3],
			[14, "第十一阅览室北区", 2, 3],
			[15, "第十一阅览室中区", 2, 3],
			...........................
			[RoomID, "room name", BuildingID, Floor]
			[62, "文化展厅（一楼北）", 1, 1]
		],
		"hours": 15,
		"dates": ["2018-06-21", "2018-06-22"]
	},
	"message": "",
	"code": "0"
}*/
func (u *User) Filters() ([]byte, error) {
	body, err := u.request("GET", FILTERS_URL, nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* RoomStats JSON
{
	"status": "success",
	"data": [{
		"roomId": 41,
		"room": "第一阅览室",
		"floor": 2,
		"maxHour": -1,
		"reserved": 1,
		"inUse": 133,
		"away": 0,
		"totalSeats": 136,
		"free": 2
	}, {
        ................
		................
        ................
	},	{
		"roomId": 25,
		"room": "第六阅览室南区",
		"floor": 7,
		"maxHour": -1,
		"reserved": 2,
		"inUse": 83,
		"away": 0,
		"totalSeats": 108,
		"free": 22
	}],
	"message": "",
	"code": "0"
}*/
func (u *User) RoomStats(buildingID int) ([]byte, error) {
	body, err := u.request("GET", fmt.Sprintf(ROOM_STATS_URL, buildingID), nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* LayoutByDate JSON
{
	"status": "success",
	"data": {
		"id": 54,
		"name": "二楼大厅",
		"cols": 24,
		"rows": 8,
		"layout": {
			"0": {
				"type": "empty"
			},
			.........
			"2002": {
				"id": 41087,
				"name": "001",
				"type": "seat",
				"status": "FREE",
				"window": false,
				"power": false,
				"computer": false,
				"local": false
			},
			.........
			"3005": {
				"id": 4401,
				"name": "235",
				"type": "seat",
				"status": "IN_USE",
				"window": false,
				"power": false,
				"computer": false,
				"local": false
			},
			.........
			"3007": {
				"name": "架",
				"type": "word"
			},
			.........
			"20008": {
				"type": "empty"
			}
		}
	},
	"message": "",
	"code": "0"
}*/
func (u *User) LayoutByDate(roomID int, date string) ([]byte, error) {
	body, err := u.request("GET", fmt.Sprintf(LAYOUTBYDATE_URL, roomID, date), nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* Seat start time JSON
{
	"status": "success",
	"data": {
		"startTimes": [{
			"id": "420",
			"value": "07:00"
		} ,{
			..............
		} ,{
			"id": "1260",
			"value": "21:00"
		}]
	},
	"message": "",
	"code": "0"
}
*/
func (u *User) SeatStartTime(seatID int, date string) ([]byte, error) {
	body, err := u.request("GET", fmt.Sprintf(SEAT_START_TIME_URL, seatID, date), nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* Seat end time JSON
{
	"status": "success",
	"data": {
		"endTimes": [{
			"id": "480",
			"value": "08:00"
		} ,{
			..............
		} ,{
			"id": "1320",
			"value": "22:00"
		}]
	},
	"message": "",
	"code": "0"
}*/
func (u *User) SeatEndTime(seatID int, date, startTime string) ([]byte, error) {
	body, err := u.request("GET", fmt.Sprintf(SEAT_END_TIME_URL, seatID, date, startTime), nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* Free Book JSON
{
	"status": "success",
	"data": {
		"id": 4309649,
		"receipt": "2177-649-4",
		"onDate": "2018 年 06 月 21 日",
		"begin": "20 : 00",
		"end": "22 : 00",
		"location": "东校区2层二楼大厅区二楼大厅，座位号024",
		"checkedIn": false,
		"checkInMsg": "当前没有可用预约"
	},
	"message": "",
	"code": "0"
}
*/
func (u *User) FreeBook(seatID int, startTime, endTime, date string) ([]byte, error) {
	data := url.Values{}
	data.Set("t", "1")
	data.Set("startTime", startTime)
	data.Set("endTime", endTime)
	data.Set("seat", strconv.Itoa(seatID))
	data.Set("t2", "2")
	body, err := u.request("POST", FREEBOOK_URL, data)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* Check in JSON

*/
func (u *User) CheckIn() ([]byte, error) {
	body, err := u.request("GET", CHECKIN_URL, nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* Cancel JSON
{
	"status": "success",
	"data": null,
	"message": "",
	"code": "0"
}
*/
func (u *User) Cancel(reservationID int)  ([]byte, error) {
	body, err := u.request("GET", fmt.Sprintf(CANCEL_URL, reservationID), nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

/* History JSON
{
	"status": "success",
	"data": {
		"reservations": [{
			"id": 4300306,
			"date": "2018-6-21",
			"begin": "07:00",
			"end": "11:00",
			"awayBegin": null,
			"awayEnd": null,
			"loc": "主校区2层213室区第一阅览室018号",
			"stat": "RESERVE"
		}, {
			"id": 4300252,
			"date": "2018-6-21",
			"begin": "07:00",
			"end": "08:00",
			"awayBegin": null,
			"awayEnd": null,
			"loc": "主校区3层303室区第二阅览室北区002号",
			"stat": "CANCEL"
		}]
	},
	"message": "",
	"code": "0"
}
*/
func (u *User) History(page, count string) ([]byte, error) {
	body, err := u.request("GET", fmt.Sprintf(HISTORY_URL, page, count), nil)
	if err != nil {
		return nil, err
	}
	return body, nil
}

