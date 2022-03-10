parameters_description = { "address": ("string", "0.0.0.0"),
                           "port": ("int", 12345),
                           "userdb": ("string", "") }

class ConfigError(BaseException):
    pass


class Config:
    def __init__(self):
        self.params = dict()
        for p in parameters_description:
            self.params[p] = parameters_description[p][1]

    def add_param(self, name, value):
        if name in parameters_description:
            t = parameters_description[name][0]
            if t == "string":
                self.params[name] = value
            elif t == "int":
                self.params[name] = int(value)
            else:
                raise ConfigError("Unknown type for parameter \"%s\"" % name)

    def __getitem__(self, name):
        return self.params[name]
   

def load_config_from_content(content):
    config = Config()
    for line in content.split('\n'):
        if line == "":
            continue
        elts = line.split("=")
        config.add_param(elts[0].strip(), elts[1].strip())
    return config

def load_config_from_file(filename):
    f = open(filename)
    return load_config_from_content(f.read())


class UserDB:
    def __init__(self):
        self.users = dict()
        self.add_user("admin", "admin", True)
        self.add_user("guest", "guest", False)

    def add_user(self, login, password, admin):
        self.users[login] = { "login": login, "admin" : bool(admin), "password" : password }

    def get(self, login):
        try:
            return self.users[login]
        except Exception:
            return None

    def user_list(self):
        result = list(self.users.keys())
        result.sort()
        return result


def load_userdb_from_content(content):
    userdb = UserDB()
    for line in content.split('\n'):
        if line == "":
            continue
        login, password, admin = line.split(None, 2)
        userdb.add_user(login, password, admin)
    return userdb

def load_userdb_from_file(filename):
    f = open(filename)
    return load_userdb_from_content(f.read())
