import simplejson
from selenium import webdriver
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
from tkinter import StringVar
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

driver = webdriver.Chrome()
driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

if not os.path.isfile('./liked_users.txt'):
    with open("liked_users.txt", "w") as file_liked_users:
        file_liked_users.write('["one","two"]')

if not os.path.isfile('./vip_accounts.txt'):
    with open("vip_accounts.txt", "w") as file_vip_accounts:
        file_vip_accounts.write('["one","two"]')


def gather_i_follow(my_account):
    users_to_save = []
    driver.get("https://www.instagram.com/" + my_account)
    time.sleep(gathering_waiting)
    driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a""").click()
    time.sleep(gathering_waiting)
    actions = ActionChains(driver)
    for i in range(5):
        try:
            scroll_window = driver.find_element_by_class_name("""PZuss""")
            scroll_window.click()
            time.sleep(1)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(0.25)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(0.25)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(0.25)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(0.25)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(gathering_waiting)
            temp_names = driver.find_elements_by_class_name('FPmhX')
            for link in temp_names:
                if link.get_attribute('href') not in users_to_save:
                    users_to_save.append(link.get_attribute('href'))
        except Exception as e:
            print(e)
    return users_to_save

def gather_my_followers(my_account):
    users_to_save = []
    driver.get("https://www.instagram.com/" + my_account)
    time.sleep(gathering_waiting)
    driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a""").click()
    time.sleep(gathering_waiting)
    actions = ActionChains(driver)
    for i in range(5):
        try:
            scroll_window = driver.find_element_by_class_name("""PZuss""")
            scroll_window.click()
            time.sleep(1)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(0.25)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(0.25)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(0.25)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(0.25)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(gathering_waiting)
            temp_names = driver.find_elements_by_class_name('FPmhX')
            for link in temp_names:
                if link.get_attribute('href') not in users_to_save:
                    users_to_save.append(link.get_attribute('href'))
        except Exception as e:
            print(e)
    return users_to_save


def gather_users():
    something_went_wrong = 0
    users_to_save = []
    account_to_inspect = str(get_who_to_spy.get())
    time.sleep(gathering_waiting)
    driver.get("https://www.instagram.com/" + account_to_inspect)
    time.sleep(gathering_waiting)
    try:
        driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a""").click()
    except:
        something_went_wrong = 1
        showinfo("Warning!", "Was uanble to click the right thing")
    if something_went_wrong == 0:
        time.sleep(gathering_waiting)
        actions = ActionChains(driver)
        number_of_followers_to_save = int(get_number_of_followers.get())
        index_of_try = 0
        while len(users_to_save) < number_of_followers_to_save:
            if index_of_try < 15:
                try:
                    scroll_window = driver.find_element_by_class_name("""PZuss""")
                    scroll_window.click()
                    time.sleep(1)
                    actions.send_keys(Keys.SPACE).perform()
                    time.sleep(0.25)
                    actions.send_keys(Keys.SPACE).perform()
                    time.sleep(0.25)
                    actions.send_keys(Keys.SPACE).perform()
                    time.sleep(0.25)
                    actions.send_keys(Keys.SPACE).perform()
                    time.sleep(0.25)
                    actions.send_keys(Keys.SPACE).perform()
                    time.sleep(gathering_waiting)
                    temp_names = driver.find_elements_by_class_name('FPmhX')
                    for link in temp_names:
                        if link.get_attribute('href') not in users_to_save:
                            users_to_save.append(link.get_attribute('href'))
                    with open(account_to_inspect + "_followers.txt", "w") as my_gathered_users: 
                        my_gathered_users.write(str(users_to_save))
                    index_of_try += 1
                    print("Loop went " + str(index_of_try) + " times")
                    print(len(users_to_save))
                except Exception as e:
                    print('error scrolling down web element', e)
                gathered_users_text_variable.set("Users saved: " + str(len(users_to_save)))
                main_window_of_gui.update_idletasks()
                time.sleep(gathering_waiting)
            else:
                number_of_followers_to_save = 0

def extracting_user_to_like(account_to_inspect):      
    with open(account_to_inspect + "_followers.txt", "r") as file_gathered_users:
        users_to_like = eval(file_gathered_users.read())
        user_to_like = users_to_like.pop(0)
    with open(account_to_inspect + "_followers.txt", "w") as file_gathered_users:
        file_gathered_users.write(str(users_to_like))
    print("User chosen:" + user_to_like)
    return user_to_like

def like_gathered_users():
    account_to_inspect = str(get_who_to_spy.get())
    number_of_likes = int(get_number_of_likes.get())
    likes_given = 0
    while likes_given < number_of_likes:
        user_to_like = extracting_user_to_like(account_to_inspect)
        with open("liked_users.txt", "r") as file_liked_users:
            liked_users = eval(file_liked_users.read())
        if user_to_like not in liked_users:
            liking_user(user_to_like)
            liked_users.append(user_to_like)
            with open("liked_users.txt", "w") as file_liked_users:
                file_liked_users.write(str(liked_users))
            print(user_to_like + "saved and liked")
            likes_given += 1
        like_text_variable.set("Users liked: " + str(likes_given))
        main_window_of_gui.update_idletasks()

def liking_user(user_to_like):
    driver.get(user_to_like)
    time.sleep(browser_waiting)
    try:
        first_photo = driver.find_element_by_class_name('''eLAPa''')
        first_photo.click()
        time.sleep(like_waiting)
        driver.find_element_by_class_name("coreSpriteHeartOpen").click()
    except:
        print("Couldn't like")

def cleaning_account():
    account_to_clean = str(get_account_to_clean.get())
    with open("vip_accounts.txt", "r") as file_vip_accounts:
        vip_accounts = eval(file_vip_accounts.read())
    my_followers = gather_my_followers(account_to_clean)
    i_follow = gather_i_follow(account_to_clean)
    accounts_kicked = 0
    if len(gather_my_followers(account_to_clean)) > 100:
        for account in i_follow:
            if account not in my_followers and account not in vip_accounts:
                try:
                    driver.get(account)
                    time.sleep(browser_waiting)
                    driver.find_element_by_class_name('''_5f5mN''').click()
                    time.sleep(browser_waiting)
                    driver.find_element_by_xpath('''/html/body/div[3]/div/div/div/div[3]/button[1]''').click()
                    accounts_kicked += 1
                    print(account + " kicked")
                    print(str(accounts_kicked) + " accounts kicked")
                    time.sleep(browser_waiting)
                except:
                    cleaning_account()
        showinfo("Job's done", str(accounts_kicked) + " accounts kicked")


    
def follow_user():
    account_to_inspect = str(get_who_to_spy.get())
    number_to_follow = int(get_number_of_follows.get())
    followed = 0
    while followed < number_to_follow:
        user_to_like = extracting_user_to_like(account_to_inspect)
        with open("liked_users.txt", "r") as file_liked_users:
            liked_users = eval(file_liked_users.read())
        if user_to_like not in liked_users:
            time.sleep(browser_waiting)
            driver.get(user_to_like)
            time.sleep(browser_waiting)
            try:
                first_photo = driver.find_element_by_class_name('''eLAPa''')
                first_photo.click()
                time.sleep(like_waiting)
                driver.find_element_by_class_name("coreSpriteHeartOpen").click()
                time.sleep(like_waiting)
                driver.find_element_by_class_name('''oW_lN''').click()
                followed += 1
                print(user_to_like + " followed")
            except:
                print("Couldn't like and follow")
            liked_users.append(user_to_like)
            with open("liked_users.txt", "w") as file_liked_users:
                file_liked_users.write(str(liked_users))
            print(user_to_like + " saved")
        like_text_variable.set("Users followed: " + str(followed))
        main_window_of_gui.update_idletasks()


main_window_of_gui = tkinter.Tk()
main_window_of_gui.title("Инстаграм помошник 22.10.2018")
main_window_of_gui.wm_attributes("-topmost", 1)

like_text_variable = StringVar()
like_text_variable.set("Users liked: 0")
gathered_users_text_variable = StringVar()
gathered_users_text_variable.set("Users saved: 0")



ask_who_to_spy = Label(main_window_of_gui, text = "Get followers from who? : ")
get_who_to_spy = Entry(main_window_of_gui, width=15)
ask_who_to_spy.grid(row = 2, column = 0)
get_who_to_spy.grid(row = 2, column = 1)
ask_number_of_followers = Label(main_window_of_gui, text = "How many followers\nsave to a list? : ")
get_number_of_followers = Entry(main_window_of_gui, width=15)
ask_number_of_followers.grid(row = 3, column = 0)
get_number_of_followers.grid(row = 3, column = 1)
ask_number_of_likes = Label(main_window_of_gui, text = "How many likes to give? : ")
get_number_of_likes = Entry(main_window_of_gui, width=15)
ask_number_of_likes.grid(row = 4, column = 0)
get_number_of_likes.grid(row = 4, column = 1)
ask_number_of_follows = Label(main_window_of_gui, text = "How many users to follow? : ")
get_number_of_follows = Entry(main_window_of_gui, width=15)
ask_number_of_follows.grid(row = 5, column = 0)
get_number_of_follows.grid(row = 5, column = 1)

ask_account_to_clean = Label(main_window_of_gui, text = "Which account to clean? : ")
ask_account_to_clean.grid(row = 10, column = 0)
get_account_to_clean = Entry(main_window_of_gui, width=15)
get_account_to_clean.grid(row = 10, column = 1)
clean_account_button = Button(main_window_of_gui, text ="Clean account", width = 15, height = 1, command = cleaning_account)
clean_account_button.grid(row = 11, column = 1)

gather_button = Button(main_window_of_gui, text ="Save followers\nto a list", width = 15, height = 3, command = gather_users)
like_button = Button(main_window_of_gui, text ="Like users", width = 15, height = 3, command = like_gathered_users)
follow_button = Button(main_window_of_gui, text ="Follow users", width = 15, height = 3, command = follow_user)
gather_button.grid(row = 6, column = 0)
like_button.grid(row = 6, column = 1)
follow_button.grid(row = 7, column = 0)

users_saved_in_a_list = Label(main_window_of_gui, textvariable = gathered_users_text_variable)
users_saved_in_a_list.grid(row = 8, column = 0)
users_liked = Label(main_window_of_gui, textvariable = like_text_variable)
users_liked.grid(row = 9, column = 0)
main_window_of_gui.mainloop()