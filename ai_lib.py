import cv2
import easyocr
import numpy as np
from PIL import Image
import base64
import io

import vertexai
from vertexai.language_models import TextGenerationModel

def data_url_to_cv2(data_url):
    # Extract the base64 encoded image data from the data URL
    image_data = data_url.split(',')[1]

    # Decode the base64 encoded image data
    decoded_image_data = base64.b64decode(image_data)

    # Convert the decoded image data to a numpy array
    nparr = np.frombuffer(decoded_image_data, np.uint8)

    # Read the image using cv2.imread
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return image

def crop_face_from_id(img):
    id_img = data_url_to_cv2(img)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    scale_percent = 60  # percent of original size
    width = int(id_img.shape[1] * scale_percent / 100)
    height = int(id_img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    image = cv2.resize(id_img, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # face classifier
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    # When no faces detected, face_classifier returns and empty tuple
    if faces is ():
        return None

    else:

        ct = 0
        for (x, y, width, height) in faces:
            if len(faces) == ct + 1:
                y -= 25
                height += 25
                roi = image[y:y + height, x:x + width]
                return roi

            ct += 1


def id_img_to_text(image):
    """
    Transforms image to text.
    @image: numpy array
    """
    reader = easyocr.Reader(['ro'])
    generated_text = reader.readtext(image, detail=0)
    return resulting_text_array_to_text(generated_text)


def image_path_to_np_array(image_path):
    image = Image.open(image_path).convert("RGB")
    return np.array(image)


def resulting_text_array_to_text(text_array):
    text = ""

    for line in text_array:
        text = text + line + "\n"

    return text

def request_json_from_id_text(input_text):

    vertexai.init(project="hacathon-405514", location="europe-west9")
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        """
        I will be giving you a text in tripple quotes, resembling the the ocr scan of a romanian id. 
        I want you to extract the data from it in the following JSON format. 
        I included a little description for how the data may look like for each field:
    {
        \"cnp\" : \"Form: 13 digit number\", 
        \"series\" : , \"Form: 2 Characters\"
        \"number\" : , \"Form: 6 digit number\"
        \"name\" : , \"Form: all caps, indefiinite number of characters, no numbers\"
        \"surname\" : , \"Form: all caps, indefiinite number of characters, no numbers\"
        \"citizenship\" : \"Form: Română\" (most likely answer, other answers may be here), 
        \"place_of_birth\" : \"Form: Jud.XX Munn.[indefinite number of characters, no numbers]. Hint: you cand find it most likely below line \'Loc nastere/Lieu de naissance/Place of birth\' \"
        \"adress\" : \"Hint:figure it out, but it must contain the whole adress with street, municipality and county\",
        \"authority\" : \"Hint:figure it out\", 
        \"date issued\" : \"Hint:is a date, figure out which\",
        \"valid_until\" : \"Hint:is a date, figure out which\",
        \"sex\" : \"Form:M or F\"
    }
    You will be responding with just the resulting json, that means just the json brackets and the json file contents, no quotation marks and no extra text except the json file.
    This is the ocr text: \'\'\' """ + input_text + """"\'\'\'""", **parameters
    )

    return response.text

def data_url_to_np_array(data_url):
    # Remove the data URL prefix
    encoded_image = data_url.split(",")[1]

    # Decode the base64-encoded image data
    decoded_image = base64.b64decode(encoded_image)

    # Open the image using PIL
    image = Image.open(io.BytesIO(decoded_image))

    # Convert the image to a NumPy array
    np_array = np.array(image)

    return np_array

def photo_to_json(data_url):
    return request_json_from_id_text(id_img_to_text(data_url_to_np_array(data_url)))



