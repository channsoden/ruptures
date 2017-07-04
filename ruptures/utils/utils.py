"""Miscellaneous functions for ruptures."""

from itertools import tee

from random import choice
import numpy as np


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def draw_bkps(n_samples, n_bkps, min_size=None):
    """Return a set of random breakpoint indexes."""
    bkps = [n_samples]
    if min_size is None:
        min_size = n_samples // 20  # maximum 20 breakpoints allowed
    ind = np.arange(n_samples)
    mask = np.ones(n_samples, dtype=bool)
    mask[:min_size] = False
    mask[-min_size:] = False
    for _ in range(n_bkps):
        bkp = choice(ind[mask])
        mask[bkp - min_size:bkp + min_size] = False
        bkps.append(bkp)
    return sorted(bkps)


def unzip(seq):
    """Reverse zip"""
    return zip(*seq)


def admissible_filter(start, end, jump, min_size):
    """A filter to know if an index can be considered as a change point."""
    def filtre(ind):
        """Return True if index is admissible."""
        return all((ind - start > min_size, end - ind > min_size, ind % jump == 0))
    return filtre
