import configparser, pymysql, bcrypt, requests
import os

def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "DB_password", "DB_password_value")
    config.set("Settings", "mail_password", "mail_password_value")


    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    #msg = "{section} {setting} is {value}".format(section=section, setting=setting, value=value)
    #print(msg)
    return value


def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)


def delete_setting(path, section, setting):
    """
    Delete a setting
    """
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w") as config_file:
        config.write(config_file)


'''
if __name__ == "__main__":
    path = "settings.ini"
    DB_password = get_setting(path, 'Settings', 'DB_password')
    mail_password = get_setting(path, 'Settings', 'mail_password')

    #update_setting(path, "Settings", "font_size", "12")
    #delete_setting(path, "Settings", "font_style")
'''

path = "settings.ini"

#URL = get_setting(path, 'Settings', 'URL')
#print(URL)
