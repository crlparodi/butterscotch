# -*- coding: utf-8 -*-

def convert_human(value):
    if value >= 1e03 and value < 1e06:
        value /= 1024
        return f"{value:.2f} k"
    if value >= 1e06 and value < 1e09:
        value /= 1024 ** 2
        return f"{value:.2f} M"
    if value >= 1e09:
        value /= 1024 ** 3
        return f"{value:.2f} G"
    return f"{value:.2f}"

def convert_percent(value):
    return f"{value:.2f}"