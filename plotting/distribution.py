"""Provides Plotting capabilites for point distributions with errors."""

import matplotlib.pyplot as plt


def errorbar(x_data, y_data, x_err, y_err, plot=plt, color="blue", label=None):
    plt.errorbar(x_data, y_data, yerr=y_err, xerr=x_err, fmt='.', color=color,
                 label=label)


def no_errorbars(x_data, y_data, plot=plt, color="blue", label=None):
    plt.plot(x_data, y_data, color=color, label=label)
