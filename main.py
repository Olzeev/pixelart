import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

root = tk.Tk()  # создаем корневой объект - окно
im_canvas = tk.Canvas(bg="white", width=850, height=700)
im_canvas.place(x=400, y=10)
root.title("Pixel art generator")  # устамнавливаем заголовок окна
root.geometry("1280x720")  # устанавливае размеры окна

icon = ImageTk.PhotoImage(Image.open('icon.jpg').resize((20, 20)))
root.iconphoto(False, icon)

image = None
image_label = None

errmsg = None

table = []
total_colors = []
table_colors = []

colors_num = tk.IntVar(value=15)
table_size_x = 70
table_size_y = 70
tile_size_x = 0
tile_size_y = 0

cursor_color = None


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def mouse_button_pressed(event):
    global table_colors, tile_size_y, tile_size_x, cursor_color, im_canvas
    if tile_size_x == 0:
        return
    x, y = event.x, event.y

    if table_colors[x // tile_size_x][y // tile_size_y] is not None:
        im_canvas.delete(table_colors[x // tile_size_x][y // tile_size_y])
        table_colors[x // tile_size_x][y // tile_size_y] = None
    elif cursor_color is not None:
        table_colors[x // tile_size_x][y // tile_size_y] = im_canvas.create_rectangle(
            x // tile_size_x * tile_size_x, y // tile_size_y * tile_size_y,
            x // tile_size_x * tile_size_x + tile_size_x, y // tile_size_y * tile_size_y + tile_size_y,
            fill=rgb_to_hex(cursor_color[0], cursor_color[1], cursor_color[2]))


def find(r, g, b, colors):
    L = 1
    R = len(colors)
    while R - L > 1:
        m = (R + L) // 2
        if colors[m].value[0] > r:
            R = m
        elif colors[m].value[0] < r:
            L = m
        else:
            if colors[m].value[1] > g:
                R = m
            elif colors[m].value[1] < g:
                L = m
            else:
                if colors[m].value[2] > b:
                    R = m
                else:
                    L = m
    return R


def convert_image_to_pixel(image):
    global table, colors_num, total_colors, table_sizey_entry, table_sizex_entry, im_canvas, tile_size_x, tile_size_y, table_colors

    table_size_x = int(table_sizex_entry.get())
    table_size_y = int(table_sizey_entry.get())
    table = [[0 for i in range(table_size_y)] for j in range(table_size_x)]
    table_colors = [[None for i in range(table_size_y)] for j in range(table_size_x)]

    colors_num1 = colors_num.get()

    pix = image.load()
    sizex, sizey = image.size
    colors = []
    for x in range(sizex):
        for y in range(sizey):
            colors.append(pix[x, y])
    colors.sort()
    cnt_x = 0

    for i in range(0, len(colors), len(colors) // colors_num1):
        if cnt_x + 1 > colors_num1:
            break
        r, g, b = 0, 0, 0
        cnt = 0
        for j in range(len(colors) // colors_num1):
            cnt += 1
            r += colors[i + j][0]
            g += colors[i + j][1]
            b += colors[i + j][2]
        total_colors.append(Color((r // cnt, g // cnt, b // cnt), cnt_x + 1, 5 + cnt_x * 35 % 330, 10 + cnt_x * 35 // 330 * 50, 30, 30))
        total_colors[-1].create()
        cnt_x += 1

    x1 = 0
    y1 = 0
    tile_size_x = im_canvas.winfo_width() // table_size_x
    tile_size_y = im_canvas.winfo_height() // table_size_y

    for x in range(0, sizex, sizex // table_size_x):
        for y in range(0, sizey, sizey // table_size_y):
            if x1 >= table_size_x or y1 >= table_size_y:
                break
            r, g, b = 0, 0, 0
            cnt = 0
            for deltax in range(sizex // table_size_x):
                for deltay in range(sizey // table_size_y):
                    if x + deltax >= sizex or y + deltay >= sizey:
                        break
                    r += pix[x + deltax, y + deltay][0]
                    g += pix[x + deltax, y + deltay][1]
                    b += pix[x + deltax, y + deltay][2]
                    cnt += 1
            r //= cnt
            g //= cnt
            b //= cnt

            table[x1][y1] = find(r, g, b, total_colors)
            '''
            table_colors[x1][y1] = im_canvas.create_rectangle(
                x1 * tile_size_x, y1 * tile_size_y,
                x1 * tile_size_x + tile_size_x, y1 * tile_size_y + tile_size_y,
                fill=rgb_to_hex(r, g, b))
            '''

            y1 += 1
        y1 = 0
        x1 += 1

    for x in range(len(table)):
        for y in range(len(table[0])):
            im_canvas.create_rectangle(x * tile_size_x, y * tile_size_y, x * tile_size_x + tile_size_x, y * tile_size_y + tile_size_y,
                                       fill="white", outline="black")
            im_canvas.create_text(x * tile_size_x + tile_size_x / 2, y * tile_size_y + tile_size_y / 2,
                                  text=str(table[x][y]))


def im_open():
    global im_entry
    name = filedialog.askopenfilename()
    im_entry.insert(0, name)


def image_set():
    global im_entry, image, errmsg, total_colors, table, im_canvas, cursor_color
    try:
        image1 = Image.open(im_entry.get())

        total_colors = []
        table = []
        im_canvas.delete("all")
        cursor_color = None

        image = image1

        convert_image_to_pixel(image)
        if errmsg is not None:
            errmsg.destroy()
            errmsg = None

    except:
        errmsg = ttk.Label(text='Не удалось открыть изображение!', foreground="#FF0000")
        errmsg.place(x=im_entry_x, y=im_entry_y + im_entry_height * 2 + 10, width=200, height=20)


def change(newVal):
    float_value = float(newVal)     # получаем из строки значение float
    int_value = round(float_value)  # округляем до целочисленного значения
    colors_num_label["text"] = f"Количество цветов: {int_value}"


class Color:
    def __init__(self, value, num, x, y, sizex, sizey):
        self.value = value
        self.num = num
        self.x, self.y = x, y
        self.sizex, self.sizey = sizex, sizey

    def check(self):
        global cursor_color
        cursor_color = self.value

    def create(self):
        button = tk.Button(text=str(self.num), command=self.check, background=rgb_to_hex(self.value[0], self.value[1], self.value[2]))
        button.place(x=self.x, y=220+self.y,
                               width=self.sizex, height=self.sizey)


im_entry_width = 300
im_entry_height = 20
im_entry_x = 10
im_entry_y = 10

im_entry = ttk.Entry()
im_entry.place(x=im_entry_x, y=im_entry_y, width=im_entry_width)

image_open_button = tk.Button(text='...', command=im_open)
image_open_button.place(x=im_entry_x+im_entry_width, y=im_entry_y + 1,
                        width=30, height=im_entry_height)

image_set_button = tk.Button(text='Открыть картинку', command=image_set)
image_set_button.place(x=im_entry_x, y=im_entry_y + im_entry_height + 5,
                        width=120, height=im_entry_height)


colors_num_scale = ttk.Scale(orient=tk.HORIZONTAL, length=100, from_=5, to=20, value=15,
                             variable=colors_num,
                             command=change)
colors_num_scale.place(x=im_entry_x, y=im_entry_y + im_entry_height * 3 + 15)

colors_num_label = ttk.Label(text=f'Количество цветов: 15')
colors_num_label.place(x=im_entry_x, y=im_entry_y + im_entry_height * 4 + 20, width=200, height=20)

table_sizex_label = ttk.Label(text='Ширина:')
table_sizex_label.place(x=im_entry_x, y=im_entry_y + im_entry_height * 6 + 30, width=200, height=20)

table_sizey_label = ttk.Label(text='Высота:')
table_sizey_label.place(x=im_entry_x + 200, y=im_entry_y + im_entry_height * 6 + 30, width=180, height=20)

table_sizex_entry = ttk.Entry()
table_sizex_entry.insert(0, '70')
table_sizex_entry.place(x=im_entry_x + 55, y=im_entry_y + im_entry_height * 6 + 30, width=80)

table_sizey_entry = ttk.Entry()
table_sizey_entry.insert(0, '70')
table_sizey_entry.place(x=im_entry_x + 255, y=im_entry_y + im_entry_height * 6 + 30, width=80)

im_canvas.bind("<Button-1>", mouse_button_pressed)

root.mainloop()
