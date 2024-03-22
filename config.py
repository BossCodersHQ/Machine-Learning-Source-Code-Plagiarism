import os

import logging
import config


def initialise_logging():
    logging.basicConfig(level=config.get_log_level(), format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')


def get_log_level():
    return os.environ.get('LOG_LEVEL', 'INFO')

def get_training_directory():
    return os.environ.get('TRAINING_DIRECTORY', "./data/SOCO.14/train/java/")

def get_test_directory():
    return os.environ.get('TEST_DIRECTORY', "./data/SOCO.14/train/java/")


def get_similarity_threshold():
    return os.environ.get('SIMILARITY_THRESHOLD', 0.3)


def get_rf_model_path():
    return os.environ.get('RF_MODEL_PATH', "./data/models/rf_model.pkl")