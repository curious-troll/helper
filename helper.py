import keyring
from keyrings.alt import Windows
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import random
from tkinter import Tk
from tkinter import Label, Button, Entry, Checkbutton
from tkinter import StringVar, IntVar
from tkinter import Listbox
from tkinter import Scrollbar
from tkinter import messagebox
from tkinter import N, S, E, W, END
from tkinter import VERTICAL
from threading import Thread

'''Below module allows us to interact with Windows files.'''
import os

keyring.set_keyring(Windows.RegistryKeyring())

'''below 3 lines allows script to check the directory where it is executed, so it knows where to crete the excel file. I copied the whole block from stack overflow'''
abspath = os.path.abspath(__file__)
current_directory = os.path.dirname(abspath)
os.chdir(current_directory)


def browser_waiting():
    return random.randint(5, 10)


def gathering_waiting():
    return random.randint(1, 3)


def like_waiting():
    return random.randint(10, 30)


def rest_waiting():
    return random.randint(3600, 4200)
    insert_text("J'attends. Il est " + get_timestamp())


def get_timestamp():
    return str(time.strftime("%Hh%Ms%S"))


def space_hiting():
    return (random.randint(2, 10)) / 10


LOGGED_IN = 0

NEED_TO_STOP = 0

driver = ""



def start_web_driver():
    global driver
    options = webdriver.ChromeOptions()
    if display_browser_var.get() == 1:
        options.add_argument('headless')
    pc_browser = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    options.add_argument(pc_browser)
    options.add_experimental_option('prefs', {'intl.accept_languages': "fr-fr"})
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)


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
            file_saved_account.write("Ton adress e-mail.")


def create_seeder_accounts_txt():
    if not os.path.isfile('seeder_accounts.txt'):
        with open("seeder_accounts.txt", "w") as file_seeder_accounts:
            file_seeder_accounts.write("")


def get_saved_account_txt():
    with open("saved_account.txt", "r") as file_saved_account:
        return file_saved_account.read()


def save_seeder_account():
    global driver
    def slow_magic():
        seeder_list = []
        with open("seeder_accounts.txt", "r") as file_gathered_seeders:
            for line in file_gathered_seeders:
                seeder_list.append(line.strip("\n"))
        seeder_account = get_who_to_spy.get()
        seeder_list.append(seeder_account)
        with open("seeder_accounts.txt", "w") as seeder_accounts_file:
            for seeder_account in seeder_list:
                seeder_accounts_file.write(seeder_account + "\n")
        insert_text(seeder_account + " ajoute dans la liste a " + get_timestamp())
        get_who_to_spy.delete(0, END)
    executing = Thread(target=slow_magic)
    executing.start()


def save_list_of_target_accounts(existing_list_of_target_accounts, new_list_of_target_accounts):
    list_of_target_accounts = existing_list_of_target_accounts
    for target_account in new_list_of_target_accounts:
        if target_account not in list_of_target_accounts:
            list_of_target_accounts.append(target_account)


def gather_users():
    create_file_of_target_accounts_if_was_not_there()
    list_of_users_to_save = []
    account_to_inspect = str(get_seeder_account())
    insert_text("Extracting users from " + account_to_inspect)
    time.sleep(gathering_waiting())
    driver.get("https://www.instagram.com/" + account_to_inspect + "/")
    time.sleep(gathering_waiting())
    driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span""").click()
    time.sleep(gathering_waiting())
    index_of_try = 0
    actions = ActionChains(driver)
    while index_of_try < 20:
        starting_length = len(list_of_users_to_save)
        driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/ul""").click()
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(space_hiting())
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(space_hiting())
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(space_hiting())
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(space_hiting())
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(space_hiting())
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(space_hiting())
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(space_hiting())
        temp_names = driver.find_elements_by_class_name('FPmhX')
        for link in temp_names:
            if link.get_attribute('href') not in list_of_users_to_save:
                list_of_users_to_save.append(link.get_attribute('href'))
        index_of_try += 1
        insert_text("Loop went " + str(index_of_try) + " times. " + str(len(list_of_users_to_save)) + " users saved.")
        ending_length = len(list_of_users_to_save)
        if starting_length == ending_length:
            break
        time.sleep(gathering_waiting())
    with open("target_accounts.txt", "w") as target_accounts_file:
        for target_account in list_of_users_to_save:
            target_accounts_file.write(target_account + "\n")
    insert_text(str(ending_length) + "comptes-cibles recupere a " + get_timestamp())


def get_seeder_account():
    seeder_list = []
    with open("seeder_accounts.txt", "r") as file_gathered_seeders:
        for line in file_gathered_seeders:
            seeder_list.append(line.strip("\n"))
    try:    
        seeder_account = seeder_list.pop(0)
    except:
        messagebox.showinfo("Attention", "No seeder left in the list")
        seeder_account = ""
    with open("seeder_accounts.txt", "w") as seeder_accounts_file:
        for seeder_account in seeder_list:
            seeder_accounts_file.write(seeder_account + "\n")
    return seeder_account


def extracting_user_to_like():
    users_to_like = []
    with open("target_accounts.txt", "r") as file_gathered_users:
        for line in file_gathered_users:
            users_to_like.append(line.strip("\n"))
    try:
        user_to_like = users_to_like.pop(0)
    except:
        insert_text("Pas de compte cible dans la liste. J'essay d'en recupere. Il est " + get_timestamp())
        user_to_like = ""
    with open("target_accounts.txt", "w") as target_accounts_file:
        for target_account in users_to_like:
            target_accounts_file.write(target_account + "\n")
    if user_to_like == "":
        gather_users()
        user_to_like = extracting_user_to_like()
    return user_to_like


def like_gathered_users():
    def slow_magic():
        global driver
        global LOGGED_IN
        start_web_driver()
        while LOGGED_IN == 0:
            try:
                insert_text("J'essaye de me conecter a " + save_account_name_variable.get())
                login_with_selected_account()
            except:
                insert_text("J'ai pas reussi a me connecter. Je re-essay.")
        likes_given = 0
        try:
            number_of_likes = int(get_number_of_likes.get())
            insert_text("Je commence a distribuer des likes. Il est " + get_timestamp())
        except:
            messagebox.showinfo("Attention!", "Il faut preciser le nombre de like a distribuer.")
            number_of_likes = 0
        while likes_given < number_of_likes:
            for _ in range(20):
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
            insert_text("Je prends une pause entre des series de like. Il est " + get_timestamp())
            rest_waiting()
        messagebox.showinfo("Voila !", str(likes_given) + "Likes distribue. Il est " + get_timestamp())
    executing = Thread(target=slow_magic)
    executing.start()


def liking_user(user_to_like, likes_given):
    global NEED_TO_STOP
    global driver
    driver.get(user_to_like)
    time.sleep(browser_waiting())
    move_to_next_user = 0
    try:
        driver.find_element_by_class_name('''eLAPa''')
    except:
        move_to_next_user = 1
        insert_text(user_to_like + " n'a pas de photo a liker.")
    if move_to_next_user == 0:
        followers_of_user = driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span''')
        if len(followers_of_user.text) < 4:
            try:
                driver.find_element_by_class_name('''eLAPa''').click()
                time.sleep(like_waiting())
                driver.find_element_by_xpath('''/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button/span''').click()
                likes_given += 1
                insert_text(user_to_like + " liked (" + str(likes_given) + ")")
            except:
                insert_text("Pas reussi a donner un like a " + user_to_like)
        else:
            insert_text(user_to_like + " compte Pro. Je passe.")
    return likes_given


def add_account_name_and_password():
    account_name = save_account_name_variable.get()
    account_password = save_account_password_variable.get()
    if account_name != "Ton adress e-mail." and account_password != "Password":
        keyring.set_password("instagram", account_name, account_password)
        with open("saved_account.txt", "w") as file_saved_acount:
            file_saved_acount.write(str(account_name))
            messagebox.showinfo("Super !", str(account_name) + " et mot de pass enregistres !")
    else:
        messagebox.showinfo("Attention !", "Il faut tapper ton mot de pass")
    save_account_password_variable.set("Password")


def get_list_of_accounts():
    with open("saved_account.txt", "r") as file_saved_accounts:
        saved_accounts = eval(file_saved_accounts.read())
    return saved_accounts


def login_with_selected_account():
    global LOGGED_IN
    global driver
    chosen_login = save_account_name_variable.get()
    chosen_password = str(keyring.get_password("instagram", chosen_login))
    driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
    driver.find_element_by_name("username").send_keys(chosen_login)
    time.sleep(gathering_waiting())
    driver.find_element_by_name("password").send_keys(chosen_password)
    time.sleep(gathering_waiting())
    driver.find_element_by_css_selector('''#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div.Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB > button > div''') .click()
    insert_text("Connecte avec " + chosen_login)
    time.sleep(3)
    LOGGED_IN = 1


def insert_text(text):
    text_box.insert('end', text)
    text_box.see("end")


create_liked_users_txt()
create_saved_account_txt()
create_seeder_accounts_txt()
create_file_of_target_accounts_if_was_not_there()

main_window_of_gui = Tk()
main_window_of_gui.title("Insta liker 08/05/2019")
main_window_of_gui.wm_attributes("-topmost", 1)

display_browser_var = IntVar()

display_browser_toggle = Checkbutton(main_window_of_gui, text="Cacher le navigateur.", variable=display_browser_var)
display_browser_toggle.grid(row = 0, column = 2, columnspan = 1)

save_account_name_variable = StringVar()
save_account_name_variable.set(get_saved_account_txt())
save_account_password_variable = StringVar()
save_account_password_variable.set("Password")

save_account_name = Entry(main_window_of_gui, width=30, textvariable = save_account_name_variable)
save_account_name.grid(row = 0, column = 0)
save_account_password = Entry(main_window_of_gui, width=30, show="*", textvariable = save_account_password_variable)
save_account_password.grid(row = 1, column = 0)

save_account_name_and_password_button = Button(main_window_of_gui, text = "Enregistrer", width = 10, height = 1, command = add_account_name_and_password)
save_account_name_and_password_button.grid(row = 0, column = 1)

ask_who_to_spy = Label(main_window_of_gui, text = "Compte-source ?")
get_who_to_spy = Entry(main_window_of_gui, width=15)
ask_who_to_spy.grid(row = 3, column = 0)
get_who_to_spy.grid(row = 3, column = 1)

ask_number_of_likes = Label(main_window_of_gui, text = "Combien de likes ?")
get_number_of_likes = Entry(main_window_of_gui, width=15)
get_number_of_likes.insert("end", '799')
ask_number_of_likes.grid(row = 4, column = 0)
get_number_of_likes.grid(row = 4, column = 1)

save_seeder_button = Button(main_window_of_gui, text ="Ajouter\n compte-source", width = 15, height = 3, command = save_seeder_account)
save_seeder_button.grid(row = 3, column = 2, rowspan = 2)

like_button = Button(main_window_of_gui, text ="Commencer !", width = 15, height = 3, command = like_gathered_users)
like_button.grid(row = 6, column = 2)

text_box = Listbox(main_window_of_gui, height=8)
text_box.grid(column=0, row=7, columnspan=6, sticky=(N,W,E,S))
main_window_of_gui.grid_columnconfigure(0, weight=1)
main_window_of_gui.grid_rowconfigure(7, weight=1)
my_scrollbar = Scrollbar(main_window_of_gui, orient=VERTICAL, command=text_box.yview)
my_scrollbar.grid(column=5, row=7, sticky=(N,S))
text_box['yscrollcommand'] = my_scrollbar.set

main_window_of_gui.mainloop()
driver.close()
