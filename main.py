# import pandas
from tkinter import *
from random import randint
import pandas

BACKGROUND_COLOR = "#B1DDC6"

try:
    words_data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    words_data = pandas.read_csv("data/french_words.csv")
words_list_dict = words_data.to_dict(orient='records')
current_word = {}


def change_word():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = words_list_dict[randint(0, len(words_list_dict))]
    french_words = current_word['French']
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=french_words, fill='black')
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global current_word
    canvas.itemconfig(canvas_image, image=card_back)
    english_word = current_word['English']
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=english_word, fill='white')


# ---------------------------- Creating a new csv file of yet unlearnt French words ------------------------- #
def remove_word():
    words_list_dict.remove(current_word)
    new_words_csv = pandas.DataFrame(words_list_dict)
    new_words_csv.to_csv('words_to_learn.csv', index=False)
    change_word()
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Flash Cards")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)


card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text='', font=('Arial', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=('Arial', 60, 'bold'))
change_word()

# Buttons
right_button = Button(image=right, highlightthickness=0, command=remove_word)
right_button.grid(row=1, column=1)
wrong_button = Button(image=wrong, highlightthickness=0, command=change_word)
wrong_button.grid(row=1, column=0)

window.mainloop()
