# -*- coding: utf-8 -*-

import json
import io

def get_json_from_file(filename):
    with open(filename) as json_input:
        json_data = json.load(json_input)
        json_input.close()

    parse_json_file(json_data, filename)

    return json_data

def parse_json_file(json_data, filename):
    with open(filename, "w") as json_input:
        json_input.write(json.dumps(json_data, indent=4))
        json_input.close()


def get_data_from_json(data, value):
    stream = data['data']['result'][0]['value'][1]
    value = eval(stream)
    return value