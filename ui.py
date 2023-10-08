import socket
import mcrcon
import PySimpleGUIWx as sg
import configparser
from os.path import exists

# var ini
sg.theme("SystemDefaultForReal")
used_command_list = []
config_file = "config.ini"
sock = None
saved_host = None
saved_port = None

# read config
config = configparser.ConfigParser()
config.read(config_file)


"""
if not config.ini
create config.ini 
"""
if not exists("config.ini"):
    config.add_section("Login_Data")
    config.set("Login_Data", "host" , "")
    config.set("Login_Data", "port", "25575")

    with open(config_file, "w") as configfile:
        config.write(configfile)
        configfile.close()


saved_host = config.get("Login_Data", "host")
saved_port = config.get("Login_Data", "port")


# define layout
login_layout = [
                [sg.Text("Minecraft RCON login", font=("Segoe UI", 12))],
                [sg.Text("Host"), sg.InputText(key="-HOST-", default_text=saved_host, font=("Segoe UI", 12))],
                [sg.Text("Port"), sg.InputText(key="-PORT-", default_text=str(saved_port), font=("Segoe UI", 12))],
                [sg.Text("Password"), sg.InputText(key="-PASSWORD-", password_char="*", font=("Segoe UI", 12))],
                [sg.Button("Connect")],
]


manager_layout = [
    [sg.Text("Minecraft RCON Manager", font=("Segoe UI", 12))],
    [sg.Output(size=(80, 20), font=("Cascadia Mono", 12))],
    [sg.Text("Command", font=("Segoe UI", 12)), sg.InputText(key="-COMMAND-", font=("Cascadia Mono", 12), focus=True, size=(70, 1))],
    [sg.Button("Send", font=("Segoe UI", 12))],
]

# create manager window
def create_manager_window():
    return sg.Window("MCRcon GUI - manage", manager_layout)


while True:
    # create login_window in every loop if login_window is not defined
    login_window = sg.Window("MCRcon GUI - login", login_layout)

    # read window
    login_event, login_values = login_window.read()

    # read events
    if login_event == sg.WIN_CLOSED:
        break
    elif login_event == "Connect":
        host = login_values["-HOST-"]
        port = int(login_values["-PORT-"])
        password = login_values["-PASSWORD-"]

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))

            if mcrcon.login(sock, password):
                sg.popup(f"successfully connect to {host}:{port}")
                login_window.close()

                config.set("Login_Data", "host", value=host)
                config.set("Login_Data", "port", value=str(port))
                with open(config_file, "w") as configfile:
                    config.write(configfile)
                    configfile.close()

                manager_window = create_manager_window()

                while True:
                    manager_event, manager_values = manager_window.read()

                    if manager_event == sg.WIN_CLOSED:
                        sock.close()
                        manager_window.close()
                        break
                    elif manager_event == "Send":
                        manager_window["-COMMAND-"].update("")
                        if sock:
                            command = manager_values["-COMMAND-"]
                            manager_window["-COMMAND-"].update()
                            response = mcrcon.command(sock, command)
                            print(response)

            else:
                encoded_password = ""
                sg.popup_error("Wrong password")
                login_window.close()

        except Exception as e:
            sg.popup_error(f"error: {str(e)}")

if sock:
    sock.close()
