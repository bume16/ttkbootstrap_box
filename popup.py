import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk


def focus_in(e, entry, value):
    if value.get() == entry.placeholder_text:  # placegholder가 있으면
        entry.delete(0, "end")  # 엔트리 값 삭제(시작위치:0, 끝위치:"end")
        entry.configure(foreground="black")  # 글자색(fg-foreground)은 검정색으로


def focus_out(e, entry, value):
    if not value.get():  # 엔트리에 값이 입력되어 있지 않으면
        entry.configure(foreground="gray")  # 글자색을 회색으로
        entry.insert(0, entry.placeholder_text)  # placeholder 재삽입

def open_popup():
    # Create secondary (or popup) window.
    popup = ttk.Toplevel()
    popup.title("Secondary Window")
    popup.config(width=200, height=100)

    # Create a text
    value = ttk.StringVar() 
    valueEntry = ttk.Entry(popup, textvariable=value, style='warning.TEntry')
    valueEntry.placeholder_text = "Input your value"
    valueEntry.insert(0, valueEntry.placeholder_text)
    valueEntry.bind("<FocusIn>", lambda event : focus_in(event, valueEntry, value))
    valueEntry.bind("<FocusOut>", lambda event : focus_out(event, valueEntry, value))
    
    valueEntry.place(x=5, y=5)

    # Create a button to close (destroy) this window.
    button_close = ttk.Button(
        popup,
        text="Close window",
        command=popup.destroy
    )
    button_close.place(x=30, y=40)
