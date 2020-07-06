"""Module that provides simple funcitons for the calculation of averages."""

import numpy as np


def weighted_average(data, err):
    """Calculates the weightes average of a numpy array with it's errors."""
    inv_error_sq_sum = sum(1 / err / err)
    x_corrected_sum = sum(data / err / err)
    return x_corrected_sum / inv_error_sq_sum, np.sqrt(1 / inv_error_sq_sum)
