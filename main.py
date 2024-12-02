import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import popup as popup

def resizeImage(rawImage, ratio=1.0):
    
    width = int(rawImage.width * ratio)
    height = int(rawImage.height * ratio)
    
    return ImageTk.PhotoImage(rawImage.resize((width,height)))

# get mouse position
def motion(event):
    """ Get mouse position """
    x,y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    print("{}|{}".format(x,y))

def leftClicked(event):
    """ Get mouse click position """
    x,y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    print(">>>{},{}<<<".format(x,y))

    for img in canvas.image_store:
        if is_inside_rectangle(x, y, img[1]):
            if img[2] == '2번':
                popup.open_popup(root, 120,80)
            print(f"{img[2]} 사각형 내부 클릭! ({x}, {y})")

def create_transparent_rectangle(canvas, name, rect_coords, color, alpha):
    # 좌표 추출
    x1, y1, x2, y2 = rect_coords
    # 투명한 이미지를 생성합니다.
    width, height = int(x2 - x1), int(y2 - y1)
    image = Image.new("RGBA", (width, height), color + (int(alpha * 255),))
    tk_image = ImageTk.PhotoImage(image)
    
    # 캔버스에 이미지를 배치합니다.
    canvas.create_image(x1, y1, anchor="nw", image=tk_image)
    # 참조가 유지되도록 저장
    canvas.image_store.append([tk_image,(x1, y1, x2, y2),name])  # 참조 유지

def is_inside_rectangle(x, y, rect_coords):
    """
    마우스 좌표가 사각형 내부에 있는지 확인하는 함수.
    
    Args:
        x (int): 마우스의 x 좌표.
        y (int): 마우스의 y 좌표.
        rect_coords (tuple): 사각형의 좌표 (x1, y1, x2, y2).

    Returns:
        bool: 사각형 내부에 있으면 True, 그렇지 않으면 False.
    """
    x1, y1, x2, y2 = rect_coords
    return x1 <= x <= x2 and y1 <= y <= y2

# 마우스 이벤트 핸들러
def on_mouse_move(event):
    mouse_x, mouse_y = event.x, event.y
    if is_inside_rectangle(mouse_x, mouse_y, rectangle_coords):
        print(f"마우스가 사각형 내부에 있습니다! ({mouse_x}, {mouse_y})")
    else:
        print(f"마우스가 사각형 바깥에 있습니다. ({mouse_x}, {mouse_y})")


root = ttk.Window()
root.title("LDO Resistor Calculator")
root.geometry("600x480")

#Notebook 위젯 생성
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

#첫 번째 프레임생성  
# frame1 = ttk.Frame(notebook, padding=10)
# notebook.add(frame1, text="LT3020EMS8")

# label1 = ttk.Label(frame1, image=image1, padding=4)
# label1.pack()

# 1번째 프레임생성  
frame1 = ttk.Frame(notebook, padding=0)
notebook.add(frame1, text="LT3020EMS8")

rawImage = Image.open("./resource/images/LT3020EMS8_OPERATOR_PIC1.png")
image1 = resizeImage(rawImage, ratio=0.8)

canvas = ttk.Canvas(frame1, width=image1.width(), height=image1.height(), relief="solid", bd=1, background="red")
# canvas.bind("<Motion>", on_mouse_move)
canvas.bind("<Button-1>", leftClicked)

canvas.pack(padx=0, pady=0)

# 이미지 참조를 저장할 리스트
canvas.image_store = []
rectangle_coords = (105,65,135,95)

canvas.create_image(image1.width()/2,image1.height()/2,image=image1)
# canvas.create_polygon(229.0,38.0,247.0,38.0,226.0,62.0,243.0,64.0)
create_transparent_rectangle(canvas, name="1번", rect_coords=(105,65,135,95), color=(255,0,0), alpha=0.5)
create_transparent_rectangle(canvas, name="2번", rect_coords=(205,65,235,95), color=(255,0,0), alpha=0.5)

print(canvas.image_store)
# canvas.image_names = image1




# b1 = ttk.Button(root, text="Solid Button", bootstyle=SUCCESS)
# b1.pack(side=LEFT, padx=5, pady=10)

# b2 = ttk.Button(root, text="Outline Button", bootstyle=(SUCCESS, OUTLINE))
# b2.pack(side=LEFT, padx=5, pady=10)


    


# APP 실행
root.mainloop()