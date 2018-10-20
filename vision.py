import requests
import re
import settings
import json
import base64
import urllib.request

KEY_ms = settings.KEY_ms
KEY_gg = settings.KEY_gg
"""
def get_url_from_text(image_url=None, image=None):
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"

    ocr_url = vision_base_url + "ocr"

    if image_url:
        headers = {'Ocp-Apim-Subscription-Key': KEY_ms, 'Content-Type': 'application/json'}
        params  = {'language': 'en', 'detectOrientation': 'true'}
        data    = {'url': image_url}
        response = requests.post(ocr_url, headers=headers, params=params, json=data)
        response.raise_for_status()

        data = response.json()
        print(data)
    elif image is not None:
        headers = {'Ocp-Apim-Subscription-Key': KEY_ms, "Content-Type": "application/octet-stream"}
        params  = {'language': 'en', 'detectOrientation': 'true'}
        response = requests.post(ocr_url, headers=headers, params=params, data=image)
        data = response.json()        
    else:
        return("Nothing has been sended.")

    text_li = []
    # Extract the word bounding boxes and text.
    for region in data['regions']:
        for line in region['lines']:
            line_text = ''
            for word in line['words']:
                line_text += word.get('text', '')
                line_text
            matchOB = re.search(r"http" , line_text)
            if matchOB:
                start_index = matchOB.start() 
                line_text_modified = line_text[start_index:]
                text_li.append(line_text_modified)
    return_text = "\n\n".join(text_li)
    return(return_text)
"""
def get_url_from_text_gg(image_url=None, image=None):
    GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate'
    if image_url:
        api_url = GOOGLE_CLOUD_VISION_API_URL 
        req_body = {
                'image': {'source':{
                    'imageUri': image_url
                }},
                'features': [{
                    'type': 'DOCUMENT_TEXT_DETECTION'
                }],
                'imageContext':{
                    'languageHints': "en"
                }
            }
        res = requests.post(api_url, data=json.dumps({"requests":req_body}),
                                params={'key': KEY_gg},
                                headers={'Content-Type': 'application/json'})
        text = res.json()["responses"][0]["fullTextAnnotation"]["text"]
        text_li = text.split("\n")
        return_li = []
        for text in text_li:
            matchOB = re.search(r"http" , text)
            if matchOB:
                start_index = matchOB.start() 
                line_text_modified = text[start_index:]
                return_li.append(line_text_modified)
        return_text = "\n\n".join(return_li)
        return return_text
        
    elif image:
        img = base64.b64encode(image)
        api_url = GOOGLE_CLOUD_VISION_API_URL 
        req_body = {
                'image': {'content': base64.b64encode(img).decode()},
                'features': [{
                    'type': 'DOCUMENT_TEXT_DETECTION'
                }],
                'imageContext':{
                    'languageHints': "en"
                }
            }
        res = requests.post(api_url, data=json.dumps({"requests":req_body}).encode(),
                                params={'key': KEY_gg},
                                headers={'Content-Type': 'application/json'})
        text = res.json()["responses"][0]["fullTextAnnotation"]["text"]
        text_li = text.split("\n")
        return_li = []
        for text in text_li:
            matchOB = re.search(r"http" , text)
            if matchOB:
                start_index = matchOB.start() 
                line_text_modified = text[start_index:]
                return_li.append(line_text_modified)
        return_text = "\n\n".join(return_li)
        return return_text

if __name__ == "__main__":
    image_url = "https://lh3.googleusercontent.com/UWZ8RwvggpAlqDgTnITi8U1TRJ2l91jtWE6g-mSlY-Yk64xsDO2XLdAVP7UfYRsmOCRQv_iEpAioM7a4ybaRhpxR-GJbRPcYLywb6B363mTGLLIyomUW76vTVd5tbeCA9ZsddkKl6BY=w704-h939-no"
    print(get_url_from_text_gg(image_url))