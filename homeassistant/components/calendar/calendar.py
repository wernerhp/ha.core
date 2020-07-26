"""Calendar entity with support for events."""
import calendar
import logging

from abc import ABC
from aiohttp import web
from datetime import timedelta
from typing import List

from homeassistant.components import http
from homeassistant.const import HTTP_BAD_REQUEST
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.util import dt

from .const import (
    ATTR_CURRENT,
    ATTR_UPCOMING,
    STATE_BUSY,
    STATE_FREE,
    VIEW_MODE_MONTH,
    VIEW_MODE_WEEK,
    VIEW_MODE_DAY,
    VIEW_MODE_SCHEDULE,
    VIEW_MODES,
)

_LOGGER = logging.getLogger(__name__)


class CalendarEvent(ABC):
    """Calendar Event object"""

    id = None
    title = None
    description = None
    location = None
    start = None
    end = None
    status = None
    organizer = None
    creator = None
    created = None
    updated = None
    ical_uid = None
    url = None


class CalendarEntity(Entity):
    """An entity representing a calendar."""

    def __init__(self, data):
        """Initialize Calendar Entity"""
        self._data = data
        self._state = None
        self._events = []

    @property
    def state(self):
        """Return the state of the calendar."""
        return self._state

    @property
    def state_attributes(self):
        """Return the state attributes."""
        data = {
            ATTR_CURRENT: self.current_events(),
            ATTR_UPCOMING: self.upcoming_events(),
        }

        return {key: val for key, val in data.items() if val is not None}

    def current_events(self) -> List:
        """Return a list of events that are currently happening."""
        events = []
        for event in self._events:
            event_start = dt.as_utc(event.start.replace(year=dt.now().year))
            event_end = dt.as_utc(event.start.replace(year=dt.now().year))

            if event_start <= dt.now() < event_end:
                events.append(vars(event))

        return events

    def upcoming_events(self, count=10) -> List:
        """Return a list of the next x upcoming events."""
        events = []
        for i, event in enumerate(self._events, start=1):
            events.append(vars(event))
            if i == count:
                break

        return events

    def view_events(self, mode=None, **kwargs) -> List:
        """Return a list of events for a view."""

        if mode == VIEW_MODE_SCHEDULE:
            count = kwargs.get("count")
            return self.upcoming_events(count=count)

        now = dt.now()

        # VIEW_MODE_DAY
        view_start = dt.as_utc(now.replace(hour=0, minute=0, second=0))
        view_end = view_start + timedelta(days=1)

        if mode == VIEW_MODE_WEEK:
            view_start = now - timedelta(days=now.weekday())
            view_end = view_start + timedelta(days=6)

        if mode == VIEW_MODE_MONTH:
            view_start = view_start.replace(day=1)
            view_end = view_end.replace(
                day=calendar.monthrange(year=now.year, month=now.month)[1]
            )

        events = []
        for event in self._events:
            event_start = dt.as_utc(event.start.replace(year=dt.now().year))
            event_end = dt.as_utc(event.end.replace(year=dt.now().year))

            if (
                view_start <= event_start < view_end
                or view_start <= event_end < view_end
            ):
                events.append(vars(event))

        return events

    def update(self):
        """Update Calendar Entity"""
        self._state = STATE_FREE

        if self._events is None:
            return True

        if self.current_events():
            self._state = STATE_BUSY

        return True


class CalendarEventView(http.HomeAssistantView):
    """Returns a list of events for a given calendar and view mode."""

    url = "/api/v2/calendars/{entity_id}"
    name = "api:calendars:calendar"

    def __init__(self, component: EntityComponent) -> None:
        """Initialize calendar view."""
        self.component = component

    async def get(self, request, entity_id):
        """Return calendar events."""
        try:
            entity = self.component.get_entity(entity_id)
            mode = request.query.get("mode")
            count = int(request.query.get("count", 10))
        except (ValueError, TypeError):
            return web.Response(status=HTTP_BAD_REQUEST)

        if None in (entity, mode) or mode not in VIEW_MODES:
            return web.Response(status=HTTP_BAD_REQUEST)

        events = entity.view_events(mode=mode, count=count)
        return self.json(events)


class CalendarListView(http.HomeAssistantView):
    """Returns a list of calendars."""

    url = "/api/v2/calendars"
    name = "api:calendars"

    def __init__(self, component: EntityComponent) -> None:
        """Initialize calendar view."""
        self.component = component

    async def get(self, request: web.Request) -> web.Response:
        """Retrieve calendar list."""
        hass = request.app.get("hass")
        calendars = []

        for entity in self.component.entities:
            state = hass.states.get(entity.entity_id)
            calendars.append({"name": state.name, "entity_id": entity.entity_id})

        return self.json(sorted(calendars, key=lambda x: x["name"]))
