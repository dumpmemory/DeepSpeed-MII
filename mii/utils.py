'''
Copyright 2022 The Microsoft DeepSpeed Team
'''
import sys
import os
import logging
import importlib


def get_model_path():
    aml_model_dir = os.getenv('AZUREML_MODEL_DIR')
    if aml_model_dir is not None:
        return aml_model_dir

    mii_model_dir = os.getenv('MII_MODEL_DIR')

    if mii_model_dir is not None:
        return mii_model_dir

    #assert False, "MII_MODEL_DIR must be set if not running on AML. Current value is None"
    #TODO remove this and uncomment above line. Only doing this for debugging
    return "temp_model"


def is_aml():
    return os.getenv('AZUREML_MODEL_DIR') is not None


def set_model_path(model_path):
    os.environ['MII_MODEL_DIR'] = model_path


def import_score_file(model_name):
    #TODO: dynamically create score file for model in ~/.cache/mii path
    assert model_name == 'gpt2', "only gpt2 supported right now"
    import mii.models.gpt2.score as score
    # spec=importlib.util.spec_from_file_location('score', f'models/{model_name}/score.py')
    # score = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(score)
    return score


'''returns i) model path
          ii) enables grpc_server if runninng locally, else sets it to False
         iii) disables grpc_client if running locally as this would be done by client
            on a different process else sets it to tru
'''


def setup_generation_task():
    return get_model_path(), not is_aml(), is_aml()


log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


class LoggerFactory:
    @staticmethod
    def create_logger(name=None, level=logging.INFO):
        """create a logger
        Args:
            name (str): name of the logger
            level: level of logger
        Raises:
            ValueError is name is None
        """

        if name is None:
            raise ValueError("name for logger cannot be None")

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] "
            "[%(filename)s:%(lineno)d:%(funcName)s] %(message)s")

        logger_ = logging.getLogger(name)
        logger_.setLevel(level)
        logger_.propagate = False
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger_.addHandler(ch)
        return logger_


logger = LoggerFactory.create_logger(name="MII", level=logging.INFO)