# -*- coding: utf-8 -*-

def convert_human(_value):
    if 1e03 <= _value < 1e06:
        _value /= 1024
        return f"{_value:.2f} k"
    if 1e06 <= _value < 1e09:
        _value /= 1024 ** 2
        return f"{_value:.2f} M"
    if _value >= 1e09:
        _value /= 1024 ** 3
        return f"{_value:.2f} G"
    return f"{_value:.2f} "

def convert_percent(_value):
    return f"{_value:.2f}"