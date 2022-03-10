import codecs
import socket
from threading import Thread
from config import *

context_counter = 0

class Context:
    def __init__(self):
        global context_counter
        self.current_user = None
        self.socket = None
        self.id = context_counter
        context_counter += 1

    def send_to_socket(self, msg):
        if self.socket:
            try:
                self.socket.send(codecs.encode(msg + "\n", "utf8"))
            except Exception:
                pass

    def check_current_user(self, login):
        return self.current_user is not None and self.current_user['login'] == login


class QuitCommand(BaseException):
    pass


def handle_client(server, context):
    socket = context.socket
    try:
        while True:
            request = socket.recv(16384).strip()
            request = codecs.decode(request, "utf8")
            result, answer = server.execute(context, request)
            if result:
                prefix = b"+ "
            else:
                prefix = b"- "
            answer = codecs.encode(answer, "utf8")
            socket.send(b"%s%s\n" % (prefix, answer))
    except QuitCommand:
        pass
    except Exception as e:
        print("[C%d] Error while handling the socket (Reason %s)" % (context.id, e))

    server.destroy_context(context)
    try:
        socket.close()
        print("[C%d] Connection closed" % context.id)
    except Exception:
        pass


class Server:
    def __init__(self, config):
        self.config = config
        self.contexts = []
        if config['userdb']:
            self.users = load_userdb_from_file(config['userdb'])
        else:
            self.users = UserDB()

    def new_context(self):
        result = Context()
        self.contexts.append(result)
        return result

    def destroy_context(self, context):
        self.contexts = list(filter(lambda c : c.id != context.id, self.contexts))

    def execute(self, context, line):
        if line == "":
            return False, "Empty request"
        command_and_args = line.split()
        command = command_and_args[0]
        args = command_and_args[1:]
        if command == "login":
            login, password = args
            login = login.strip()
            password = password.strip()
            temp = self.users.get(login)
            if temp and temp['password'] == password:
                context.current_user = temp
                return True, ("Welcome %s" % login)
            else:
                return False, "Invalid user or password"

        elif command == "logout":
            if context.current_user:
                login = context.current_user['login']
                context.current_user = None
                return True, ("Bye %s" % login)
            else:
                return False, "You are not currently logged in"

        elif command == "whoami":
            if context.current_user:
                login = context.current_user['login']
                return True, ("You are %s, silly" % login)
            else:
                return False, "You are not currently logged in"

        elif command == "list":
            if context.current_user:
                logins = self.users.user_list()
                result = []
                for l in logins:
                    relevant_contexts = filter(lambda c: c.check_current_user(l), self.contexts)
                    connected = list(relevant_contexts) != []
                    if connected:
                        result.append("*%s" % l)
                    elif context.current_user['admin']:
                        result.append("%s" % l)
                return True, ", ".join(result)
            else:
                return False, "You are not currently logged in"

        elif command == "print":
            if args == []:
                msg = "nothing"
            else:
                print_cmd, msg = line.split(None, 1)
                msg = "\"%s\"" % msg
            if context.current_user:
                username = context.current_user['login']
            else:
                username = "Anonymous coward"
            msg = "%s says %s" % (username, msg)
            print(msg)
            for c in self.contexts:
                c.send_to_socket(msg)
            return True, "Message posted"

        elif command == "help":
            return True, "Valid commands are: help, list, login, logout, print, quit, whoami"

        elif command == "quit":
            raise QuitCommand

        else:
            return False, "Invalid command"

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address_and_port = self.config['address'], self.config['port']
        server_socket.bind(address_and_port)
        server_socket.listen(5)
        print("[S] Server listening on %s:%d" % address_and_port)

        while True:
            context = self.new_context()
            try:
                s, client_address = server_socket.accept()
                context.socket = s
                print("[C%d] Connection accepted from %s" % (context.id, client_address))
                t = Thread(target=handle_client, args=(self, context))
                t.start()
            except Exception as e:
                print("[C%d] Failed (Reason: %s)" % (context.id, e))
                self.destroy_context(context)


if __name__ == "__main__":
    try:
        config = load_config_from_file("config")
    except Exception:
        config = Config()
    server = Server(config)
    try:
        server.run()
    except KeyboardInterrupt:
        print()
        pass
