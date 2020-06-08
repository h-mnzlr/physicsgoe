"""Module that provides functionalities for orth. distance regresseion."""

import numpy as np
from scipy.odr import ODR, RealData, Model


def orthogonal_distance_regression(func, data, err, beta0=None):
    """Fit the function using scipy.odr and return fit output."""
    if not beta0:
        beta0 = _start_values(data)
    model = Model(func)
    rdata = _real_data(data, err)
    fit = ODR(rdata, model, beta0=beta0)
    output = fit.run()
    print(output.beta)
    return output


def _real_data(data, err):
    """Basic function returning odr.RealData object."""
    return RealData(data[:], data[:], sx=err[0], sy=err[1])


def _start_values(data):
    """Return start values for fitting."""
    ls = []
    for datu in data:
        ls.append(1e9)
    return np.array(ls)
