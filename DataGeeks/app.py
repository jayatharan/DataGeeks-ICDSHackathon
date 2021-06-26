from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import os
from google.cloud import vision
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'credential.json'

root = Tk()
root.geometry("400x400")
root.title("Invoice Text Extraction")

images = []
image_datas = []
total_datas = []


def getFolderPath():
    text_area.delete(0.1, END)
    text_area.insert(1.0, "File Name\t\tTotal")
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)
    get_images(folderPath.get())


def single_img():
    text_area.delete(0.1, END)
    text_area.insert(1.0, "File Name\t\tTotal")
    file_selected = filedialog.askopenfilenames()
    length = len(file_selected[0])
    img = ""
    folder = ""
    for i in range(length):
        if(file_selected[0][length-i-1] == "/"):
            img = file_selected[0][length-i:]
            folder = file_selected[0][:length-i-1]
            break
    convert_image(folder, img)


def get_images(file_path):
    global images
    images = sorted(os.listdir(file_path))
    get_image_datas()


def get_image_datas():
    global image_datas
    if(len(images) <= 0):
        return
    else:
        for img in images:
            data = convert_image(folderPath.get(), img)
            image_datas.append((img, data))


def convert_image(folder, img):
    path = folder+"/"+img
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    words_list = []

    for text in texts:
        vertises = []

        for vertex in text.bounding_poly.vertices:
            vertises.append((vertex.x, vertex.y))

        words_list.append((text.description, vertises))

    get_total(img, words_list)
    return words_list


def get_total(img, img_data):
    global total_datas
    lines = []
    for i, v in enumerate(img_data[1:]):
        if((v[0].lower()).find("total") != -1):
            avr = (v[1][0][1]+v[1][3][1])/2
            line = []
            for c in img_data[1:]:
                if((c[1][0][1] < int(avr) and c[1][3][1]) > int(avr)):
                    line.append((c[0], c[1][0][0]))
            lines.append(line)

    ttl = 0.00
    for i in lines:
        for l in i:
            if(l[0].find(".") != -1):
                price = ""
                for t in l[0]:
                    if t in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
                        price = price+t
                try:
                    p = float(price)
                    if (p > ttl):
                        ttl = p
                except:
                    pass
    text_area.insert(END, "\n"+img+"\t\t"+str(ttl))


folderPath = StringVar()

b_1 = Button(text="Open Folder", command=getFolderPath)
b_1.pack()


b_2 = Button(root, text="Single_IMG", command=single_img)
b_2.pack()


text_area = scrolledtext.ScrolledText(root,
                                      wrap=WORD,
                                      width=40,
                                      height=15,
                                      font=("Times New Roman",
                                            15))
text_area.pack()

root.mainloop()
