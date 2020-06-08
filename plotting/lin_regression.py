"""Plot the typical data for a linear regression in a pleasing manner."""


import matplotlib.pyplot as plt
from .function import plot_function
from .distribution import errorbar


def plot_lin_regr(data, err,  fit_out, plot=plt, color='blue',
                  x_range=None, label="Lineare Regression"):
    """Plot the data of a typical Linear Regression to a preexisting Plot."""
    if not x_range:
        x_range = _x_range(data[:, 0])

    set_x_range(x_range, plot=plt)

    def lin_func(x):
        return fit_out.beta[0] * x + fit_out.beta[1]
    plot_function(lin_func, x_range, plot=plt, color=color, label=None)
    errorbar(data[:, 0], data[:, 1], err[:, 0], err[:, 1],
             color=color, label=label)


def set_x_range(x_range, plot=plt):
    """Sets given x range to a given plot object."""
    plt.xlim(x_range[0], x_range[1])


def _x_range(x_data, margin=.1):
    """Return the range of the iterator and return it plus a percent margin."""
    x_max, x_min = max(x_data), min(x_data)
    x_margin = (x_max - x_min) * margin
    return (x_min - x_margin, x_max + x_margin)
