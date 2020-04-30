import os
import re
import datetime
import platform
import subprocess

host = platform.system()
if host == "Windows":
    host_int = 0
elif host == "Darwin":
    host_int = 1
elif host == "Linux":
    host_int = 2
else:
    # unknown host; try to run anyway
    host_int = 3

def clear_console(host_os):
    if host_int == 0:
        os.system("cls")
    elif host_int == 2 or 3:
        os.system("clear")
    else:
        print("could not determine host os to clear screen")


def pip_check():
    output = str(subprocess.check_output("pip"))
    if "pip <command> [options]" in output:
        return True
    else:
        return False


def pip_init():
    subprocess.call("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    subprocess.call("python get-pip.py --user")
    os.remove("get-pip.py")


def pip_install(package):
    status = subprocess.call("pip install " + package + " --user")
    if status != 0:
        print("error while installing " + package + " using pip.")
        print("please manually install " + package + " for python and try again.")
        raise Exception("pip install error")


try:
    from selenium import webdriver
except ModuleNotFoundError:
    if not pip_check():
        pip_init()
    pip_install("selenium")
    from selenium import webdriver
try:
    import keyring
except ModuleNotFoundError:
    if not pip_check():
        pip_init()
    pip_install("keyring")
    import keyring

clear_console(host_int)
user_browser = int(input("Which browser do you want to use?\n1) Chrome\n2) Firefox\n3) Safari\n"))

# commands to run on host regardless of browser
if host_int == 0:
    path = subprocess.check_output("echo %appdata%", shell=True).decode('UTF-8')
    path = path.replace("\\", "/").replace("\r\n", "")
    if not os.path.exists(path + "/teacherBTFO/"):
        os.mkdir(path + "/teacherBTFO/")
elif host_int == 1:
    # placeholder for mac commands
    pass
else:
    # placeholder for linux and other commands
    pass

if user_browser == 1:
    if host_int == 0:
        if not os.path.exists(path + "/teacherBTFO/chromedriver.exe"):
            subprocess.call("curl https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_win32.zip -o %APPDATA%/teacherBTFO/chromedriver.zip", shell=True)
            subprocess.call("powershell.exe Expand-Archive -LiteralPath %APPDATA%/teacherBTFO/chromedriver.zip -DestinationPath %APPDATA%/teacherBTFO/", shell=True)
            if not os.path.exists(path + "/teacherBTFO/chromedriver.exe"):
                print("error during driver download")
                exit(1)
        driver = webdriver.Chrome(executable_path=path + "/teacherBTFO/chromedriver.exe")
elif user_browser == 2:
    if host_int == 0:
        if not os.path.exists(path + "/teacherBTFO/geckodriver.exe"):
            extracted_url = subprocess.check_output("curl https://github.com/mozilla/geckodriver/releases/", shell=True).decode('UTF-8')
            extracted_url = "https://github.com" + re.findall(r"\/mozilla\/geckodriver\/releases\/download/v[0-9].[0-9][0-9].[0-9]/geckodriver-v[0-9].[0-9][0-9].[0-9]-win64.zip", extracted_url)[0]
            subprocess.call("curl -L " + extracted_url + " -o %APPDATA%/teacherBTFO/firefoxdriver.zip", shell=True)
            subprocess.call("powershell.exe Expand-Archive -LiteralPath %APPDATA%/teacherBTFO/firefoxdriver.zip -DestinationPath %APPDATA%/teacherBTFO/", shell=True)
            if not os.path.exists(path + "/teacherBTFO/"):
                print("error during driver download")
                exit(1)
        driver = webdriver.Firefox(executable_path=path + "/teacherBTFO/geckodriver.exe")
elif user_browser == 3:
    input("Safari is untested and may not work. Press enter to continue.")
    if host_int != 2:
        print("Safari is not supported on Windows, Linux, or other operating systems")
        exit(1)
    driver = webdriver.Safari()