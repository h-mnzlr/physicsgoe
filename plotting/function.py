"""Provides plotting capability for functions."""

import matplotlib.pyplot as plt
from numpy import linspace
from .distribution import no_errorbars


def plot_function(f, x_range, plot=plt, color="blue", label=None):
    values = linspace(x_range[0], x_range[1])
    no_errorbars(values, f(values), plt, color=color, label=label)
