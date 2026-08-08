"""Can scipy express the workspace's null model, or must stats keep real code?

The null in question (reconstructed generically, no research content):
  N ordered positions. A marker occupies k of them. Each occurrence covers
  a window of +/-W. Statistic = how many of a fixed set of target points
  fall inside the covered mask. Null = k positions drawn uniformly without
  replacement.

That is NOT a relabelling of samples, so permutation_test's three
permutation_types cannot express it. The question is whether
monte_carlo_test can, and whether it agrees numerically.
"""
import sys, inspect
import numpy as np, scipy.stats as st
sys.stdout.reconfigure(encoding="utf-8")

N, W, K, B = 404, 2, 18, 20000
TARGETS = np.array([0, 17, 40, 61, 88, 115, 140, 166, 190, 221,
                    247, 268, 291, 310, 333, 350, 371, 388, 399, 402])
rng_seed = 20260807

def cover(occ):
    a = np.zeros(N, bool)
    for o in np.atleast_1d(occ):
        a[max(0, o - W):min(N, o + W + 1)] = True
    return a

def stat_from_points(pts):
    return int(cover(pts)[TARGETS].sum())

observed_points = np.array([3, 20, 44, 90, 118, 143, 168, 193, 224,
                            250, 271, 294, 313, 336, 353, 374, 391, 400])
obs = stat_from_points(observed_points)
print(f"N={N} W={W} k={K} targets={len(TARGETS)} observed statistic={obs}\n")

# --- A. the workspace's hand-rolled version -------------------------------
rng = np.random.default_rng(rng_seed)
null_hand = np.empty(B, int)
for b in range(B):
    null_hand[b] = stat_from_points(rng.choice(N, size=K, replace=False))
p_hand = ((null_hand >= obs).sum() + 1) / (B + 1)

# --- B. permutation_test: can it even be expressed? ------------------------
print("permutation_test permutation_type options:",
      [p for p in inspect.signature(st.permutation_test).parameters])
print("  -> the null here is not a relabelling of observed data;")
print("     there is no second sample and no pairing. Not expressible.\n")

# --- C. monte_carlo_test with a custom rvs --------------------------------
rng2 = np.random.default_rng(rng_seed)
def rvs(size):
    n_res = size[0] if isinstance(size, tuple) else size
    return np.array([rng2.choice(N, size=K, replace=False) for _ in range(n_res)])

def statistic(sample, axis=-1):
    sample = np.asarray(sample)
    if sample.ndim == 1:                      # the observed sample
        return stat_from_points(sample)
    return np.array([stat_from_points(row) for row in sample])

res = st.monte_carlo_test(observed_points, rvs, statistic,
                          n_resamples=B, alternative="greater",
                          vectorized=True)

print(f"A. hand-rolled   p = {p_hand:.6f}   (null mean {null_hand.mean():.3f})")
print(f"C. monte_carlo   p = {res.pvalue:.6f}   (null mean {res.null_distribution.mean():.3f})")
print(f"   statistic agrees: {int(res.statistic) == obs}")
d = abs(p_hand - res.pvalue)
print(f"   |difference| = {d:.6f}  -> {'AGREE' if d < 3e-3 else 'DISAGREE'}")

k = int((res.null_distribution >= res.statistic).sum())
print(f"\n   monte_carlo p vs (k+1)/(n+1): {res.pvalue:.6f} vs {(k+1)/(B+1):.6f}"
      f"  same={abs(res.pvalue-(k+1)/(B+1))<1e-12}")
