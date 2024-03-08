from apiCalls import detect_labels


with open("img5.jpeg", "rb") as image_file:
    print(detect_labels(image_file.read()))


