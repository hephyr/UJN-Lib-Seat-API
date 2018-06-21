package LeosysLibSystemAPI

const BASE_URL = "http://seat.ujn.edu.cn"

const (
	GET_TOKEN_URL       = BASE_URL + "/rest/auth?username=%s&password=%s"
	CHECK_TOKEN_URL     = BASE_URL + "/rest/v2/user/reservations"
	USER_URL            = BASE_URL + "/rest/v2/user"
	FILTERS_URL         = BASE_URL + "/rest/v2/free/filters"
	CHECKIN_URL         = BASE_URL + "/rest/v2/checkIn"
	ROOM_STATS_URL      = BASE_URL + "/rest/v2/room/stats2/%d"
	LAYOUTBYDATE_URL    = BASE_URL + "/rest/v2/room/layoutByDate/%d/%s/"
	SEAT_START_TIME_URL = BASE_URL + "/rest/v2/startTimesForSeat/%d/%s"
	SEAT_END_TIME_URL   = BASE_URL + "/rest/v2/endTimesForSeat/%d/%s/%s"
	HISTORY_URL         = BASE_URL + "/rest/v2/history/%s/%s"
	CANCEL_URL          = BASE_URL + "/rest/v2/cancel/%d"
	FREEBOOK_URL        = BASE_URL + "/rest/v2/freeBook"
	// 可能被废弃的 API
	STOP_URL            = BASE_URL + "/rest/v2/stop"
	ALLOWED_HOURS_URL   = BASE_URL + "/rest/v2/allowedHours"
	QUICKBOOK_URL       = BASE_URL + "/rest/v2/quickBook"
)
