# -*- coding: utf-8 -*-

import os, sys
import configparser
from PyQt5 import QtWidgets
from src.http.http_check import http_address_verification
from src.ui.dashboard import Dashboard
import src.metrics.metric as metric
import src.database.database as database

DATA_FOLDER_PATH = "data/"
CONFIG_FOLDER_PATH = "config/"

GLOBAL_CONFIG_FILE = "config/global.config.ini"
API_CONFIG_FILE = "config/api.config.ini"

def init_directories():
    """ 
    Initiation of the configuration and data directories, 
    creation if not present in the project. \n
    Checking the configuration files.

    TODO: Generate the configuration files if they doesn't exists.
    """

    print("Checking data directory ...")
    if not os.path.exists(DATA_FOLDER_PATH):
        try:
            print("DATA directory doesn't exist, creation ...")
            os.mkdir(DATA_FOLDER_PATH)
        except OSError:
            print("ERROR: DATA directory creation failed. \n")
        else:
            print("DATA directory successfully created.")

    print("Checking config directory ...")
    if not os.path.exists(CONFIG_FOLDER_PATH):
        try:
            print("CONFIG directory doesn't exist, creation ...")
            os.mkdir(CONFIG_FOLDER_PATH)
        except OSError:
            print("ERROR: CONFIG directory creation failed. \n")
        else:
            print("CONFIG directory successfully created.")

    print("Checking configuration files ...")
    if not os.path.exists(GLOBAL_CONFIG_FILE):
        try:
            raise FileNotFoundError
        except FileNotFoundError:
            print("ERROR: Can't find", GLOBAL_CONFIG_FILE, ". \nExiting.")
            sys.exit()
    if not os.path.exists(API_CONFIG_FILE):
        try:
            raise FileNotFoundError
        except FileNotFoundError:
            print("ERROR: Can't find", API_CONFIG_FILE, ". \nExiting.")
            sys.exit()

def run():
    metric_repo = []

    init_directories()

    database.create_db()
    db = database.connect_to_db()

    if not http_address_verification():
        exit()
        
    config_parser = configparser.ConfigParser()
    config_parser.read(API_CONFIG_FILE)
    for section in config_parser:
        for key in config_parser[section]:
            item = metric.MetricProcess(config_parser[section][key])
            item_post = metric.MetricPostProcess()
            item.add_observer(item_post)
            item.process()
            metric_repo.append(item.get_metric_set())

    application = QtWidgets.QApplication(sys.argv)
    butterscotch = Dashboard(metric_repo)
    sys.exit(application.exec_())
    

if __name__ == '__main__':
    run()