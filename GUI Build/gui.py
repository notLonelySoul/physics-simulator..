from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"F:\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1440x1024")
window.configure(bg = "#111111")


canvas = Canvas(
    window,
    bg = "#111111",
    height = 1024,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    295.0,
    234.0,
    1097.0,
    560.0,
    fill="#111111",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=51.0,
    y=293.0,
    width=80.0,
    height=80.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=47.0,
    y=394.0,
    width=84.0,
    height=83.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=51.0,
    y=501.0,
    width=80.0,
    height=80.0
)

canvas.create_rectangle(
    318.0,
    259.0,
    620.0,
    535.0,
    fill="#1E1E1E",
    outline="")

canvas.create_rectangle(
    759.0,
    259.0,
    1061.0,
    535.0,
    fill="#1E1E1E",
    outline="")

canvas.create_rectangle(
    143.0,
    144.0,
    1247.0,
    146.0000193119049,
    fill="#F5F5F5",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    179.0,
    69.0,
    image=image_image_1
)

canvas.create_text(
    248.0,
    47.0,
    anchor="nw",
    text="Dashboard",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 30 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=383.0,
    y=371.0,
    width=167.0,
    height=26.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=827.0,
    y=371.0,
    width=166.0,
    height=35.0
)
window.resizable(False, False)
window.mainloop()
