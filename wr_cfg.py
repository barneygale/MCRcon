import configparser
import os

config = configparser.ConfigParser()
def create_config(file_name):
    config.read(file_name)
    if not os.path.exists(file_name):
        config.add_section("Login_Data")
        config.set("Login_Data", "host", "")
        config.set("Login_Data", "port", "25575")

        config.add_section("Config")
        config.set("Config", "Default_Font", "Noto Sans")
        config.set("Config", "Version", "1.2")

        with open(file_name, "w") as configfile:
            config.write(configfile)
            configfile.close()

def read_config(file_name, section, option):
    config.read(file_name)
    return config.get(section, option)

def write_config(file_name, section, option, value):
    config.read(file_name)
    config.set(section, option, value)
    with open(file_name, "w") as configfile:
        config.write(configfile)
        configfile.close()
