import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import popup as popup

class Mainframe:
    def __init__(self, config):
        self.config = config  # 설정 값 저장
        
    def resizeImage(self, rawImage, ratio=1.0):
        
        width = int(rawImage.width * ratio)
        height = int(rawImage.height * ratio)
        
        return ImageTk.PhotoImage(rawImage.resize((width,height)))

    # get mouse position
    def motion(self, event):
        """ Get mouse position """
        x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        print("{}|{}".format(x,y))

    def leftClicked(self, event):
        """ Get mouse click position """
        x,y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        print(">>>{},{}<<<".format(x,y))

        for img in self.canvas.image_store:
            if self.is_inside_rectangle(x, y, img[1]):
                # if img[2] == '2번':
                print(f"{img[2]} 사각형 내부 클릭! ({x}, {y})")
                result = popup.open_popup(self.root,img[2], 120,80)
                print(f"입력값 = {result}")

                oldId = self.get_object_id(img[2])
                print(f"old id = {oldId}")
                # if oldId is not None : 
                #     self.clear_canvas_obj(self.canvas, self.get_object_id(img[2]))

                obj_id = self.create_box_text(self.canvas, img[1], f"{img[2]} = {result}")                
                self.add_object_id(img[2], obj_id)
                
    def create_transparent_rectangle(self, canvas, name, rect_coords, color, alpha):
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

    def create_fill_rectangle(self, canvas, rect_coords, color):
        # 좌표 추출
        x1, y1, x2, y2 = rect_coords
        # 투명한 이미지를 생성합니다.
        width, height = int(x2 - x1), int(y2 - y1)
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        
    def is_inside_rectangle(self, x, y, rect_coords):
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

    def calc_rectangle_center(self, rect_coords):
        x1, y1, x2, y2 = rect_coords
        return (x2-x1)/2 + x1, (y2-y1)/2 + y1

    def create_only_text(self, canvas, x, y, text, color="black", font=("Arial", 12), anchor="w"):
        canvas.create_text(x, y, text=text, fill=color, font=font, anchor=anchor)

    def create_box_text(self, canvas, box, text, fcolor="black", bcolor="white", font=("Arial", 12), anchor="center"):
        self.create_fill_rectangle(canvas, box, bcolor)
        x, y = self.calc_rectangle_center(box)
        print(f"{x} {y}")
        canvas.create_text(x, y, text=text, fill=fcolor, font=font, anchor=anchor)
    
    def clear_text_and_images(self, canvas):
        # Canvas에 있는 모든 객체의 ID를 가져옵니다.
        for item in canvas.find_all():  
            # 객체의 타입을 확인합니다.
            item_type = canvas.type(item)
            print(item_type)
            # 타입이 text 또는 image인 경우 해당 객체를 삭제합니다.
            # if item_type in ('text', 'image'):
            if item_type in ('text'):
                canvas.delete(item)
    def clear_canvas_obj(self, canvas, id):
        if id is None:
            canvas.delete(id)


    # 마우스 이벤트 핸들러
    def on_mouse_move(self, event):
        mouse_x, mouse_y = event.x, event.y
        # if is_inside_rectangle(mouse_x, mouse_y, rectangle_coords):
        #     print(f"마우스가 사각형 내부에 있습니다! ({mouse_x}, {mouse_y})")
        # else:
        #     print(f"마우스가 사각형 바깥에 있습니다. ({mouse_x}, {mouse_y})")

    def add_object_id(self, name, obj_id):
        self.object_ids.update({name: obj_id})
        print(self.object_ids)

    def get_object_id(self, name):
        return self.object_ids.get(name)

    def run(self):

        self.root = ttk.Window()
        root = self.root
        root.title("LDO Resistor Calculator")
        root.geometry("600x480")
        root.minsize(640,480)
        root.maxsize(640,480)

        # 객체 ID를 저장할 리스트
        self.object_ids = {}

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
        image1 = self.resizeImage(rawImage, ratio=0.8)

        self.canvas = ttk.Canvas(frame1, width=image1.width(), height=image1.height(), relief="solid", bd=1, background="red")
        canvas = self.canvas
        # canvas.bind("<Motion>", on_mouse_move)
        canvas.bind("<Button-1>", self.leftClicked)

        canvas.pack(padx=0, pady=0)

        # 이미지 참조를 저장할 리스트
        canvas.image_store = []
        self.click_rectangle_coords = [
            {"name" :"Vin", "coord" : (105,68,135,95)},
            {"name" :"Vout", "coord" : (520,35,565,60)},
            {"name" :"R2", "coord" : (390,75,415,95)},
        ]

        canvas.create_image(image1.width()/2,image1.height()/2,image=image1)

        # canvas.create_polygon(229.0,38.0,247.0,38.0,226.0,62.0,243.0,64.0)
        self.create_fill_rectangle(canvas, (390,150,410,170), "white")

        for click_rectangle in self.click_rectangle_coords:
            self.create_transparent_rectangle(canvas, name=click_rectangle["name"], rect_coords=click_rectangle["coord"], color=(255,0,0), alpha=0.5)

        print(canvas.image_store)


        font = ("Arial", 12)
        # self.create_text(canvas, 10, 200, "Vin = 0.9V", color="red", font=font, anchor="w")
        self.create_only_text(canvas, 390, 140, "R1", color="black", font=font, anchor="w")
        self.create_only_text(canvas, 390, 160, "1.5㏀(Fixed)", color="black", font=font, anchor="w")

        # b1 = ttk.Button(root, text="Solid Button", bootstyle=SUCCESS)
        # b1.pack(side=LEFT, padx=5, pady=10)

        # b2 = ttk.Button(root, text="Outline Button", bootstyle=(SUCCESS, OUTLINE))
        # b2.pack(side=LEFT, padx=5, pady=10)
        # APP 실행
        root.mainloop()


if __name__ == "__main__":
    config = {"debug": True, "version": "1.0"}  # 설정 값
    app = Mainframe(config)
    app.run()