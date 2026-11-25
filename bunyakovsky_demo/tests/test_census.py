"""Tests for the landscape census (census.py). Small parameters only."""
from bunyakovsky_demo import render_census_md, run_census
from bunyakovsky_demo.census import enumerate_polys
from bunyakovsky_demo.demo import cli


def test_enumerate_basics():
    polys = list(enumerate_polys(2, 1))
    assert [1, 0, 1] in polys                  # x^2 + 1
    # primitive filter: 2x is excluded (content 2), x is present
    assert [0, 2] not in polys and [0, 1] in polys
    # positive leading coefficient only
    assert all(p[-1] > 0 for p in polys)
    # deterministic order: degree ascending
    assert [len(p) for p in polys] == sorted(len(p) for p in polys)


def test_census_small():
    res = run_census(D=2, B=1, scan_N=40, pmax_C=60, blind_pmax=60)
    s = res["stats"]
    assert s["total"] > 0
    assert s["satisfies"] <= s["total"]
    # x^2+1 must be classified as satisfying
    row = next(r for r in res["rows"] if r["coeffs"] == [1, 0, 1])
    assert row["satisfies"] and row["fixed_divisor"] == 1
    # x^2+x+... with fd>1? x^2+x has content 1 but fd 2 (x(x+1) always even)
    row2 = next(r for r in res["rows"] if r["coeffs"] == [0, 1, 1])
    assert row2["fixed_divisor"] == 2
    # no blind spots at prime degree (theorem; must hold in data)
    assert res["by_degree"][1]["blind"] == 0
    assert res["by_degree"][2]["blind"] == 0


def test_census_finds_blind_spot_degree4():
    # x^4 + 1 is inside the B=1 box: the census must rediscover it
    res = run_census(D=4, B=1, scan_N=40, pmax_C=100, blind_pmax=100)
    assert res["by_degree"][3]["blind"] == 0
    blind_coeffs = [r["coeffs"] for r in res["archetypes"]["blind"]]
    assert [1, 0, 0, 0, 1] in blind_coeffs


def test_census_limit_guard():
    import pytest
    with pytest.raises(ValueError):
        run_census(D=3, B=9, limit=100)


def test_render_census():
    res = run_census(D=1, B=1, scan_N=20, pmax_C=40, blind_pmax=40)
    md = render_census_md(res)
    assert md.startswith("# Census")
    assert "| class | count | share |" in md
    assert "| degree | total | satisfies | blind spots |" in md


def test_cli_census(capsys):
    cli(["--census", "--degree", "1", "--height", "1"])
    out = capsys.readouterr().out
    assert "# Census" in out
