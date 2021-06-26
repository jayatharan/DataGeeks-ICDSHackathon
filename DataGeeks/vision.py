import os
import cv2
import pytesseract
from google.cloud import vision
import io
import pickle

# set envirnment varioble for Google Vision API credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'credential.json'


# Extract Text from image(GOOGLE OCR API)
def get_text(path):
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

    return words_list


# Import all image files
entries = os.listdir('./data/img')

# Get image datas from google api
image_texts = []
for entry in entries:
    texts = get_text("./data/img/"+entry)
    image_texts.append(texts)


a = {"img_name": entries, "img_datas": image_texts}

with open('filename.pickle', 'wb') as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)

print(a == b)
