"""Tkinter GUI (v1.6.0): a teacher-facing front end for the whole package.

tkinter is stdlib, so the core stays dependency-free; this module is only
imported when the user asks for the GUI (`bunyakovsky-gui` or
`bunyakovsky-demo --gui`) — never from the package root.

Design notes:
- The Markdown cards are not shown raw: `render_lines` turns them into
  (tag, text) pairs and `pretty_math` substitutes real Unicode
  (x^{2} -> x\u00b2, $\\mathbb{Z}$ -> \u2124, \\le -> \u2264, \\nu -> \u03bd), so the output reads like
  a handout instead of a terminal dump. Raw Markdown stays available via
  Copy / Save .md.
- Scans (analysis, census) run in a worker thread; results re-enter the
  UI through root.after(), Tk is only ever touched from the main thread.
- Input dispatch: an expression containing a comma is a Hypothesis H
  tuple, otherwise a single polynomial. Never eval: parsing goes through
  analysis.parse_poly.
"""
from __future__ import annotations

import re
import threading
import time

__all__ = ["main", "compute_for", "compute_census", "render_lines",
           "pretty_math"]

# --------------------------------------------------------------------------
# Markdown -> pretty Unicode lines (pure logic, testable without a display)
# --------------------------------------------------------------------------

_SUPER = str.maketrans("0123456789", "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079")

_SYMBOLS_RAW = [
    (r"\\mathbb\{Z\}", "\u2124"), (r"\\mathbb\{P\}", "\u2119"),
    (r"\\mathbb\{N\}", "\u2115"), (r"\\mathbb\{Q\}", "\u211a"),
    (r"\\pmod\{([^}]*)\}", r"(mod \1)"), (r"\\le(?![A-Za-z])", "\u2264"),
    (r"\\ge(?![A-Za-z])", "\u2265"), (r"\\ne(?![A-Za-z])", "\u2260"),
    (r"\\nu(?![A-Za-z])", "\u03bd"),
    (r"\\omega(?![A-Za-z])", "\u03c9"), (r"\\equiv(?![A-Za-z])", "\u2261"),
    (r"\\infty(?![A-Za-z])", "\u221e"), (r"\\ldots(?![A-Za-z])", "\u2026"),
    (r"\\dots(?![A-Za-z])", "\u2026"),
    (r"\\cdots(?![A-Za-z])", "\u22ef"), (r"\\cdot(?![A-Za-z])", "\u00b7"),
    (r"\\times(?![A-Za-z])", "\u00d7"), (r"\\int(?![A-Za-z])", "\u222b"),
    (r"\\prod(?![A-Za-z])", "\u220f"), (r"\\sum(?![A-Za-z])", "\u03a3"),
    (r"\\pi(?![A-Za-z])", "\u03c0"), (r"\\in(?![A-Za-z])", "\u2208"),
    (r"\\gcd(?![A-Za-z])", "gcd"), (r"\\ln(?![A-Za-z])", "ln"),
    (r"\\deg(?![A-Za-z])", "deg"),
    (r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2"),
    (r"\\[A-Za-z]+", ""),                      # drop any remaining command
]
_SYMBOLS = [(re.compile(a), b) for a, b in _SYMBOLS_RAW]


def pretty_math(s: str) -> str:
    """Convert $...$ math spans (and \\\\(...\\\\)) to Unicode plain text."""
    def one(m):
        e = m.group(1)
        e = re.sub(r"\^\{(\d+)\}", lambda k: k.group(1).translate(_SUPER), e)
        e = re.sub(r"\^(\d)", lambda k: k.group(1).translate(_SUPER), e)
        e = re.sub(r"_\{(\d+)\}", lambda k: k.group(1), e)
        e = re.sub(r"_\{([^{}]*)\}", r"_\1", e)     # p_{max} -> p_max
        e = re.sub(r"\\,", " ", e)
        for pat, rep in _SYMBOLS:
            e = pat.sub(rep, e)
        return e.replace("\\", "")

    s = re.sub(r"\$([^$]*)\$", one, s)
    s = re.sub(r"\\\(([^)]*)\\\)", one, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)           # strip bold markers
    return re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", s)  # italics


def render_lines(md: str):
    """Markdown -> [(tag, text)] with tags h1, h2, table, bullet, text."""
    out: list[tuple[str, str]] = []
    table: list[list[str]] = []

    def flush():
        if not table:
            return
        ncols = max(len(r) for r in table)
        for r in table:
            r += [""] * (ncols - len(r))
        widths = [max(len(r[i]) for r in table) for i in range(ncols)]
        for idx, r in enumerate(table):
            cells = [c.ljust(widths[i]) if i < ncols - 1 else c
                     for i, c in enumerate(r)]
            out.append(("table", "  ".join(cells).rstrip()))
            if idx == 0:
                out.append(("table", "  ".join(
                    "-" * min(w, 60) for w in widths)))
        table.clear()

    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("|"):
            cells = [pretty_math(c.strip())
                     for c in line.strip().strip("|").split("|")]
            if cells and all(set(c.lower()) <= set(":- ") for c in cells):
                continue                        # alignment row
            table.append(cells)
            continue
        flush()
        if line.startswith("# "):
            out.append(("h1", pretty_math(line[2:])))
        elif line.startswith("## "):
            out.append(("h2", pretty_math(line[3:])))
        elif line.startswith("- "):
            out.append(("bullet", "\u2022 " + pretty_math(line[2:])))
        elif line:
            out.append(("text", pretty_math(line)))
    flush()
    return out


# --------------------------------------------------------------------------
# Computation dispatch (pure, no Tk — so it is testable headless)
# --------------------------------------------------------------------------

def compute_for(expr: str) -> str:
    """Analysis card for one polynomial, or Hypothesis H card for a tuple
    (comma-separated). Raises ValueError on unparsable input."""
    from .analysis import analyze, parse_poly, render_analysis_md
    parts = [p for p in expr.split(",")]
    if len(parts) > 1:
        from .tuples import analyze_tuple, render_tuple_md
        return render_tuple_md(analyze_tuple([parse_poly(p) for p in parts]))
    return render_analysis_md(analyze(parse_poly(expr)))


def compute_census(D: int, B: int) -> str:
    from .census import render_census_md, run_census
    return render_census_md(run_census(D=D, B=B))


PRESETS = {
    "Landau: x^2 + 1": "x^2 + 1",
    "Euler: x^2 + x + 41": "x^2 + x + 41",
    "Mirror: x^2 - x + 41": "x^2 - x + 41",
    "Blind spot: x^4 + 1": "x^4 + 1",
    "FD trap: x^2 + x + 2": "x^2 + x + 2",
    "Reducible: 2x^2 + 3x + 1": "2x^2 + 3x + 1",
    "Twins: x, x + 2": "x, x + 2",
    "Triplet (fails p=3): x, x+2, x+4": "x, x+2, x+4",
}

# --------------------------------------------------------------------------
# The app itself (only touched from the main thread)
# --------------------------------------------------------------------------


def main(initial: str = "") -> None:
    """Open the GUI. `initial` optionally pre-fills the input and runs it
    (used by `bunyakovsky-gui "x, x+2"` style launches and tests)."""
    import tkinter as tk
    from tkinter import filedialog, ttk

    root = tk.Tk()
    root.title("Bunyakovsky's conjecture — lab")
    root.geometry("980x720")

    text = tk.Text(root, wrap="word", state="disabled", padx=12, pady=8)
    scroll = ttk.Scrollbar(root, command=text.yview)
    text.configure(yscrollcommand=scroll.set)

    body_font = ("Segoe UI", 10)
    text.tag_configure("h1", font=("Segoe UI", 15, "bold"),
                       foreground="#0b5394", spacing3=6)
    text.tag_configure("h2", font=("Segoe UI", 12, "bold"),
                       foreground="#20124d", spacing1=8, spacing3=4)
    text.tag_configure("table", font=("Consolas", 9), lmargin1=16,
                       lmargin2=16)
    text.tag_configure("bullet", font=body_font, lmargin1=16, lmargin2=30)
    text.tag_configure("text", font=body_font)
    text.tag_configure("error", font=("Segoe UI", 11, "bold"),
                       foreground="#b91c1c")

    entry = ttk.Entry(root, font=("Consolas", 12))
    status = tk.StringVar(value="ready — try a preset, e.g. Twins: x, x + 2")
    busy = {"on": False}
    last_md = {"raw": ""}

    def show_md(md: str) -> None:
        last_md["raw"] = md
        text.configure(state="normal")
        text.delete("1.0", "end")
        for tag, line in render_lines(md):
            text.insert("end", line + "\n", tag)
        text.configure(state="disabled")
        text.see("1.0")

    def set_status(msg: str, is_err: bool = False) -> None:
        status.set(msg)
        if is_err:
            text.configure(state="normal")
            text.insert("end", "\n" + msg + "\n", "error")
            text.configure(state="disabled")

    def worker(fn, done_msg: str) -> None:
        if busy["on"]:
            return
        busy["on"] = True
        t0 = time.time()
        status.set("computing…")

        def work():
            try:
                md = fn()
                err = None
            except Exception as e:                     # noqa: BLE001
                md, err = "", f"{type(e).__name__}: {e}"
            dt = time.time() - t0
            root.after(0, lambda: finish(md, err, dt))

        def finish(md: str, err: str | None, dt: float) -> None:
            busy["on"] = False
            if err:
                set_status(err, is_err=True)
            else:
                show_md(md)
                status.set(f"{done_msg} in {dt:.1f} s")

        threading.Thread(target=work, daemon=True).start()

    def on_analyze(_event=None) -> None:
        expr = entry.get().strip()
        if not expr:
            set_status("type a polynomial (e.g. x^2 + 1) or a tuple "
                       "(e.g. x, x + 2) first")
            return
        worker(lambda: compute_for(expr),
               "tuple analyzed" if "," in expr else "polynomial analyzed")

    def on_census() -> None:
        worker(lambda: compute_census(degsel.get(), htsel.get()),
               f"census D={degsel.get()} B={htsel.get()}")

    def on_preset(_event=None) -> None:
        entry.delete(0, "end")
        entry.insert(0, PRESETS[preset_var.get()])
        on_analyze()

    def on_copy() -> None:
        root.clipboard_clear()
        root.clipboard_append(last_md["raw"])
        status.set("raw Markdown copied to clipboard")

    def on_save() -> None:
        if not last_md["raw"]:
            set_status("nothing to save yet")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("All files", "*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(last_md["raw"])
            status.set(f"saved {path}")

    # ---- top control bar --------------------------------------------------
    bar = ttk.Frame(root, padding=8)
    ttk.Label(bar, text="f(x)  (comma = Hypothesis H tuple):").pack(
        side="left")
    entry.pack(side="left", fill="x", expand=True, padx=8)
    entry.bind("<Return>", on_analyze)
    ttk.Button(bar, text="Analyze", command=on_analyze).pack(side="left")
    preset_var = tk.StringVar(value=list(PRESETS)[0])
    ttk.OptionMenu(bar, preset_var, *PRESETS.keys(),
                   command=on_preset).pack(side="left", padx=(8, 0))
    bar.pack(fill="x")

    cbar = ttk.Frame(root, padding=(8, 0, 8, 8))
    ttk.Label(cbar, text="CENSUS \u2192", font=("Segoe UI", 10, "bold")
              ).pack(side="left")
    degsel = tk.IntVar(value=3)
    htsel = tk.IntVar(value=2)
    ttk.Label(cbar, text="degree").pack(side="left", padx=(10, 4))
    ttk.Spinbox(cbar, from_=1, to=4, width=3, textvariable=degsel).pack(
        side="left")
    ttk.Label(cbar, text="height").pack(side="left", padx=(10, 4))
    ttk.Spinbox(cbar, from_=1, to=3, width=3, textvariable=htsel).pack(
        side="left")
    ttk.Button(cbar, text="Run census", command=on_census).pack(
        side="left", padx=8)
    ttk.Button(cbar, text="Copy Markdown", command=on_copy).pack(side="left")
    ttk.Button(cbar, text="Save .md", command=on_save).pack(side="left",
                                                            padx=4)
    cbar.pack(fill="x")

    text.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    ttk.Label(root, textvariable=status, padding=(8, 4),
              anchor="w").pack(fill="x", side="bottom")

    if initial:
        entry.delete(0, "end")
        entry.insert(0, initial)
        root.after(200, on_analyze)

    try:
        root.mainloop()
    except tk.TclError:
        pass
    return None


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "")
