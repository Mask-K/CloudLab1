import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "imagedescr-e6e0072f3f5c.json"


def detect_labels(content: bytes):
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print("Labels:")

    for label in labels:
        print(label.description)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )