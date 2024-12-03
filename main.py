from tkinter import *
import pandas  # `pandas` is a popular Python library used for data manipulation and analysis. In this code
import random

# snippet, `pandas` is being used to read data from a CSV file containing Mandarin, English,
# and Spanish words. The `pandas.read_csv()` function is used to load the data from the CSV
# file into a DataFrame, which can then be used for further processing or analysis.

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
to_learn = {}


try:
    data = pandas.read_csv(
        "/Users/mei/projects/python_practice_flash_card_mand_to_span_app_capstone/data/words_to_learn.csv"
    )
    # print(data)
except FileNotFoundError:
    original_data = pandas.read_csv(
        "/Users/mei/projects/python_practice_flash_card_mand_to_span_app_capstone/data/mandarin_english_spanish_words.csv"
    )
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")  # use orient parameter to set
    # print(to_learn)

current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Mandarin")
    canvas.itemconfig(card_word, text=current_card["Mandarin"])
    print(current_card["Mandarin"])
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)  # after 3s


def is_known():
    # remove from to_learn list
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv(
        "/Users/mei/projects/python_practice_flash_card_mand_to_span_app_capstone/data/words_to_learn.csv",
        index=False,
    )
    next_card()


# Delay 3s
def flip_card():
    # Back Card
    canvas.itemconfig(card_title, text="Spanish")
    canvas.itemconfig(card_word, text=current_card["Spanish"])
    canvas.itemconfig(card_background, image=card_back_img)
    print(current_card["Spanish"])


window = Tk()
window.title("Mandarin English Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)  # after 3s
canvas = Canvas(width=800, height=526)

# Front Card
card_front_img = PhotoImage(
    file="/Users/mei/projects/python_practice_flash_card_mand_to_span_app_capstone/images/card_front.png"
)
card_back_img = PhotoImage(
    file="/Users/mei/projects/python_practice_flash_card_mand_to_span_app_capstone/images/card_back.png"
)

card_background = canvas.create_image(400, 263, image=card_front_img)

# Use for both Front and Back Card
card_title = canvas.create_text(400, 150, text="Title", font=TITLE_FONT)
card_word = canvas.create_text(400, 263, text="word", font=WORD_FONT)

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons

cross_image = PhotoImage(
    file="/Users/mei/projects/python_practice_flash_card_mand_to_span_app_capstone/images/wrong.png"
)

unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(
    file="/Users/mei/projects/python_practice_flash_card_mand_to_span_app_capstone/images/right.png"
)
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()


window.mainloop()
