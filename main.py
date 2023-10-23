from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
# get data from input
def save_data():
    website = website_entry.get()
    user = user_entry.get()
    password = password_entry.get()

    if website_entry.get() == "" or password_entry.get() == "":
        messagebox.showerror(message="Please don't leave anything blank")
    else:

        data = {website: {
            "email": user,
            "password": password,
        }
        }

        try:
            # Save data to a .json file
            with open("data.json", "r") as file:
                # Reading old data
                data_file = json.load(file)
        except FileNotFoundError:
            # saving dumped data
            with open("data.json", "w") as file:
                json.dump(data_file, file, indent=4)
        else:
            # Updating old data with new data
            data_file.update(data)
            with open("data.json", "w") as file:
                json.dump(data_file, file, indent=4)
        finally:
            website_entry.delete(0, END)
            user_entry.delete(0, END)
            password_entry.delete(0, END)
            print("Data Saved Successfully")


def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(message="No Data File Found")
    else:
        if website_entry.get() in data:
            email = data[website_entry.get()]["email"]
            password = data[website_entry.get()]["password"]
            messagebox.showinfo(title=website_entry.get(), message=f"Email:{email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Data not found", message="entry is not in the list of saved passwords")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(window, width=200, height=200)
canvas.grid(row=0, column=1, columnspan=2, padx=(0, 60))
image = PhotoImage(file="logo.png")
canvas.create_image(100, 0, image=image, anchor="n")

website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="e")
website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, sticky="w")

search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="e")

user_label = Label(text="Email/Username:")
user_label.grid(row=2, column=0, sticky="e")
user_entry = Entry(width=35)
user_entry.grid(row=2, column=1, columnspan=2, sticky="w")
user_entry.insert(0, "Johnsmith123@gmail.com")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e")  #
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="w")

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2, sticky="w")

add_button = Button(text="Add", width=36, command=save_data)
add_button.grid(row=4, column=1, columnspan=2, sticky="w")

window.mainloop()
