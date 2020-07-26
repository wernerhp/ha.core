"""Constants for the Calendar component."""
DOMAIN = "calendar"

VIEW_MODE_MONTH = "month"
VIEW_MODE_WEEK = "week"
VIEW_MODE_DAY = "day"
VIEW_MODE_SCHEDULE = "schedule"
VIEW_MODES = [
    VIEW_MODE_MONTH,
    VIEW_MODE_WEEK,
    VIEW_MODE_DAY,
    VIEW_MODE_SCHEDULE,
]

DEFAULT_CALENDAR_VIEW = "schedule"
DEFAULT_NAME = "Calendar"

ATTR_CURRENT = "current"
ATTR_EVENT = "event"
ATTR_EVENT_TITLE = "title"
ATTR_EVENT_DESCRIPTION = "description"
ATTR_EVENT_LOCATION = "location"
ATTR_EVENT_STATUS = "status"
ATTR_EVENT_VISIBILITY = "visibility"
ATTR_NAME = "name"
ATTR_UPCOMING = "upcoming"

STATE_BUSY = "busy"
STATE_FREE = "free"
