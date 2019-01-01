import simplejson
import keyring
from keyrings.alt import Windows
keyring.set_keyring(Windows.RegistryKeyring())
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import sys
import random
import tkinter
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import OptionMenu
from tkinter import StringVar
from tkinter import Listbox
from tkinter import Scrollbar
from tkinter import messagebox
from tkinter import N, S, E, W
from tkinter import VERTICAL
from threading import Thread
from tkinter.messagebox import showinfo

'''Below module allows us to interact with Windows files.'''
import os

'''below 3 lines allows script to check the directory where it is executed, so it knows where to crete the excel file. I copied the whole block from stack overflow'''
abspath = os.path.abspath(__file__)
current_directory = os.path.dirname(abspath)
os.chdir(current_directory)

browser_waiting = random.randint(5,10)
gathering_waiting = random.randint(1,3)
like_waiting = random.randint(45, 90)
space_hiting = (random.randint(2, 10)) / 10

driver = webdriver.Chrome()

driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

#driver.get("https://www.instagram.com/lenuancierdujardinier/")
#followers_of_user = driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span''')
#print(len(followers_of_user.text))

def create_file_of_target_accounts_if_was_not_there():
    if not os.path.isfile('target_accounts.txt'):
        with open("target_accounts.txt", "w") as file_target_accounts:
            file_target_accounts.write("")

def create_liked_users_txt():
    if not os.path.isfile('liked_users.txt'):
        with open("liked_users.txt", "w") as file_liked_users:
            file_liked_users.write('')

def create_saved_account_txt():
    if not os.path.isfile('saved_account.txt'):
        with open("saved_account.txt", "w") as file_saved_account:
            file_saved_account.write("Enter account name to save")

def get_saved_account_txt():
    with open("saved_account.txt", "r") as file_saved_account:
        return file_saved_account.read()

"""
def get_list_of_target_accounts():
    list_of_target_accounts = []
    file_names = []
    for ___, ____, files in os.walk(current_directory):
        for filename in files:
            if "_followers.txt" in filename:
                file_names.append(filename)
    for file_object in file_names:
        if os.path.getsize(file_object) > 2:
           list_of_target_accounts.append(file_object)
    return list_of_target_accounts
"""

def get_list_of_target_accounts():
    with open("target_accounts.txt", "r") as target_accounts_file:
        list_of_target_accounts = []
        for line in target_accounts_file:
            list_of_target_accounts.append(line.strip())
    return list_of_target_accounts

def save_list_of_target_accounts(existing_list_of_target_accounts, new_list_of_target_accounts):
    list_of_target_accounts = existing_list_of_target_accounts
    for target_account in new_list_of_target_accounts:
        if target_account not in list_of_target_accounts:
            list_of_target_accounts.append(target_account)
    with open("target_accounts.txt", "w") as target_accounts_file:
        for target_account in list_of_target_accounts:
            target_accounts_file.write(target_account + "\n")

def gather_users():
    def slow_magic():
        create_file_of_target_accounts_if_was_not_there()
        list_of_users_to_save = []
        account_to_inspect = str(get_who_to_spy.get())
        insert_text("Extracting users from " + str(get_who_to_spy.get()))
        time.sleep(gathering_waiting)
        driver.get("https://www.instagram.com/" + account_to_inspect)
        time.sleep(gathering_waiting)
        driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a""").click()
        time.sleep(gathering_waiting)
        index_of_try = 0
        actions = ActionChains(driver)
        while index_of_try < 20:
            starting_length = len(list_of_users_to_save)
            driver.find_element_by_class_name("isgrP").click()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(space_hiting)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(space_hiting)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(space_hiting)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(space_hiting)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(space_hiting)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(space_hiting)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(space_hiting)
            temp_names = driver.find_elements_by_class_name('FPmhX')
            for link in temp_names:
                if link.get_attribute('href') not in list_of_users_to_save:
                    list_of_users_to_save.append(link.get_attribute('href'))
            index_of_try += 1
            insert_text("Loop went " + str(index_of_try) + " times. " + str(len(list_of_users_to_save)) + " users saved.")
            ending_length = len(list_of_users_to_save)
            if starting_length == ending_length:
                break
            time.sleep(gathering_waiting)
        existing_list_of_target_accounts = get_list_of_target_accounts()
        save_list_of_target_accounts(existing_list_of_target_accounts, list_of_users_to_save)
        insert_text("Extracting done!")
    executing = Thread(target=slow_magic)
    executing.start()

"""
def extracting_user_to_like(account_to_inspect):      
    with open(account_to_inspect + "_followers.txt", "r") as file_gathered_users:
        users_to_like = eval(file_gathered_users.read())
        user_to_like = users_to_like.pop(0)
    with open(account_to_inspect + "_followers.txt", "w") as file_gathered_users:
        file_gathered_users.write(str(users_to_like))
    return user_to_like
"""

def extracting_user_to_like():
    users_to_like = []
    with open("target_accounts.txt", "r") as file_gathered_users:
        for line in file_gathered_users:
            users_to_like.append(line.strip("\n"))
    try:    
        user_to_like = users_to_like.pop(0)
    except:
        messagebox.showinfo("Attention", "No users left in the list")
        user_to_like = ""
    with open("target_accounts.txt", "w") as target_accounts_file:
        for target_account in users_to_like:
            target_accounts_file.write(target_account + "\n")
    return user_to_like

def like_gathered_users():
    def slow_magic():
        likes_given = 0
        try:
            number_of_likes = int(get_number_of_likes.get())
            insert_text("Starting liking")
        except:
            messagebox.showinfo("Attention", "Set the number of accounts to like")
            number_of_likes = 0
        while likes_given < number_of_likes:
            user_to_like = extracting_user_to_like()
            with open("liked_users.txt", "r") as file_liked_users:
                liked_users = []
                for line in file_liked_users:
                    liked_users.append(line.strip("\n"))
            if user_to_like not in liked_users:
                likes_given = liking_user(user_to_like, likes_given)
                liked_users.append(user_to_like)
                with open("liked_users.txt", "w") as file_liked_users:
                    for liked_user in liked_users:
                        file_liked_users.write(liked_user + "\n")
    executing = Thread(target=slow_magic)
    executing.start()


def liking_user(user_to_like, likes_given):
    driver.get(user_to_like)
    time.sleep(browser_waiting)
    move_to_next_user = 0
    try:
        driver.find_element_by_class_name('''eLAPa''')
    except:
        move_to_next_user = 1
    if move_to_next_user == 0:
        followers_of_user = driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span''')
        if len(followers_of_user.text) < 4:
            try:
                driver.find_element_by_class_name('''eLAPa''').click()
                time.sleep(like_waiting)
                driver.find_element_by_class_name("coreSpriteHeartOpen").click()
                likes_given += 1
                insert_text(user_to_like + " liked (" + str(likes_given) + ")")
            except:
                insert_text(user_to_like + " has no photo to like")
        else:
            insert_text(user_to_like + " pro account")
    return likes_given

def add_account_name_and_password():
    account_name = save_account_name_variable.get()
    account_password = save_account_password_variable.get()
    if account_name != "Enter account name to save" and account_password != "Password":
        keyring.set_password("instagram", account_name, account_password)
        with open("saved_account.txt", "w") as file_saved_acount:
            file_saved_acount.write(str(account_name))
            showinfo("Done!", str(account_name) + " and password saved")
    else:
        showinfo("Warning!", "please, make sure to provide account name and password")
    save_account_name_variable.set("Enter account name to save")
    save_account_password_variable.set("Password")
    
def get_list_of_accounts():
    with open("saved_account.txt", "r") as file_saved_accounts:
        saved_accounts = eval(file_saved_accounts.read())
    return saved_accounts

"""
def create_dropdown_list_of_saved_accounts():
    global login_drop_down_list_of_accounts_var
    global login_drop_down_list_of_accounts
    list_of_accounts = get_list_of_accounts()
    login_drop_down_list_of_accounts_var = StringVar(main_window_of_gui)
    login_drop_down_list_of_accounts_var.set(list_of_accounts[-1])
    if login_drop_down_list_of_accounts.winfo_exists() == 1:
        login_drop_down_list_of_accounts.destroy()
    login_drop_down_list_of_accounts = OptionMenu(main_window_of_gui, login_drop_down_list_of_accounts_var, *list_of_accounts)
    login_drop_down_list_of_accounts.configure(width=15)
    login_drop_down_list_of_accounts.grid(row = 2, column = 0)
"""     

def login_with_selected_account():
    chosen_login = save_account_name_variable.get()
    chosen_password = str(keyring.get_password("instagram", chosen_login))
    driver.find_element_by_name("username").send_keys(chosen_login)
    time.sleep(gathering_waiting)
    driver.find_element_by_name("password").send_keys(chosen_password)
    time.sleep(gathering_waiting)
    driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button''').click()

def insert_text(text):
    text_box.insert('end', text)
    text_box.see("end")




create_liked_users_txt()
create_saved_account_txt()

main_window_of_gui = tkinter.Tk()
main_window_of_gui.title("Инстаграм помошник 01.01.2019")
main_window_of_gui.wm_attributes("-topmost", 1)

save_account_name_variable = StringVar()
save_account_name_variable.set(get_saved_account_txt())
save_account_password_variable = StringVar()
save_account_password_variable.set("Password")

save_account_name = Entry(main_window_of_gui, width=30, textvariable = save_account_name_variable)
save_account_name.grid(row = 0, column = 0)
save_account_password = Entry(main_window_of_gui, width=30, show="*", textvariable = save_account_password_variable)
save_account_password.grid(row = 1, column = 0)

save_account_name_and_password_button = Button(main_window_of_gui, text = "save", width = 5, height = 1, command = add_account_name_and_password)
save_account_name_and_password_button.grid(row = 0, column = 1)

#login_drop_down_list_of_accounts = Label(main_window_of_gui, text = "Place holder")


login_button = Button(main_window_of_gui, text = "Log in", width = 15, height = 1, command = login_with_selected_account)
login_button.grid(row = 2, column = 1)


ask_who_to_spy = Label(main_window_of_gui, text = "Get followers from who? : ")
get_who_to_spy = Entry(main_window_of_gui, width=15)
ask_who_to_spy.grid(row = 3, column = 0)
get_who_to_spy.grid(row = 3, column = 1)
"""
ask_number_of_followers = Label(main_window_of_gui, text = "How many followers\nsave to a list? : ")
get_number_of_followers = Entry(main_window_of_gui, width=15)
ask_number_of_followers.grid(row = 4, column = 0)
get_number_of_followers.grid(row = 4, column = 1)
"""
ask_number_of_likes = Label(main_window_of_gui, text = "How many likes to give? : ")
get_number_of_likes = Entry(main_window_of_gui, width=15)
ask_number_of_likes.grid(row = 5, column = 0)
get_number_of_likes.grid(row = 5, column = 1)

gather_button = Button(main_window_of_gui, text ="Save followers\nto a list", width = 15, height = 3, command = gather_users)
gather_button.grid(row = 6, column = 0)
like_button = Button(main_window_of_gui, text ="Like users", width = 15, height = 3, command = like_gathered_users)
like_button.grid(row = 6, column = 1)

text_box = Listbox(main_window_of_gui, height=8)
text_box.grid(column=0, row=7, columnspan=6, sticky=(N,W,E,S))  # columnspan − How many columns widgetoccupies; default 1.
main_window_of_gui.grid_columnconfigure(0, weight=1)
main_window_of_gui.grid_rowconfigure(12, weight=1)
#scroll bar
my_scrollbar = Scrollbar(main_window_of_gui, orient=VERTICAL, command=text_box.yview)
my_scrollbar.grid(column=3, row=7, sticky=(N,S))
#attaching scroll bar to text box
text_box['yscrollcommand'] = my_scrollbar.set


main_window_of_gui.mainloop()
"""
https://sites.google.com/a/chromium.org/chromedriver/downloads
"""