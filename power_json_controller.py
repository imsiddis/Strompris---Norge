# This program will check if the power_json_controller.py script is running.
# If it is not running, it will start it.
# If it is running, it will do nothing.
# The program is run on an Ubuntu server.


import os
import time
import subprocess


def waiting_animation(duration):
    animation = "|/-\\"
    idx = 0
    for i in range(duration):
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)

def control_logs():
    # This function will log whenever the power_json_controller.py script is started through this script.
    # It will log the date and time in the control_logs.txt file.
    # Open the control_logs.txt file.
    with open("control_logs.txt", "a") as control_logs:
        # Write the date and time to the file in format ""[DD-MM-YYY HH:MM:SS] - Started power_json_controller.py.""
        control_logs.write(f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] - Started power_json_controller.py.\n")

#==================#
# Json Constructor #
#==================#

def check_if_running():
    # This function will check if the power_json_controller.py script is running.
    # Get the current processes.
    process_status = subprocess.run(["ps", "-fA"], stdout=subprocess.PIPE)
    # Get the output of the command.
    output = process_status.stdout.decode("utf-8")
    # Check if the power_json_constructor.py script is running.
    if "power_json_constructor.py" in output:
        # If it is running, return True.
        return True
    else:
        # If it is not running, return False.
        print("Not running")
        return False

def start_script():
    # This function will start the power_json_controller.py script.
    # Start the script.
    print("Starting power_json_constructor.py...")
    os.system("python3 power_json_constructor.py &")

def main():
    # This function will check if the power_json_controller.py script is running.
    # If it is not running, it will start it.
    # If it is running, it will do nothing.
    # Check if the power_json_controller.py script is running.
    if check_if_running() == False:
        # If it is not running, start it.
        start_script()
        print("power_json_constructor.py started.")
        # Log that the script was started.
        control_logs()
    else:
        # If it is running, do nothing.
        print("power_json_constructor.py is already running.")

#=======================#
# TeamViewer Controller #
#=======================#
def check_teamviewer_running():
    # This function will check if the power_json_controller.py script is running.
    # Get the current processes.
    process_status = subprocess.run(["ps", "-fA"], stdout=subprocess.PIPE)
    # Get the output of the command.
    output = process_status.stdout.decode("utf-8")
    # Check if the power_json_constructor.py script is running.
    if "/opt/teamviewer/tv_bin/TeamViewer_Desktop" in output:
        # If it is running, return True.
        return True
    else:
        # If it is not running, return False.
        print("Not running")
        return False

def start_teamviewer():
    # This function will start the power_json_controller.py script.
    # Start the script.
    print("Starting TeamViewer...")
    os.system("teamviewer &")

def teamviewer_controller():
    # This function will check if the TeamViewer is running.
    # If it is not running, it will start it.
    # If it is running, it will do nothing.
    # Check if the teamviewer is running.
    if check_teamviewer_running() == False:
        # If it is not running, start it.
        start_teamviewer()
        check_teamviewer_running()
        if check_teamviewer_running() == True:
            print("TeamViewer started.")
    else:
        # If it is running, do nothing.
        print("TeamViewer is already running.")


while True:
    main()
    teamviewer_controller()
    waiting_animation(200)
