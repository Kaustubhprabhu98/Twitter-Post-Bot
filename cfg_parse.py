import configparser


def parse_auth(section):
    cfg = configparser.ConfigParser()
    cfg.read("auth.cfg")
    return cfg[section]
