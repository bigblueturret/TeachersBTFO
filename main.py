import os
import re
import json
import time
import datetime
import platform
import subprocess
import urllib.request
from tkinter import *
from zipfile import ZipFile

hcpss_username = "nbagda3531"
hcpss_password = ""

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
    # import selenium
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys
except ModuleNotFoundError:
    if not pip_check():
        pip_init()
    pip_install("selenium")
    # import selenium
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys

try:
    import keyring
except ModuleNotFoundError:
    if not pip_check():
        pip_init()
    pip_install("keyring")
    import keyring

clear_console(host_int)
# user_browser = int(input("Which browser do you want to use?\n1) Chrome\n2) Firefox\n3) Safari\n"))

if host_int == 0:
    path = subprocess.check_output("echo %appdata%", shell=True).decode('UTF-8')
    path = path.replace("\\", "/").replace("\r\n", "")
    if not os.path.exists(path + "/teacherBTFO/"):
        os.mkdir(path + "/teacherBTFO/")
    if not os.path.exists(path + "/teacherBTFO/chrome-win/chrome.exe"):
        try:
            os.remove(path + "/teacherBTFO/chrome.zip")
            os.remove(path + "/teacherBTFO/chromedriver.zip")
        except FileNotFoundError:
            pass
        version_json = json.load(urllib.request.urlopen(
            "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o/Win%2FLAST_CHANGE"))
        chrome_version = json.load(urllib.request.urlopen(
            "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o/Win%2FLAST_CHANGE"))['metadata'][
            'cr-commit-position-number']
        chrome_generation = json.load(urllib.request.urlopen(
            "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o/Win%2F" + chrome_version + "%2Fchrome-win.zip"))[
            "generation"]
        latest_chrome = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win%2F" + chrome_version + "%2Fchrome-win.zip?generation=" + chrome_generation + "&alt=media"
        chromedriver_generation = json.load(urllib.request.urlopen(
            "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o/Win%2F" + chrome_version + "%2Fchromedriver_win32.zip"))[
            "generation"]
        latest_chromedriver = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win%2F" + chrome_version + "%2Fchromedriver_win32.zip?generation=" + chromedriver_generation + "&alt=media"
        urllib.request.urlretrieve(latest_chrome, path + "/teacherBTFO/chrome.zip")
        urllib.request.urlretrieve(latest_chromedriver, path + "/teacherBTFO/chromedriver.zip")
        with ZipFile(path + "/teacherBTFO/chrome.zip") as zipf:
            zipf.extractall(path=path + "/teacherBTFO/")
        with ZipFile(path + "/teacherBTFO/chromedriver.zip") as zipf:
            zipf.extractall(path=path + "/teacherBTFO/")
        try:
            os.remove(path + "/teacherBTFO/chrome.zip")
            os.remove(path + "/teacherBTFO/chromedriver.zip")
        except FileNotFoundError:
            pass
elif host_int == 1:
    # placeholder for mac commands
    pass
else:
    # placeholder for linux and other commands
    pass

def meet(username, password, meeting_id):
    boptions = webdriver.ChromeOptions()
    boptions.binary_location = path + "/teacherBTFO/chrome-win/chrome.exe"
    # boptions.headless = True
    boptions.add_argument('--disable-gpu')
    boptions.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path=path + "/teacherBTFO/chromedriver_win32/chromedriver.exe",
                              options=boptions)
    driver.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmeet.google.com%2F&sacu=1&hl=en_US&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    e = driver.find_element_by_id("identifierId")
    e.clear()
    e.send_keys(hcpss_username + "@inst.hcpss.org")
    driver.find_element_by_xpath("//*[text()='Next']").click()
    while True:
        try:
            driver.find_element_by_id("username")
            break
        except:
            time.sleep(0.05)
    driver.find_element_by_id("username").send_keys(username)
    e = driver.find_element_by_id("password")
    e.send_keys(password)
    e.send_keys(Keys.ENTER)
    while True:
        try:
            driver.find_element_by_xpath("//*[text()='Use a meeting code']").click()
            time.sleep(0.25)
            break
        except:
            time.sleep(0.05)
    driver.find_element_by_xpath("//input[@type='text']").send_keys(meeting_id)
    driver.find_element_by_xpath("//span[text()='Continue']").click()
    # missing code to actually join and to auto disconnect
    # add screenshot code for testing
    time.sleep(3)
    driver.close()

def write_json_config(data):
    with open(path + "/teacherBTFO/config.json", "w") as f:
        f.write(json.dumps(data, indent=4))

def refresh_schedule(slist, data):
    print(slist.winfo_children())
    for widget in slist.winfo_children():
        widget.destroy
    menu_row = 0
    data_column = 0
    for entry in data["schedule"]:
        menuitem = LabelFrame(slist)
        menuitem.grid(row=menu_row, column=0)
        namebox = Entry(menuitem, textvariable=config["schedule"][entry])
        menu_row += 1

def create_event(data):
    data["schedule"].append({1: {"name": "", "day": "", "time": "", "code": "", "case": ""}})
    refresh_schedule(schedule_list, config)

# meet(hcpss_username, hcpss_password, "test")

config = None
try:
    config = json.load(open(path + "/teacherBTFO/config.json"))
except FileNotFoundError:
    with open(path + "/teacherBTFO/config.json", "w") as f:
        f.write(json.dumps({"username": "", "schedule": []}, indent=4))
    config = json.load(open(path + "/teacherBTFO/config.json"))

window = Tk()
window.title("pog window")
window.geometry("600x300")

schedule_list = Listbox(window)
schedule_list.pack(pady=15)

# refresh_schedule(config)
menuitem = LabelFrame(schedule_list)
menuitem.grid(row=0, column=0)

var = StringVar(window)
testbox1 = OptionMenu(menuitem, var, *{"fefefefe1", "2fefefffef", "3gttthththt"})
testbox1.grid(row=0, column=0)
testbox2 = OptionMenu(menuitem, var, *{"fefefefe1", "2fefefffef", "3gttthththt"})
testbox2.grid(row=0,column=1)
testbox3 = OptionMenu(menuitem, var, *{"fefefefe1", "2fefefffef", "3gttthththt"})
testbox3.grid(row=0, column=2)

add_event_button = Button(window, text="add event", command=create_event(config))
add_event_button.pack()

window.protocol("WM_DELETE_WINDOW", write_json_config(config))
window.mainloop()
