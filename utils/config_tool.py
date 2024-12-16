import configparser
import os
import logging
logger = logging.getLogger(__name__)

# SAMPLE_LOCK_PARAMS_KEYS = [
#     "initial_range",
#     "initial_step",
#     "reference_mode",
#     "reference_axis",
#     "move_amplitude",
#     "move_time",
#     "peak_fit",
#     "sample_lock_active_axes",
#     "scale_factors",
#     "t_settle",
#     "kp",
#     "ki",
#     "ki2",
# ]

SAMPLE_LOCK_PARAMS_KEYS = [
    "reference_range_[um]",
    "reference_step_size_[um]",
    "mode",
    "axis",
    "move_amplitude_[um]",
    "move_time",
    "peak_fit",
    "sample_lock_active_axes",
    "scale_factors",
    "settling_time_[s]",
    "k_p",
    "k_i",
    "k_i2",
]



def read_config(file_path):
    if not os.path.exists(file_path):
        logger.error(f"Config file {file_path} not found!")
        raise FileNotFoundError(f"Config file {file_path} not found!")
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


def create_config(file_path):
    config = configparser.ConfigParser()
    return config


def update_config_by_section(file_path, section, params):
    try:
        config = read_config(file_path)
    except FileNotFoundError:
        config = create_config(file_path)
    if not config.has_section(section):
        config.add_section(section)
    config[section] = params
    with open(file_path, "w") as configfile:
        config.write(configfile)


def update_config_by_value(file_path, section, key, value):
    config = read_config(file_path)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)
    with open(file_path, "w") as configfile:
        config.write(configfile)

def update_config_by_dict(file_path, section, dictionary):
    if not os.path.exists(file_path):
        with open(file_path, "w") as configfile:
            configfile.write("")
    config = read_config(file_path)
    if not config.has_section(section):
        config.add_section(section)
    for key in dictionary.keys():
        config.set(section, key, str(dictionary[key]))
    with open(file_path, "w") as configfile:
        config.write(configfile)


def set_array_in_config(file_path, section, key, values):
    value_str = ",".join(str(x) for x in values)
    update_config_by_value(file_path, section, key, value_str)


def get_array_from_config(config, section, key):
    value_str = config.get(section, key)
    return [item.strip() for item in value_str.split(",")]

def convert_dict_str2float(dictionary): # <------ sample_lock params parser
    new_d = {}
    for key in dictionary.keys():
        val = dictionary[key]
        if val == '':
            new_d[key.lower()] = None
            continue
        if val == '[]':
            new_d[key.lower()] = []
            continue
        if val[0] == '[' and val[-1] == ']':
            ticks = '\"' if '\"' == val[1] else '\''
            new_d[key.lower()] = [float(x.replace(ticks, "")) for x in val[1:-1].split(',')]
            continue
        try:
            new_d[key.lower()] = float(val)
        except:
            new_d[key.lower()] = val

    return new_d

