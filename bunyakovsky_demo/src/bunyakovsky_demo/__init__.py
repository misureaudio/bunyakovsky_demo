"""Bunyakovsky conjecture demo.

Public API: evaluate, degree, format_poly, fixed_divisor, primes_upto,
is_prime, roots_mod_p, is_irreducible_mod_p, irreducible_certificate,
check_hypotheses, scan_primes, bunyakovsky_constant, predicted_count.
Teacher mode (analysis.py): parse_poly, irreducible_z, analyze,
render_analysis_md.
"""
from importlib.metadata import PackageNotFoundError, version as _dist_version

try:  # the installed distribution's metadata is authoritative
    __version__ = _dist_version("bunyakovsky-demo")
except PackageNotFoundError:  # source tree without an install
    __version__ = "0.0.0+local"

from .analysis import (analyze, irreducible_z, parse_poly,
                       render_analysis_md)
from .bunyakovsky import (bunyakovsky_constant, check_hypotheses, degree,
                          evaluate, fixed_divisor, format_poly,
                          irreducible_certificate, is_irreducible_mod_p,
                          is_prime, predicted_count, primes_upto, roots_mod_p,
                          scan_primes)
from .census import render_census_md, run_census
from .tuples import (admissible, analyze_tuple, hypothesis_h_constant,
                     render_tuple_md)

__all__ = ["__version__", "analyze", "analyze_tuple", "admissible",
           "bunyakovsky_constant",
           "check_hypotheses", "degree", "evaluate", "fixed_divisor",
           "format_poly", "hypothesis_h_constant",
           "irreducible_certificate", "irreducible_z", "is_irreducible_mod_p",
           "is_prime", "parse_poly", "predicted_count", "primes_upto",
           "render_analysis_md", "render_census_md", "render_tuple_md",
           "run_census", "roots_mod_p", "scan_primes"]
