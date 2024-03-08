import os

import config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.API_FILE


def detect_labels(content: bytes):
    from google.cloud import vision

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
