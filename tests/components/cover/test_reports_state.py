"""Tests for the cover reports_state capability property."""

from homeassistant.components.cover.const import CoverEntityStateAttribute

from .common import MockCover


def test_reports_state_defaults_false() -> None:
    """A cover that does not opt in must not vouch for motion reporting."""
    cover = MockCover()
    assert cover.reports_state is False
    assert (
        cover.state_attributes[CoverEntityStateAttribute.REPORTS_STATE] is False
    )


def test_reports_state_opt_in_true() -> None:
    """A cover that sets the attr reports the capability as True."""
    cover = MockCover()
    cover._attr_reports_state = True
    assert cover.reports_state is True
    assert (
        cover.state_attributes[CoverEntityStateAttribute.REPORTS_STATE] is True
    )


def test_reports_state_key_always_present() -> None:
    """The capability key is always surfaced so consumers can rely on it."""
    cover = MockCover()
    assert CoverEntityStateAttribute.REPORTS_STATE in cover.state_attributes
