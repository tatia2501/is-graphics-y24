from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Func import *
from ColorSpaces import *
from Gamma import *
from Disering import *
from DrawingLine import *
from Histogram import *
from Filtering import *
from Scaling import *
from tkinter import filedialog
from PIL import Image, ImageTk


def show_buffer(buffer):
    global current_gamma
    pixels_to_show = to_new_gamma(buffer, current_gamma)
    image = Image.fromarray(pixels_to_show.astype('uint8'))
    img = ImageTk.PhotoImage(image)
    disp_img.config(image=img)
    disp_img.image = img

def show_picture():
    global files_name
    global start_label
    global pixels
    global pic_height
    global pic_width
    try:
        image = Image.open(files_name)
        pic_width = w = image.size[0]
        pic_height = h = image.size[1]
        img = ImageTk.PhotoImage(image.resize((w, h)))
        disp_img.config(image=img)
        disp_img.image = img
        disp_img.place(x=100, y=50)
        start_label.destroy()
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл не найден")
    except AttributeError:
        messagebox.showerror("Ошибка", "Файл не найден")
    except Exception:
        messagebox.showerror("Ошибка", "Неверный формат файла")


def save_png_picture():
    global files_name
    try:
        h, f, k = read(files_name)
        convert(f, files_name[:len(files_name) - 4] + "_new")
    except RuntimeError:
        messagebox.showerror("Ошибка", "Файл не найден")


def save_pnm_picture():
    global files_name
    global pixels
    try:
        f = pixels
        if (files_name == ""):
            files_name_new = "unnamed"
        else:
            files_name_new = files_name[:len(files_name) - 4] + "_new.pnm"
        write(files_name_new, f, 255)
    except RuntimeError:
        messagebox.showerror("Ошибка", "Файл не найден")


def save_as_picture(comboExample, new_files_name):
    global files_name
    global pixels
    try:
        h, f, k = read(files_name)
        p = ""
    except RuntimeError:
        k = 255
        p = "P5"

    try:
        f = pixels
        if (comboExample.get() == ".png"):
            if (new_files_name.get() == ""):
                save_png_picture()
            else:
                convert(f, new_files_name.get())
        if (comboExample.get() == ".pnm"):
            if (new_files_name.get() == ""):
                save_pnm_picture()
            else:
                write(new_files_name.get() + ".pnm", f, k, p)
    except RuntimeError:
        messagebox.showerror("Ошибка", "Файл не может быть создан")


def browse_files():
    global files_name
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(
                                          ("PNM files", "*.pnm*"), ("PPM files", "*.ppm*"), ("PGM files", "*.pgm*"),
                                          ("all files", "*.*")))
    files_name = filename


def on_closing():
    window.destroy()


def open():
    global pixels
    global pixels_backup
    global current_gamma
    global files_name
    global pixel_buffer
    current_gamma = 1
    browse_files()
    show_picture()
    pixels = read(files_name)[1]
    pixels_backup = pixels

    pixel_buffer = np.copy(pixels)

# def open_jpeg():
#     global pixels
#     global pixels_backup
#     global current_gamma
#     global files_name
#     global pixel_buffer
#     current_gamma = 1
#     browse_files()
#     # show_picture()
#     pixels = read(files_name)[1]
#     pixels_backup = np.copy(pixels)
#     pixel_buffer = np.copy(pixels)


def save_as():
    newWindow = Toplevel(window)
    newWindow.title("Сохранить как")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text="Название файла: ")
    labelTop.grid(row=1, column=1)
    new_files_name = Entry(
        newFrame,
    )
    new_files_name.grid(row=1, column=2)
    labelTop = Label(newFrame, text="Формат: ")
    labelTop.grid(row=1, column=3)
    comboExample = ttk.Combobox(newFrame, values=[".png", ".pnm"])
    comboExample.grid(row=1, column=4)
    save_as_btn = Button(
        newFrame,
        text='Cохранить',
        command=lambda: save_as_picture(comboExample, new_files_name)
    )
    save_as_btn.grid(row=1, column=5)


def clean_picture():
    global start_label
    global files_name
    disp_img.config(image='')
    disp_img.image = ''
    files_name = ""
    start_label = Label(frame, text="Для начала работы выберите изображение (Файл - Открыть)")
    start_label.grid(row=1, column=1)


def change_space(new_space):
    global pixels
    global current_space
    global current_gamma
    if new_space[0] != current_space[0]:
        if current_space[0] != "RGB":
            pixels = to_RGB(current_space[0], pixels)
            if new_space[0] != "RGB":
                pixels = from_RGB(new_space[0], pixels)
        else:
            pixels = from_RGB(new_space[0], pixels)
        current_space = new_space
    if current_space[0] != "RGB":
        pixels_backup = to_RGB(current_space[0], pixels)
    else:
        pixels_backup = pixels

    canals.delete(0, 3)
    canals.add_command(label=current_space[0], command=lambda: change_canal(0))
    canals.add_command(label=current_space[1], command=lambda: change_canal(1))
    canals.add_command(label=current_space[2], command=lambda: change_canal(2))
    canals.add_command(label=current_space[3], command=lambda: change_canal(3))

    show_buffer(pixels_backup)

def change_canal(index):
    global current_space
    global pixels
    global current_gamma
    if (index == 0):
        pixels_backup = pixels
    else:
        pixels_backup = np.zeros((len(pixels[0]), len(pixels[0]), 3), dtype="float32")
        for i in range(len(pixels)):
            for j in range(len(pixels[0])):
                for k in range(3):
                    if k + 1 == index:
                        pixels_backup[i, j][k] = pixels[i, j][k]

        if current_space[0] != "RGB":
            pixels_backup = to_RGB(current_space[0], pixels_backup)

    show_buffer(pixels_backup)

def assign_gamma(gamma):
    global pixels
    global current_gamma
    global pixels_buffer

    current_gamma = gamma
    show_buffer(pixels)


def convert_gamma(gamma):
    global pixels
    global current_gamma
    global pixels_backup

    pixels = to_new_gamma(pixels_backup, gamma)

    if gamma == 0:
        current_gamma = -1
    else:
        current_gamma = 1/gamma

    show_buffer(pixels)

def gamma_window():
    newWindow = Toplevel(window)
    newWindow.title("Задать гамму")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text="Гамма: ")
    labelTop.grid(row=1, column=1)
    new_gamma_1 = Entry(
        newFrame,
    )
    new_gamma_1.grid(row=1, column=2)
    save_as_btn_1 = Button(
        newFrame,
        text='назначить',
        command=lambda: assign_gamma(float(new_gamma_1.get()))
    )
    save_as_btn_1.grid(row=1, column=3)

    labelTop = Label(newFrame, text="Гамма: ")
    labelTop.grid(row=3, column=1)
    new_gamma = Entry(
        newFrame,
    )
    new_gamma.grid(row=3, column=2)
    save_as_btn = Button(
        newFrame,
        text='преобразовать',
        command=lambda: convert_gamma(float(new_gamma.get()))
    )
    save_as_btn.grid(row=3, column=3)


def onmouse(event):
    global px
    global py
    px.append(event.x)
    py.append(event.y)
    if (len(px) > 2):
        px.pop(0)
        px.pop(0)
        py.pop(0)
        py.pop(0)


def line_drawing(c1=0, c2=0, c3=0, visibility=1.0, thickness=1.0):
    global px
    global py
    global pixels
    global current_gamma

    pixels_backup = to_new_gamma(pixels, current_gamma)
    pixels_backup = drawing(px, py, pixels_backup, c1, c2, c3, visibility, thickness)
    if current_gamma == -1:
        pixels_backup = to_new_gamma(pixels_backup, 0)
    else:
        pixels_backup = to_new_gamma(pixels_backup, 1/current_gamma)

    if current_space[0] != "RGB":
        pixels_backup = to_RGB(current_space[0], pixels_backup)

    pixels = pixels_backup
    show_buffer(pixels)


def drawing_window():
    global current_space
    newWindow = Toplevel(window)
    newWindow.title("Нарисовать линию")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)
    null_var_1 = StringVar(newWindow, value="0")
    null_var_2 = StringVar(newWindow, value="0")
    null_var_3 = StringVar(newWindow, value="0")

    labelTop = Label(newFrame, text="Цветовые каналы: ")
    labelTop.grid(row=2, column=1)

    labelTop = Label(newFrame, text=current_space[1])
    labelTop.grid(row=2, column=2)

    canal1 = Entry(
        newFrame,
        textvariable=null_var_1
    )
    canal1.grid(row=2, column=3)

    labelTop = Label(newFrame, text=current_space[2])
    labelTop.grid(row=2, column=4)

    canal2 = Entry(
        newFrame,
        textvariable=null_var_2
    )
    canal2.grid(row=2, column=5)

    labelTop = Label(newFrame, text=current_space[3])
    labelTop.grid(row=2, column=6)

    canal3 = Entry(
        newFrame,
        textvariable=null_var_3
    )
    canal3.grid(row=2, column=7)

    trans = ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"]
    visibility_var = StringVar(value=trans[10])

    labelTop = Label(newFrame, text="Прозрачность: ")
    labelTop.grid(row=3, column=1)
    visibility = ttk.Combobox(newFrame,
                              textvariable=visibility_var,
                              values=trans)
    visibility.grid(row=3, column=3)

    thickness_arr = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    thickness = StringVar(value=thickness_arr[0])

    labelTop = Label(newFrame, text="Толщина: ")
    labelTop.grid(row=4, column=1)
    thickness_lbl = ttk.Combobox(newFrame,
                              textvariable=thickness,
                              values=thickness_arr)
    thickness_lbl.grid(row=4, column=3)

    labelTop = Label(newFrame, text="Выберете начало и конец линии")
    labelTop.grid(row=5, column=3)

    save_as_btn = Button(
        newFrame,
        text='нарисовать',
        command=lambda: line_drawing(int(canal1.get()), int(canal2.get()), int(canal3.get()),
                                     float(visibility_var.get()), float(thickness.get()))
    )
    save_as_btn.grid(row=7, column=1)

    disp_img.bind('<Button-1>', onmouse)
    disp_img.pack()

def generate_gradient(size_x, size_y):
    global start_label
    global pixels
    global pixels_backup
    global current_gamma
    current_gamma = 1
    pixels = gradient(size_x, size_y)
    pixels_backup = pixels
    start_label.destroy()
    show_buffer(pixels)

def generate_gradient_window():
    newWindow = Toplevel(window)
    newWindow.title("Сгенерировать градиент")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text="Размер: ")
    labelTop.grid(row=1, column=1)
    size_x = Entry(
        newFrame,
    )
    size_x.grid(row=1, column=2)
    sign = Label(newFrame, text="x")
    sign.grid(row=1, column=3)
    size_y = Entry(
        newFrame,
    )
    size_y.grid(row=1, column=4)

    create = Button(
        newFrame,
        text='создать',
        command=lambda: generate_gradient(int(size_x.get()), int(size_y.get()))
    )
    create.grid(row=1, column=5)

def floyd_steinberg_dithering(nc):
    global pixels
    pixels = floyd_steinberg(pixels, nc)
    show_buffer(pixels)

def ordered_dithering(nc):
    global pixels
    pixels = ordered(pixels, nc)
    show_buffer(pixels)

def random_dithering(nc):
    global pixels
    pixels = random_func(pixels, nc)
    show_buffer(pixels)

def atkinson_dithering(nc):
    global pixels
    pixels = atkinson(pixels, nc)
    show_buffer(pixels)

def cancel():
    global pixels
    global pixels_backup
    pixels = pixels_backup
    show_buffer(pixels)

def histogram(canal):
    global pixels
    global current_gamma

    if (canal == "все"):
        pixels_to_show_0 = show_histogram(pixels, 0)
        pixels_to_show_0 = to_new_gamma(pixels_to_show_0, current_gamma)
        pixels_to_show_1 = show_histogram(pixels, 1)
        pixels_to_show_1 = to_new_gamma(pixels_to_show_1, current_gamma)
        pixels_to_show_2 = show_histogram(pixels, 2)
        pixels_to_show_2 = to_new_gamma(pixels_to_show_2, current_gamma)

        hist_win_0 = Toplevel()
        hist_win_0.geometry('800x800')
        hist_win_0.title("Гистограмма по каналу 0")

        hist_win_1 = Toplevel()
        hist_win_1.geometry('800x800')
        hist_win_1.title("Гистограмма по каналу 1")

        hist_win_2 = Toplevel()
        hist_win_2.geometry('800x800')
        hist_win_2.title("Гистограмма по каналу 2")

        image_0 = Image.fromarray(pixels_to_show_0.astype('uint8'))
        hist_img_0 = ImageTk.PhotoImage(image_0.resize((image_0.size[0], 600)))
        label_0 = Label(hist_win_0, image=hist_img_0)
        label_0.image = hist_img_0
        label_0.grid(row=1, column=1)
        label_0.pack()

        image_1 = Image.fromarray(pixels_to_show_1.astype('uint8'))
        hist_img_1 = ImageTk.PhotoImage(image_1.resize((image_1.size[0], 600)))
        label_1 = Label(hist_win_1, image=hist_img_1)
        label_1.image = hist_img_1
        label_1.grid(row=1, column=2)
        label_1.pack()

        image_2 = Image.fromarray(pixels_to_show_2.astype('uint8'))
        hist_img_2 = ImageTk.PhotoImage(image_2.resize((image_2.size[0], 600)))
        label_2 = Label(hist_win_2, image=hist_img_2)
        label_2.image = hist_img_2
        label_2.grid(row=1, column=3)
        label_2.pack()
    else:
        hist_win = Toplevel()
        hist_win.geometry('800x800')
        hist_win.title("Гистограмма")

        pixels_to_show = show_histogram(pixels, int(canal))
        pixels_to_show = to_new_gamma(pixels_to_show, current_gamma)
        image = Image.fromarray(pixels_to_show.astype('uint8'))
        hist_img = ImageTk.PhotoImage(image.resize((image.size[0], 600)))
        label = Label(hist_win, image=hist_img)
        label.image = hist_img
        label.pack()

def autocorrection(coef):
    global pixels
    pixels = do_autocorrection(pixels, coef)
    show_buffer(pixels)

def histogram_window():
    newWindow = Toplevel(window)
    newWindow.title("Гистограммы")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)
    null_var_1 = StringVar(newWindow, value="0")

    trans = ["0", "1", "2", "все"]
    visibility_var = StringVar(value=trans[3])

    labelTop = Label(newFrame, text="Канал(ы): ")
    labelTop.grid(row=1, column=1)
    canals = ttk.Combobox(newFrame,
                              textvariable=visibility_var,
                              values=trans)
    canals.grid(row=1, column=2)

    show_as_btn = Button(
        newFrame,
        text='показать',
        command=lambda: histogram(canals.get())
    )
    show_as_btn.grid(row=2, column=2)

    labelTop = Label(newFrame, text="Автоматическая коррекция")
    labelTop.grid(row=3, column=2)

    labelTop = Label(newFrame, text="Доля игнорируемых пикселей: ")
    labelTop.grid(row=4, column=1)

    coef = Entry(
        newFrame,
        textvariable=null_var_1
    )
    coef.grid(row=4, column=2)

    show_as_btn = Button(
        newFrame,
        text='изменить',
        command=lambda: autocorrection(float(coef.get()))
    )
    show_as_btn.grid(row=5, column=2)

    disp_img.bind('<Button-1>', onmouse)
    disp_img.pack()

def threshold_filtering(coef):
    global pixels
    pixels = do_threshold_filtering(pixels, coef)
    show_buffer(pixels)

def threshold_filtering_window():
    newWindow = Toplevel(window)
    newWindow.title("Пороговая фильтрация")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text="Порог: ")
    labelTop.grid(row=1, column=1)

    param = Entry(
        newFrame,
    )
    param.grid(row=1, column=2)

    create = Button(
        newFrame,
        text='изменить',
        command=lambda: threshold_filtering(int(param.get()))
    )
    create.grid(row=1, column=3)

def ocu_filtering():
    global pixels
    pixels = do_ocu_filtering(pixels)
    show_buffer(pixels)

def median_filtering(coef):
    global pixels
    pixels = do_median_filtering(pixels, coef)
    show_buffer(pixels)

def median_filtering_window():
    newWindow = Toplevel(window)
    newWindow.title("Медианный фильтр")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text="Радиус ядра: ")
    labelTop.grid(row=1, column=1)

    param = Entry(
        newFrame,
    )
    param.grid(row=1, column=2)

    create = Button(
        newFrame,
        text='изменить',
        command=lambda: median_filtering(int(param.get()))
    )
    create.grid(row=1, column=3)

def gauss_filtering(coef):
    global pixels
    pixels = do_gauss_filtering(pixels, coef)
    show_buffer(pixels)

def gauss_filtering_window():
    newWindow = Toplevel(window)
    newWindow.title("Фильтр Гаусса")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text="Параметр: ")
    labelTop.grid(row=1, column=1)

    param = Entry(
        newFrame,
    )
    param.grid(row=1, column=2)

    create = Button(
        newFrame,
        text='изменить',
        command=lambda: gauss_filtering(float(param.get()))
    )
    create.grid(row=1, column=3)

def averaging_filtering(coef):
    global pixels
    pixels = do_averaging_filtering(pixels, coef)
    show_buffer(pixels)

def averaging_filtering_window():
    newWindow = Toplevel(window)
    newWindow.title("Линейный усредняющий фильтр (box blur)")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text="Радиус ядра: ")
    labelTop.grid(row=1, column=1)

    param = Entry(
        newFrame,
    )
    param.grid(row=1, column=2)

    create = Button(
        newFrame,
        text='изменить',
        command=lambda: averaging_filtering(int(param.get()))
    )
    create.grid(row=1, column=3)

def sobel_filtering():
    global pixels
    pixels = do_sobel_filtering(pixels)
    show_buffer(pixels)

def sharpening_filtering(coef):
    global pixels
    pixels = do_sharpening_filtering(pixels, coef)
    show_buffer(pixels)

def sharpening_filtering_window():
    newWindow = Toplevel(window)
    newWindow.title("Contrast Adaptive Sharpening")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text="Sharpness [0.0; 1.0]: ")
    labelTop.grid(row=1, column=1)

    param = Entry(
        newFrame,
    )
    param.grid(row=1, column=2)

    create = Button(
        newFrame,
        text='изменить',
        command=lambda: sharpening_filtering(float(param.get()))
    )
    create.grid(row=1, column=3)


def scaling_opt(size_x, size_y, cent_x, cent_y, method_var, param_b, param_c):
    global pixels
    global current_gamma
    global pic_height
    global pic_width
    pixels = scaling(size_x, size_y, method_var, param_b, param_c, pixels)
    pixels_to_show = to_new_gamma(pixels, current_gamma)
    image = Image.fromarray(pixels_to_show.astype('uint8'))
    w = image.size[0]
    h = image.size[1]
    img = ImageTk.PhotoImage(image)
    disp_img.config(image=img)
    disp_img.image = img
    prev_x = int(disp_img.place_info().get('x'))
    prev_y = int(disp_img.place_info().get('y'))
    disp_img.place(x=int(prev_x+cent_x+(pic_width/2)-(w/2)), y=int(prev_y+cent_y+(pic_height/2)-(h/2)))
    pic_height = h
    pic_width = w

def scaling_window():
    newWindow = Toplevel(window)
    newWindow.title("Масштабирование")
    newWindow.geometry('600x200')

    newFrame = Frame(
        newWindow,
        padx=5,
        pady=5
    )
    newFrame.pack(expand=True)

    labelTop = Label(newFrame, text="Размер: ")
    labelTop.grid(row=1, column=1)
    labelTop = Label(newFrame, text="x: ")
    labelTop.grid(row=1, column=2)
    size_x = Entry(
        newFrame,
    )
    size_x.grid(row=1, column=3)
    labelTop = Label(newFrame, text="y: ")
    labelTop.grid(row=1, column=4)
    size_y = Entry(
        newFrame,
    )
    size_y.grid(row=1, column=5)

    null_var_1 = StringVar(newWindow, value="0")
    null_var_2 = StringVar(newWindow, value="0")
    null_var_3 = StringVar(newWindow, value="0")
    null_var_4 = StringVar(newWindow, value="0.5")

    labelTop = Label(newFrame, text="Смещение центра: ")
    labelTop.grid(row=2, column=1)

    labelTop = Label(newFrame, text="x: ")
    labelTop.grid(row=2, column=2)

    cent_x = Entry(
        newFrame,
        textvariable=null_var_1
    )
    cent_x.grid(row=2, column=3)

    labelTop = Label(newFrame, text="y: ")
    labelTop.grid(row=2, column=4)

    cent_y = Entry(
        newFrame,
        textvariable=null_var_2
    )
    cent_y.grid(row=2, column=5)

    opt = ["ближайшая точка", "билинейное", "Lanczos3", "BC-сплайны"]
    method_var = StringVar(value=opt[3])

    labelTop = Label(newFrame, text="Способ: ")
    labelTop.grid(row=3, column=1)

    method = ttk.Combobox(newFrame,
                              textvariable=method_var,
                              values=opt)
    method.grid(row=3, column=3)

    labelTop = Label(newFrame, text="Параметры BC: ")
    labelTop.grid(row=4, column=1)

    labelTop = Label(newFrame, text="B: ")
    labelTop.grid(row=4, column=2)

    param_b = Entry(
        newFrame,
        textvariable=null_var_3
    )
    param_b.grid(row=4, column=3)

    labelTop = Label(newFrame, text="C: ")
    labelTop.grid(row=4, column=4)

    param_c = Entry(
        newFrame,
        textvariable=null_var_4
    )
    param_c.grid(row=4, column=5)

    create = Button(
        newFrame,
        text='масштабировать',
        command=lambda: scaling_opt(int(size_x.get()), int(size_y.get()), int(cent_x.get()),
                                int(cent_y.get()), method_var.get(), float(param_b.get()), float(param_c.get()))
    )
    create.grid(row=5, column=5)

window = Tk()
window.title('Графическое приложение')
window.geometry('900x700')
window.option_add("*tearOff", FALSE)
main_menu = Menu()
current_space = ["RGB", "R", "G", "B"]

file_menu = Menu()
file_menu.add_command(label="Открыть", command=open)
# file_menu.add_command(label="Открыть jpeg", command=open_jpeg)
file_menu.add_command(label="Сохранить как", command=save_as)
file_menu.add_cascade(label="Сгенерировать", command=generate_gradient_window)
file_menu.add_separator()
file_menu.add_command(label="Очистить", command=clean_picture)

color_spaces = Menu()
color_spaces.add_command(label="RGB", command=lambda: change_space(["RGB", "R", "G", "B"]))
color_spaces.add_command(label="HSL", command=lambda: change_space(["HSL", "H", "S", "L"]))
color_spaces.add_command(label="HSV", command=lambda: change_space(["HSV", "H", "S", "V"]))
color_spaces.add_command(label="YCbCr601", command=lambda: change_space(["YCbCr601", "Y", "Cb", "Cr"]))
color_spaces.add_command(label="YCbCr709", command=lambda: change_space(["YCbCr709", "Y", "Cb", "Cr"]))
color_spaces.add_command(label="YCoCg", command=lambda: change_space(["YCoCg", "Y", "Co", "Cg"]))
color_spaces.add_command(label="CMY", command=lambda: change_space(["CMY", "C", "M", "Y"]))

canals = Menu()
canals.add_command(label=current_space[0], command=lambda: change_canal(0))
canals.add_command(label=current_space[1], command=lambda: change_canal(1))
canals.add_command(label=current_space[2], command=lambda: change_canal(2))
canals.add_command(label=current_space[3], command=lambda: change_canal(3))

change_menu = Menu()
change_menu.add_cascade(label="Цветовое пространство", menu=color_spaces)
change_menu.add_cascade(label="Каналы", menu=canals)

bitness_floyd_steinberg = Menu()
bitness_floyd_steinberg.add_command(label="1", command=lambda: floyd_steinberg_dithering(1))
bitness_floyd_steinberg.add_command(label="2", command=lambda: floyd_steinberg_dithering(2))
bitness_floyd_steinberg.add_command(label="3", command=lambda: floyd_steinberg_dithering(3))
bitness_floyd_steinberg.add_command(label="4", command=lambda: floyd_steinberg_dithering(4))
bitness_floyd_steinberg.add_command(label="5", command=lambda: floyd_steinberg_dithering(5))
bitness_floyd_steinberg.add_command(label="6", command=lambda: floyd_steinberg_dithering(6))
bitness_floyd_steinberg.add_command(label="7", command=lambda: floyd_steinberg_dithering(7))
bitness_floyd_steinberg.add_command(label="8", command=lambda: floyd_steinberg_dithering(8))

bitness_ordered = Menu()
bitness_ordered.add_command(label="1", command=lambda: ordered_dithering(1))
bitness_ordered.add_command(label="2", command=lambda: ordered_dithering(2))
bitness_ordered.add_command(label="3", command=lambda: ordered_dithering(3))
bitness_ordered.add_command(label="4", command=lambda: ordered_dithering(4))
bitness_ordered.add_command(label="5", command=lambda: ordered_dithering(5))
bitness_ordered.add_command(label="6", command=lambda: ordered_dithering(6))
bitness_ordered.add_command(label="7", command=lambda: ordered_dithering(7))
bitness_ordered.add_command(label="8", command=lambda: ordered_dithering(8))

bitness_random = Menu()
bitness_random.add_command(label="1", command=lambda: random_dithering(1))
bitness_random.add_command(label="2", command=lambda: random_dithering(2))
bitness_random.add_command(label="3", command=lambda: random_dithering(3))
bitness_random.add_command(label="4", command=lambda: random_dithering(4))
bitness_random.add_command(label="5", command=lambda: random_dithering(5))
bitness_random.add_command(label="6", command=lambda: random_dithering(6))
bitness_random.add_command(label="7", command=lambda: random_dithering(7))
bitness_random.add_command(label="8", command=lambda: random_dithering(8))

bitness_atkinson = Menu()
bitness_atkinson.add_command(label="1", command=lambda: atkinson_dithering(1))
bitness_atkinson.add_command(label="2", command=lambda: atkinson_dithering(2))
bitness_atkinson.add_command(label="3", command=lambda: atkinson_dithering(3))
bitness_atkinson.add_command(label="4", command=lambda: atkinson_dithering(4))
bitness_atkinson.add_command(label="5", command=lambda: atkinson_dithering(5))
bitness_atkinson.add_command(label="6", command=lambda: atkinson_dithering(6))
bitness_atkinson.add_command(label="7", command=lambda: atkinson_dithering(7))
bitness_atkinson.add_command(label="8", command=lambda: atkinson_dithering(8))

disering = Menu()
disering.add_cascade(label="Ordered", menu=bitness_ordered)
disering.add_cascade(label="Random", menu=bitness_random)
disering.add_cascade(label="Floyd-Steinberg", menu=bitness_floyd_steinberg)
disering.add_cascade(label="Atkinson", menu=bitness_atkinson)

filtering_menu = Menu()
filtering_menu.add_cascade(label="Пороговая", command=threshold_filtering_window)
filtering_menu.add_cascade(label="Пороговая методом Оцу", command=ocu_filtering)
filtering_menu.add_cascade(label="Медианный фильтр", command=median_filtering_window)
filtering_menu.add_cascade(label="Фильтр Гаусса", command=gauss_filtering_window)
filtering_menu.add_cascade(label="Линейный усредняющий фильтр", command=averaging_filtering_window)
filtering_menu.add_cascade(label="Фильтр Собеля", command=sobel_filtering)
filtering_menu.add_cascade(label="Contrast Adaptive Sharpening", command=sharpening_filtering_window)

main_menu.add_cascade(label="Файл", menu=file_menu)
main_menu.add_cascade(label="Изменить", menu=change_menu)
main_menu.add_cascade(label="Гамма", command=gamma_window)
main_menu.add_cascade(label="Рисовать", command=drawing_window)
main_menu.add_cascade(label="Дизеринг", menu=disering)
main_menu.add_cascade(label="Гистограмма", command=histogram_window)
main_menu.add_cascade(label="Фильтрация", menu=filtering_menu)
main_menu.add_cascade(label="Масштабирование", command=scaling_window)
main_menu.add_cascade(label="Отменить", command=cancel)

frame = Frame(
    window,
    padx=10,
    pady=10
)
frame.pack(expand=True)

files_name = ""

px = []
py = []

start_label = Label(frame, text="Для начала работы выберите изображение (Файл - Открыть)")
start_label.grid(row=1, column=1)

disp_img = Label()
disp_img.pack()

window.config(menu=main_menu)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
