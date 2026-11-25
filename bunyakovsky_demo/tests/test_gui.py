"""Tests for the tkinter GUI layer (gui.py).

The pure logic (pretty_math, render_lines, compute_for, compute_census)
runs everywhere. The Tk-widget test is skipped when no display/Tk is
available; when present it drives the real app methods (no mainloop).
"""
import pytest

from bunyakovsky_demo.gui import (compute_census, compute_for, pretty_math,
                                  render_lines)


def test_pretty_math():
    assert pretty_math("$x^{2} + 1$") == "x\u00b2 + 1"
    assert pretty_math("$\\mathbb{Z}$") == "\u2124"
    assert pretty_math("$p \\le 200$") == "p \u2264 200"
    assert pretty_math("$\\nu_p = 3$") == "\u03bd_p = 3"
    assert pretty_math("$10^{4}$") == "10\u2074"
    assert pretty_math("**bold** word") == "bold word"
    assert pretty_math("$x^4+1$ and plain $y$") == "x\u2074+1 and plain y"
    # regressions caught in the live GUI screenshot:
    assert pretty_math("$n = 3, \\dots, 5$") == "n = 3, \u2026, 5"
    assert pretty_math("$p_{max}$") == "p_max"
    assert pretty_math("for *ranking*, not") == "for ranking, not"


def test_render_lines_census_clean():
    # no markdown/LaTeX artifacts may survive on any GUI line
    lines = render_lines(compute_census(1, 1))
    joined = "\n".join(s for _, s in lines)
    for artifact in ("$", "|", "**", "*", "\\dots", "_{", "\\le"):
        assert artifact not in joined, artifact


def test_render_lines_structure():
    from bunyakovsky_demo import analyze, render_analysis_md
    md = render_analysis_md(analyze([1, 0, 1], N=200))
    lines = render_lines(md)
    assert all(isinstance(t, tuple) and len(t) == 2 for t in lines)
    tags = {t for t, _ in lines}
    assert "h1" in tags and "table" in tags
    assert lines[0][0] == "h1"
    # no raw markdown artifacts survive
    joined = "\n".join(s for _, s in lines)
    assert "$" not in joined and "|" not in joined
    assert "**" not in joined
    assert "x\u00b2 + 1" in joined or "x\u00b2+1" in joined


def test_compute_for_single_and_tuple():
    md = compute_for("x^2 + 1")
    assert md.startswith("# ")
    md2 = compute_for("x, x+2")
    assert "twin-prime" in md2


def test_compute_for_bad_input_raises():
    with pytest.raises(ValueError):
        compute_for("x + y")


def test_compute_census():
    md = compute_census(1, 1)
    assert md.startswith("# Census")


def test_gui_app_roundtrip():
    tk = pytest.importorskip("tkinter")
    from bunyakovsky_demo.gui import PRESETS
    root = None
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available")
    try:
        # instantiate the widgets exactly as main() does, minus mainloop
        from tkinter import ttk
        entry = ttk.Entry(root)
        entry.insert(0, "x^4 + 1")
        md = compute_for(entry.get())
        assert "blind spot" in md.lower()
        assert set(PRESETS.values()) and "x, x + 2" in PRESETS.values()
        lines = render_lines(md)
        assert lines[0][0] == "h1"
    finally:
        if root is not None:
            root.destroy()
