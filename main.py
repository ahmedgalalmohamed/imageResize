from os import execl
from sys import executable
import PySimpleGUI as sg
from PIL import Image
from PySimpleGUI import WINDOW_CLOSED
from subprocess import Popen

try:
    file = open("color.txt", "r")
    color = str(file.read())
    sg.theme(color)
    file.close()
except FileNotFoundError:
    color = "Black"
    sg.theme(color)

path_des = []
Button_resize = sg.Button("Resize", key="btn_resize")
Button_cancel = sg.Button("Cancel", key="btn_cancel")
txt_lab_w = sg.Text("Width")
txt_lab_h = sg.Text("Height")
txt_in_w = sg.Input(key="txt_width", size=10)
txt_in_h = sg.Input(key="txt_height", size=10)
list_box_img = sg.Listbox([], size=(50, 20), enable_events=True, horizontal_scroll=True, key="li_box_img")
list_des_img = sg.Listbox([], size=(50, 20), enable_events=True, horizontal_scroll=True, key="li_des_img")
list_box_theme = sg.Combo(sg.theme_list(), readonly=True, enable_events=True, key="li_box_theme", default_value=color)
txt_sr_image = sg.Input(key="txt_sr_image", enable_events=True, visible=False)

layout_ = [
    [sg.T("Select Themes"), list_box_theme],
    [sg.Text("Choose Images: "), txt_sr_image,
     sg.FilesBrowse(key="btn_fi_browse", file_types=[("ALL Files", "*.jfif;*.jpg;*.png")])],
    [sg.Text("Choose Destination: "), sg.Input(key="txt_des_image", visible=False, enable_events=True),
     sg.FolderBrowse(key="btn_fo_browse")],
    [txt_lab_h, txt_in_h, txt_lab_w, txt_in_w], [Button_resize, Button_cancel], [list_box_img, list_des_img]]

windows = sg.Window(title="Resize Image", layout=layout_)


def resize_image(img_old_path, img_new_path, w, h):
    image = Image.open(img_old_path)
    filepath = img_old_path.split('/')
    filepath = filepath[len(filepath) - 1].split('.')
    name_img = str(filepath[0])
    type_img = str(filepath[1])
    path = img_new_path[0] + "/" + name_img + "." + type_img
    image = image.resize((w, h))
    image.save(path)


def val_ele(key):
    return windows.find_element(key).get()


def ret_ele(key):
    return windows.find_element(key)


def chk_empty_h_w():
    if val_ele("txt_height").isdigit() and val_ele("txt_width").isdigit():
        h = int(values["txt_height"])
        w = int(values["txt_width"])
    elif val_ele("txt_height") == '' and val_ele("txt_width") == '':
        h = 400
        w = 400
        sg.popup("this is Default w =400 h =400 for image")
    else:
        return 0
    return w, h


def chk_empty_sr_img():
    if val_ele("txt_sr_image") in ('', None):
        return 0


def chk_empty_des_img():
    if val_ele("txt_des_image") in ('', None):
        return 0


while True:
    event, values = windows.read()
    txt_sr_image = val_ele("txt_sr_image")
    if event == "btn_resize":
        if chk_empty_sr_img() == 0:
            sg.popup("Choose Images please", "Info")
        elif chk_empty_des_img() == 0:
            sg.popup("Choose Destination", "Info")
        else:
            if chk_empty_h_w() == 0:
                sg.popup("Error input")
            else:
                width, height = chk_empty_h_w()
                images_path = txt_sr_image.split(';')
                for img_path in images_path:
                    resize_image(img_path, path_des, width, height)
                ret_ele("txt_sr_image").update(value='')
                ret_ele("li_box_img").update([])
                ret_ele("li_des_img").update([])
                sg.popup_notify("Process Success...", "Info", display_duration_in_ms=500)
    elif event == "txt_sr_image":
        ret_ele("li_box_img").update(txt_sr_image.split(';'))
    elif event == "li_box_theme":
        file = open("color.txt", "w")
        file.write(list_box_theme.get())
        file.close()
        execl(executable, "python", __file__)
    elif event == WINDOW_CLOSED or event == "btn_cancel":
        windows.close()
        break
    elif event == "li_box_img":
        if len(txt_sr_image) > 0:
            image = Image.open(val_ele("li_box_img")[0])
            image.show()
    elif event == "txt_des_image":
        path_des = [val_ele("txt_des_image")]
        ret_ele("li_des_img").update(path_des)
    elif event == "li_des_img":
        if len(path_des) > 0:
            path = 'explorer "' + path_des[0] + '"'
            path = path.replace("/", "\\")
            Popen(path)
