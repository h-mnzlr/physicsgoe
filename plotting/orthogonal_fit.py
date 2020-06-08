"""Provides common plotting capabilities for fitted function."""

import matplotlib.pyplot as plt


def plot_fit(data, err, fit_out, plot=plt, color='blue', x_range=None,
            label="Fit")
    if not x_range = _x_range(data[:,0])
