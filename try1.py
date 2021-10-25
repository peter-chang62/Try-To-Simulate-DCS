import numpy as np
import matplotlib.pyplot as plt
import clipboard_and_style_sheet
import scipy.constants as sc

clipboard_and_style_sheet.style_sheet()

start = sc.c / 4.55e-6
end = sc.c / 3.45e-6


def bandwidth(fr, dfr):
    return fr ** 2 / (2 * dfr)


def within(item, target, span):
    return target - span / 2 <= item <= target + span / 2


def floor_and_ceil_div(num, denom):
    n1 = num // denom
    n2 = - (-num // denom)
    return n1, n2


def calc_num_for_mod_cond(num, denom):
    N_smaller, N_bigger = floor_and_ceil_div(num, denom)
    eps_bigger = N_bigger * denom - num
    eps_smaller = N_smaller * denom - num
    return num + eps_bigger, num + eps_smaller


def calc_denom_for_mod_cond(num, denom):
    N_smaller, N_bigger = floor_and_ceil_div(num, denom)
    eps_bigger = (num - N_bigger * denom) / N_bigger
    eps_smaller = (num - N_smaller * denom) / N_smaller
    return denom + eps_bigger, denom + eps_smaller


# if True, then aliasing is True (bad)
# if False, then aliasing is False (good)
def is_aliasing(vi, vf, dnu):
    n1 = vi // dnu
    n2 = - (-vf // dnu)
    # print(n1, n2)
    cond = n2 - n1 > 1
    return cond, n1, n2


# trying to figure out the modulo constraint
fr = 1e9
dfr = 23e3
dfr1, dfr2 = calc_denom_for_mod_cond(fr, dfr)
fr1, fr2 = calc_num_for_mod_cond(fr, dfr)
print(is_aliasing(start, end, bandwidth(fr, dfr1)))

dfr = np.linspace(50, 24e3, 10000)
cond = np.array([is_aliasing(start, end, bandwidth(fr, i))[0] for i in dfr])
ind = (cond == False).nonzero()[0]
x = np.zeros(len(dfr))
plt.plot(dfr, x)
plt.plot(dfr[ind], x[ind], '.')
