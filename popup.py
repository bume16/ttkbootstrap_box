import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class Popup :
    """
    ttk 팝업을 띄우기 위해 구현한 클래스

    Methods:
        open_popup(parent, width, height)

    """


def _focus_in_(e, entry, value):
    if value.get() == entry.placeholder_text:  # placegholder가 있으면
        entry.delete(0, "end")  # 엔트리 값 삭제(시작위치:0, 끝위치:"end")
        entry.configure(foreground="black")  # 글자색(fg-foreground)은 검정색으로


def _focus_out_(e, entry, value):
    if not value.get():  # 엔트리에 값이 입력되어 있지 않으면
        entry.configure(foreground="gray")  # 글자색을 회색으로
        entry.insert(0, entry.placeholder_text)  # placeholder 재삽입

def open_popup(parent, width, height):
    '''
    팝업 윈도우를 띄우는 메소드.

    Args:
        parent(ttk.window)  : 부모 윈도우 객체
        width(integer)      : 팝업 width size
        height(integer)     : 팝업 height size

    '''
    # 부모 윈도우의 위치와 크기를 가져옴
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    # 자식 윈도우를 중앙에 위치시키기 위한 좌표 계산
    x = parent_x + (parent_width - width) // 2
    y = parent_y + (parent_height - height) // 2

    # Create secondary (or popup) window.
    popup = ttk.Toplevel()
    popup.title("POP-UP")
    popup.geometry(f"{width}x{height}+{x}+{y}")

    # Create a text
    value = ttk.StringVar() 
    valueEntry = ttk.Entry(popup, textvariable=value, style='warning.TEntry')
    valueEntry.placeholder_text = "Input value"
    valueEntry.insert(0, valueEntry.placeholder_text)
    valueEntry.bind("<FocusIn>", lambda event : _focus_in_(event, valueEntry, value))
    valueEntry.bind("<FocusOut>", lambda event : _focus_out_(event, valueEntry, value))
    
    
    valueEntry.place(x=5, y=5, width=width-10, height=30)

    # Create a button to close (destroy) this window.
    button_close = ttk.Button(
        popup,
        text="Confirm",
        command=popup.destroy
    )
    btnWidth = 80
    btnX = (width-btnWidth)/2
    button_close.place(x=btnX, y=40, width=btnWidth)
