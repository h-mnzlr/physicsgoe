"""Module that implements linear regressions with scipy.odr."""

# import numpy as np
from scipy.odr import ODR, RealData, Model


def linear_model(params, x):
    """A linear Function used as a model blueprint."""
    return params[0]*x+params[1]


def lineal_model_origin(params, x):
    """A linear Function without y-displacement."""
    return params[0] * x


def linear_regression(data, err):
    """Calculate a linear regression using scipy.odr and return fit output."""
    print('Fitting with')
    print(data[:, 0], data[:, 1])
    print('and Error')
    print(err[:, 0], err[:, 1])
    beta0 = get_start_values(data)
    model = Model(linear_model)
    rdata = RealData(data[:, 0], data[:, 1], sx=err[:, 0], sy=err[:, 1])
    # TODO: check different errors
    fit = ODR(rdata, model, beta0=beta0)
    output = fit.run()
    print(output.beta)
    return output


def simple_regression(data):
    """Calculate linear regression for errorless data."""
    n = len(data)
    x_sum = sum(data[:, 0])
    y_sum = sum(data[:, 1])
    xy_sum = sum(data[:, 0] * data[:, 1])
    x_sq_sum = sum(data[:, 0] * data[:, 0])
    denom = n * x_sq_sum - x_sum * x_sum
    m = (n * xy_sum - x_sum * y_sum) / denom
    b = (x_sq_sum * y_sum - x_sum * xy_sum) / denom
    dev_sum = sum((data[:, 1] - b - m * data[:, 0]) ** 2)
    sig_m = (n * dev_sum) / (n-2) / denom
    sig_b = (x_sq_sum * dev_sum) / (n-2) / denom
    return m, b, sig_m, sig_b


def get_start_values(data):
    """Return the start values for fitting."""
    return (.01, 0)
