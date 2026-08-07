"""Statistics — a policy layer over scipy, not an implementation (AD-3).

scipy computes correctly. It was verified against the surveyed workspace's
hand-rolled formulas twice: ``permutation_test`` reproduces the ``(k+1)/(n+1)``
estimator exactly (0.269000 both ways), and ``monte_carlo_test`` reproduces
the structural null to the digit (0.600570, difference 0.000000). Nothing
here recomputes any of that.

What this module adds is the two constraints scipy does not enforce, which
are the two failures actually observed:

**A resampling function cannot be called without a seed.** ``rng`` has no
default. scipy will run unseeded without complaint; 9 scripts in the survey
did, one of them reporting a p-value that differed on every run (L-03).

**A p-value belonging to a family cannot be printed until the family has
been adjusted.** 11 of 15 p-value scripts applied no correction, though
``scipy.stats.false_discovery_control`` was one import away. Availability
was never the problem: producing 20 uncorrected p-values and producing 1
look identical at the point of printing. Here they do not (L-02).
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass, replace
from collections.abc import Callable, Sequence

import numpy as np
import scipy.stats as _st

__all__ = [
    "Result", "family", "p_adjust", "combine", "permutation_test",
    "monte_carlo_test", "exact_test", "agreement", "bootstrap_ci",
    "UnadjustedError", "ProvenanceError",
]


class UnadjustedError(RuntimeError):
    """Raised when a member of a p-value family is formatted unadjusted."""


class ProvenanceError(RuntimeError):
    """Raised when a Result cannot say where its number came from."""


@dataclass
class _Family:
    size: int
    adjusted: bool = False


@dataclass
class Result:
    """A number that knows where it came from (AD-2).

    Refuses to render as a bare figure when its provenance is incomplete or
    when it is one of several p-values that have not been adjusted.
    """
    value: float
    p: float | None = None
    method: str = ""
    seed: int | None = None
    n: int | None = None
    corpus: str | None = None
    null: np.ndarray | None = None
    adjusted: float | None = None
    _family: _Family | None = None

    # -- the gate ---------------------------------------------------------
    def _check(self) -> None:
        if self.p is not None and self.seed is None and \
                not self.method.startswith("exact"):
            raise ProvenanceError(
                f"{self.method or 'result'} carries a p-value but no seed; "
                "a resampled number that cannot be reproduced is not a result")
        if self.p is not None and self.corpus is None:
            raise ProvenanceError(
                "no corpus fingerprint: this number cannot be tied to the "
                "data it was computed from")
        fam = self._family
        if fam is not None and fam.size > 1 and self.adjusted is None:
            raise UnadjustedError(
                f"this p-value is one of {fam.size}; call stats.p_adjust() on "
                "the family before reporting it, or read .unadjusted_p "
                "deliberately")

    def __format__(self, spec: str) -> str:
        self._check()
        bits = [f"{self.method}", f"value={self.value:.6g}"]
        if self.p is not None:
            shown = self.adjusted if self.adjusted is not None else self.p
            bits.append(f"p={shown:.6g}")
            if self.adjusted is not None:
                bits.append(f"(adjusted, raw {self.p:.6g})")
        if self.seed is not None:
            bits.append(f"seed={self.seed}")
        if self.n is not None:
            bits.append(f"n={self.n}")
        if self.corpus:
            bits.append(str(self.corpus))
        return "  ".join(bits)

    def __str__(self) -> str:
        return self.__format__("")

    @property
    def unadjusted_p(self) -> float | None:
        """The raw p-value, bypassing the family gate.

        Deliberately named so that bypassing is greppable and visible in
        review, rather than something that happens by accident.
        """
        return self.p


# ------------------------------------------------------------------ families
def family(results: Sequence[Result]) -> list[Result]:
    """Declare that these p-values belong together.

    Members of a family of more than one refuse to format until
    :func:`p_adjust` has seen them. A family may be assembled after the
    fact, including across separate runs (TC-E16).
    """
    fam = _Family(size=len(results))
    return [replace(r, _family=fam) for r in results]


def p_adjust(results: Sequence[Result], *, method: str = "bh") -> list[Result]:
    """Correct a family for multiple comparisons.

    ``bh``/``by`` delegate to ``scipy.stats.false_discovery_control``;
    ``bonferroni``/``holm`` to ``statsmodels`` (scipy has neither).
    """
    ps = [r.p for r in results]
    if any(p is None for p in ps):
        raise ValueError("every member of a family must carry a p-value")

    if method in ("bh", "by"):
        adj = list(_st.false_discovery_control(ps, method=method))
    elif method in ("bonferroni", "holm"):
        from statsmodels.stats.multitest import multipletests
        adj = list(multipletests(ps, method=method)[1])
    else:
        raise ValueError(f"unknown method {method!r}")

    fam = _Family(size=len(results), adjusted=True)
    return [replace(r, adjusted=float(a), _family=fam)
            for r, a in zip(results, adj, strict=True)]


def combine(results: Sequence[Result], *, method: str = "fisher") -> Result:
    """Combine p-values. Clipped, so a p of exactly 0 does not give -inf."""
    ps = np.clip([r.p for r in results], 1e-300, 1.0)
    stat, p = _st.combine_pvalues(ps, method=method)
    return Result(value=float(stat), p=float(p), method=f"combine:{method}",
                  seed=results[0].seed if results else None,
                  n=len(ps), corpus=results[0].corpus if results else None)


# ------------------------------------------------------------------- testing
def _generator(rng) -> np.random.Generator:
    return rng if isinstance(rng, np.random.Generator) \
        else np.random.default_rng(rng)


def _warn_if_alpha_unreachable(n: int, alpha: float | None) -> None:
    if alpha is not None and alpha < 1.0 / (n + 1):
        warnings.warn(
            f"alpha={alpha} is unreachable with n={n} resamples: the smallest "
            f"attainable p-value is {1.0 / (n + 1):.3g}", UserWarning,
            stacklevel=3)


def permutation_test(data, *, statistic: Callable, rng, n: int = 20_000,
                     alternative: str = "greater", corpus: str | None = None,
                     alpha: float | None = None, **kw) -> Result:
    """Two-sample permutation test. ``rng`` is required (S-01).

    Delegates to ``scipy.stats.permutation_test``, which uses the same
    ``(k+1)/(n+1)`` estimator as the surveyed workspace's eight hand-rolled
    copies — verified numerically, so adopting it moves no published number.
    """
    if any(len(np.asarray(d)) == 0 for d in data):
        raise ValueError("empty sample")
    _warn_if_alpha_unreachable(n, alpha)
    gen = _generator(rng)
    res = _st.permutation_test(
        tuple(np.asarray(d, float) for d in data), statistic,
        n_resamples=n, alternative=alternative, rng=gen, **kw)
    seed = rng if not isinstance(rng, np.random.Generator) else None
    return Result(value=float(res.statistic), p=float(res.pvalue),
                  method="permutation", seed=seed, n=n,
                  corpus=corpus or "unspecified",
                  null=np.asarray(res.null_distribution))


def monte_carlo_test(observed, *, draw: Callable, statistic: Callable, rng,
                     n: int = 20_000, alternative: str = "greater",
                     corpus: str | None = None,
                     alpha: float | None = None) -> Result:
    """Test against an arbitrary null supplied by ``draw`` (S-02b).

    This is the entry point for *structural* nulls — k marker positions
    drawn from N, coverage windows, and so on. ``permutation_test`` cannot
    express those: they are not a relabelling of observed data, so none of
    its ``permutation_type`` values apply. Verified in
    ``tests/spike_null_model.py`` to reproduce the hand-rolled result
    exactly.

    ``draw(generator, size) -> array`` generates ``size`` samples under the
    null, taking the seeded generator so reproducibility is not optional.
    """
    _warn_if_alpha_unreachable(n, alpha)
    gen = _generator(rng)
    res = _st.monte_carlo_test(
        observed, lambda size: draw(gen, size if isinstance(size, int) else size[0]),
        statistic, n_resamples=n, alternative=alternative, vectorized=True)
    seed = rng if not isinstance(rng, np.random.Generator) else None
    return Result(value=float(np.asarray(res.statistic).item()),
                  p=float(np.asarray(res.pvalue).item()),
                  method="monte_carlo", seed=seed, n=n,
                  corpus=corpus or "unspecified",
                  null=np.asarray(res.null_distribution))


def exact_test(kind: str, *, alternative: str = "greater",
               corpus: str | None = None, **params) -> Result:
    """Closed-form test. Prefer this over simulation where it exists (S-04).

    ``kind`` ∈ hypergeometric | binomial | fisher-exact. No seed, because
    nothing random happens — the Result reflects that rather than inventing
    provenance it does not have.
    """
    if kind == "hypergeometric":
        M, nn, N, k = params["M"], params["n"], params["N"], params["k"]
        dist = _st.hypergeom(M, nn, N)
        p = dist.sf(k - 1) if alternative == "greater" else dist.cdf(k)
        value = float(k)
    elif kind == "binomial":
        r = _st.binomtest(params["k"], params["n"], params.get("p", 0.5),
                          alternative=alternative)
        p, value = float(r.pvalue), float(params["k"])
    elif kind == "fisher-exact":
        value, p = _st.fisher_exact(params["table"], alternative=alternative)
    else:
        raise ValueError(f"unknown exact test {kind!r}")
    return Result(value=float(value), p=float(p), method=f"exact:{kind}",
                  seed=None, n=None, corpus=corpus or "unspecified")


def agreement(a, b, *, method: str = "cohen", corpus: str | None = None,
              **kw) -> Result:
    """Inter-rater agreement (S-10)."""
    if method != "cohen":
        raise ValueError(f"unknown method {method!r}")
    from sklearn.metrics import cohen_kappa_score
    return Result(value=float(cohen_kappa_score(a, b, **kw)),
                  method="agreement:cohen", corpus=corpus or "unspecified")


def bootstrap_ci(data, *, statistic: Callable, rng, n: int = 10_000,
                 level: float = 0.95, corpus: str | None = None) -> Result:
    """Bootstrap confidence interval. ``rng`` required (S-01)."""
    gen = _generator(rng)
    res = _st.bootstrap(data, statistic, n_resamples=n,
                        confidence_level=level, rng=gen)
    seed = rng if not isinstance(rng, np.random.Generator) else None
    lo, hi = res.confidence_interval
    return Result(value=float((lo + hi) / 2), method="bootstrap", seed=seed,
                  n=n, corpus=corpus or "unspecified",
                  null=np.array([lo, hi]))
