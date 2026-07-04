"""Tests for coordinate parsing and catalog resolution."""

import pytest

from starwatch.telescope.coordinates import (
    EquatorialCoord,
    parse_dec,
    parse_ra,
    resolve_target,
)


class TestParseRa:
    def test_float(self):
        assert parse_ra(5.5) == 5.5

    def test_colon_format(self):
        assert parse_ra("5:30:00") == pytest.approx(5.5)

    def test_hms_format(self):
        assert parse_ra("5h30m00s") == pytest.approx(5.5)


class TestParseDec:
    def test_float(self):
        assert parse_dec(-5.5) == -5.5

    def test_colon_format_negative(self):
        assert parse_dec("-5:30:00") == pytest.approx(-5.5)

    def test_colon_format_positive(self):
        assert parse_dec("+41:16:09") == pytest.approx(41.269167, rel=1e-3)


class TestEquatorialCoord:
    def test_valid(self):
        c = EquatorialCoord(ra_hours=12.0, dec_degrees=45.0)
        assert c.ra_hours == 12.0

    def test_invalid_ra(self):
        with pytest.raises(ValueError, match="RA must"):
            EquatorialCoord(ra_hours=25.0, dec_degrees=0.0)

    def test_invalid_dec(self):
        with pytest.raises(ValueError, match="DEC must"):
            EquatorialCoord(ra_hours=12.0, dec_degrees=95.0)


class TestResolveTarget:
    def test_catalog_name(self):
        coord = resolve_target("M31")
        assert coord.ra_hours == pytest.approx(0.712)
        assert coord.dec_degrees == pytest.approx(41.269)

    def test_case_insensitive(self):
        coord = resolve_target("m42")
        assert coord.ra_hours == pytest.approx(5.588)

    def test_explicit_coords(self):
        coord = resolve_target("5.5", "-10.0")
        assert coord.ra_hours == 5.5
        assert coord.dec_degrees == -10.0

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown target"):
            resolve_target("NGC999999")