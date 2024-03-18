from io import BytesIO

from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont

import os

import config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.API_FILE


def detect_labels(content: bytes):
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    labels_str = 'Labels: ' + ', '.join(label.description for label in labels)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return labels_str


def localize_objects(content: bytes):
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)
    objects = client.object_localization(image=image).localized_object_annotations

    image_bytes = BytesIO(content)
    pil_image = Image.open(image_bytes)
    draw = ImageDraw.Draw(pil_image)

    font = ImageFont.load_default(size=10)

    for object_ in objects: 
        vertices = [(vertex.x * pil_image.width, vertex.y * pil_image.height) for vertex in
                    object_.bounding_poly.normalized_vertices]
        draw.polygon(vertices, outline="red")

        text_x, text_y = vertices[0]

        name_text = f"{object_.name}"
        percentage_text = f"{object_.score * 100:.2f}%"
        label_text = f"{name_text} ({percentage_text})"

        draw.text((text_x, text_y), label_text, font=font, fill="red")

    image_bytes = BytesIO()
    pil_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    return image_bytes

