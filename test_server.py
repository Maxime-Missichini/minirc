import config
import server

# login/logout

def test_successful_login1():
    c = config.Config()
    s = server.Server(c)
    context = s.new_context()

    result, answer = s.execute(context, "login admin admin")
    assert result == True
    assert answer == "Welcome admin"
    assert context.current_user['admin'] == True


def test_successful_login2():
    c = config.Config()
    s = server.Server(c)
    context = s.new_context()

    result, answer = s.execute(context, "login guest guest")
    assert result == True
    assert answer == "Welcome guest"
    assert context.current_user['admin'] == False


def test_failed_login():
    c = config.Config()
    s = server.Server(c)
    context = s.new_context()

    result, answer = s.execute(context, "login pouet pouet")
    assert result == False
    assert answer == "Invalid user or password"

def test_failed_login2():
    c = config.Config()
    s = server.Server(c)
    context = s.new_context()

    result, answer = s.execute(context, "login guest notguest")
    assert result == False
    assert answer == "Invalid user or password"

    result, answer = s.execute(context, "whoami")
    assert result == False
    assert answer == "You are not currently logged in"


def test_logout():
    c = config.Config()
    s = server.Server(c)
    context = s.new_context()

    result, answer = s.execute(context, "logout")
    assert result == False
    assert answer == "You are not currently logged in"

    result, answer = s.execute(context, "login admin admin")
    assert result == True

    result, answer = s.execute(context, "logout")
    assert result == True
    assert answer == "Bye admin"




# whoami

def test_whoami():
    c = config.Config()
    s = server.Server(c)
    context = s.new_context()

    result, answer = s.execute(context, "whoami")
    assert result == False
    assert answer == "You are not currently logged in"

    result, answer = s.execute(context, "login admin admin")
    assert result == True

    result, answer = s.execute(context, "whoami")
    assert result == True
    assert answer == "You are admin, silly"



# Invalid command

def test_invalid_command():
    c = config.Config()
    s = server.Server(c)
    context = s.new_context()

    result, answer = s.execute(context, "invalid")
    assert result == False
    assert answer == "Invalid command"



# List

def test_list_users_from_admin():
    c = config.Config()
    s = server.Server(c)
    context = s.new_context()
    result, answer = s.execute(context, "login admin admin")

    result, answer = s.execute(context, "list")
    assert result == True
    assert answer == "*admin, guest"


def test_list_users_from_guest():
    c = config.Config()
    s = server.Server(c)
    context = s.new_context()

    result, answer = s.execute(context, "list")
    assert result == False
    assert answer == "You are not currently logged in"

    result, answer = s.execute(context, "login guest guest")

    result, answer = s.execute(context, "list")
    assert result == True
    assert answer == "*guest"


def test_list_users_with_multiple_contexts():
    c = config.Config()
    s = server.Server(c)
    context1 = s.new_context()
    s.execute(context1, "login admin admin")
    context2 = s.new_context()
    s.execute(context2, "login guest guest")

    result, answer = s.execute(context1, "list")
    assert result == True
    assert answer == "*admin, *guest"

    result, answer = s.execute(context2, "list")
    assert result == True
    assert answer == "*admin, *guest"

    s.destroy_context(context1)

    result, answer = s.execute(context2, "list")
    assert result == True
    assert answer == "*guest"
