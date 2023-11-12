import socket
import mcrcon
import configparser
from os.path import exists
import os_detect, sys
import wr_cfg

config_file = "config.ini"

wr_cfg.create_config(config_file)

# customize for different platform
os = os_detect.detect(sys.platform)
if os == "Windows":
    import PySimpleGUIWx as sg
elif os == "MacOS" or "Linux" or "aix" or "unknown":
    import PySimpleGUI as sg


# var ini
sg.theme("SystemDefaultForReal")
used_command_list = []
sock = None
saved_host = None
saved_port = None
version = wr_cfg.read_config(config_file, "Config", "Version")


# Read saved config
DeFont = wr_cfg.read_config(config_file, "Config", "Default_Font")
saved_host = wr_cfg.read_config(config_file, "Login_Data", "host")
saved_port = wr_cfg.read_config(config_file, "Login_Data", "port")


# define layout
def make_window(type):
    login_layout = [
                    [sg.Text("Minecraft RCON login", font=(DeFont, 12))],
                    [sg.Text("Host"), sg.InputText(key="-HOST-", default_text=saved_host, font=(DeFont, 12))],
                    [sg.Text("Port"), sg.InputText(key="-PORT-", default_text=str(saved_port), font=(DeFont, 12))],
                    [sg.Text("Password"), sg.InputText(key="-PASSWORD-", password_char="*", font=(DeFont, 12))],
                    [sg.Button("Connect")],
    ]

    manager_layout = [
        [sg.Text("Minecraft RCON Manager", font=(DeFont, 12))],
        [sg.Output(size=(80, 20), font=("Cascadia Mono", 12))],
        [sg.Text("Command", font=(DeFont, 12)), sg.InputText(key="-COMMAND-", font=("Cascadia Mono", 12), focus=True, size=(70, 1))],
        [sg.Button("Up"), sg.Button("Down"), sg.Button("Send", font=(DeFont, 12))],
    ]


    if type == "login":
        login_window = sg.Window("MCRcon GUI - login", login_layout, resizable=False)
        return login_window

    if type == "manager":
        manager_window = sg.Window("MCRcon GUI - manage", manager_layout, resizable=False)
        return manager_window


while True:
    # create login_window in every loop if login_window is not defined
    login_window = make_window("login")

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

                wr_cfg.write_config(config_file, "Login_Data", "host", value=host)
                wr_cfg.write_config(config_file, "Login_Data", "port", value=str(port))

                manager_window = make_window("manager")

                while True:
                    manager_event, manager_values = manager_window.read()

                    if manager_event == sg.WIN_CLOSED:
                        sock.close()
                        manager_window.close()
                        break

                    elif manager_event == "Send":
                        manager_window["-COMMAND-"].update("")
                        used_command_list.append(manager_values["-COMMAND-"])
                        lenth = len(used_command_list)
                        line = lenth

                        if sock:
                            command = manager_values["-COMMAND-"]

                            response = mcrcon.command(sock, command)
                            print(response)

                    elif manager_event == "Up":
                        try:
                            line -= 1
                            manager_window["-COMMAND-"].update(used_command_list[line])
                        except:
                            pass

                    elif manager_event == "Down":
                        try:
                            line += 1
                            manager_window["-COMMAND-"].update(used_command_list[line])
                        except:
                            manager_window["-COMMAND-"].update("")

            else:
                encoded_password = ""
                sg.popup_error("Wrong password")
                login_window.close()

        except Exception as e:
            sg.popup_error(f"error: {str(e)}")

if sock:
    sock.close()