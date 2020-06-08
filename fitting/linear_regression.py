"""Module that implements linear regressions with scipy.odr."""

# import numpy as np
from scipy.odr import ODR, RealData, Model


def linear_model(params, x):
    """A linear Function used as a model blueprint."""
    return params[0]*x+params[1]


def linear_regression(data, err):
    """Calculate a linear regression using scipy.odr and return fit output."""
    print('Fitting with')
    print(data)
    beta0 = get_start_values(data)
    model = Model(linear_model)
    rdata = RealData(data[:, 0], data[:, 1], sx=err[0])  # TODO: check different errors
    fit = ODR(rdata, model, beta0=beta0)
    output = fit.run()
    print(output.beta)
    return output


def get_start_values(data):
    """Return the start values for fitting."""
    return (1, 0)
