import config

from config import ConfigError

def test_address_port_params():
    config_content = "address = 10.0.0.1\nport = 123\n"
    c = config.load_config_from_content(config_content)
    assert c['address'] == "10.0.0.1"
    assert c['port'] == 123

def test_default_address_port():
    c = config.Config()
    assert c['address'] == "0.0.0.0"
    assert c['port'] == 12345

def test_user_database():
    users = config.UserDB()
    admin_user = users.get("admin")
    assert admin_user is not None
    assert admin_user["admin"] == True
    assert admin_user["password"] == "admin"

    users.add_user("toto", "tititoto", False)
    toto_user = users.get("toto")
    assert toto_user is not None
    assert toto_user["admin"] == False
    assert toto_user["password"] == "tititoto"

    users.add_user("tota", "tititota", "False")
    toto_user = users.get("tota")
    assert toto_user is not None
    assert toto_user["admin"] == False
    assert toto_user["password"] == "tititota"

    users.add_user("toti", "tititotd", "True")
    toto_user = users.get("toti")
    assert toto_user is not None
    assert toto_user["admin"] == True
    assert toto_user["password"] == "tititotd"

    try:
        users.add_user("tote", "tititote", "Whatever")
        assert False
    except ConfigError:
        assert True

def test_load_userdb():
    users = config.load_userdb_from_content("toto tititoto True")
    user = users.get("toto")
    assert user is not None
