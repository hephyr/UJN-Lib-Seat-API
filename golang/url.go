package LeosysLibSystemAPI

const BASE_URL = "http://seat.ujn.edu.cn"

const (
	GET_TOKEN_URL       = BASE_URL + "/rest/auth?username=%v&password=%v"
	USER_URL            = BASE_URL + "/rest/v2/user"
	FILTERS_URL         = BASE_URL + "/rest/v2/free/filters"
	RESERVATIONS_URL    = BASE_URL + "/rest/v2/user/reservations"
	CHECKIN_URL         = BASE_URL + "/rest/v2/checkIn"
	ROOM_STATS_URL      = BASE_URL + "/rest/v2/room/stats2/%v"
	LAYOUTBYDATE_URL    = BASE_URL + "/rest/v2/room/layoutByDate/%v/%v/"
	SEAT_START_TIME_URL = BASE_URL + "/rest/v2/startTimesForSeat/%v/%v"
	SEAT_END_TIME_URL   = BASE_URL + "/rest/v2/endTimesForSeat/%v/%v/%v"
	HISTORY_URL         = BASE_URL + "/rest/v2/history/%v/%v"
	CANCEL_URL          = BASE_URL + "/rest/v2/cancel/%v"
	FREEBOOK_URL        = BASE_URL + "/rest/v2/freeBook"
	// 可能被废弃的 API
	STOP_URL          = BASE_URL + "/rest/v2/stop"
	ALLOWED_HOURS_URL = BASE_URL + "/rest/v2/allowedHours"
	QUICKBOOK_URL     = BASE_URL + "/rest/v2/quickBook"
)
