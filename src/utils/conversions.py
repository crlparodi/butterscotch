# -*- coding: utf-8 -*-

def convert_human(_value):
    if _value != "--":
        value = eval(_value)
    else:
        return f"{_value} "

    if 1e03 <= value < 1e06:
        value /= 1024
        return f"{value:.2f} k"
    if 1e06 <= value < 1e09:
        value /= 1024 ** 2
        return f"{value:.2f} M"
    if value >= 1e09:
        value /= 1024 ** 3
        return f"{value:.2f} G"
    return f"{value:.2f} "

def convert_percent(_value):
    value = eval(_value)
    return f"{value:.2f}"