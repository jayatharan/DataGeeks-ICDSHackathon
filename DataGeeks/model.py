import os
from google.cloud import vision
import io


class InvoiceTotalFinder:

    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'credential.json'

    def convert_img(self, path):
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

        self.words_list = words_list

    def get_total(self):
        lines = []
        for i, v in enumerate(self.words_list[1:]):
            if((v[0].lower()).find("total") != -1):
                avr = (v[1][0][1]+v[1][3][1])/2
                line = []
                for c in self.words_list[1:]:
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
        return ttl
