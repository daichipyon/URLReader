import requests
import re
import settings

KEY_ms = settings.KEY_ms

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
            matchOB = re.match(r"http" , line_text)
            if matchOB:
                start_index = matchOB.start() 
                line_text_modified = line_text[start_index:]
                text_li.append(line_text_modified)
    print(text_li)
    return_text = "\n".join(text_li)
    return(return_text)

if __name__ == "__main__":
    image_url = "https://lh3.googleusercontent.com/UWZ8RwvggpAlqDgTnITi8U1TRJ2l91jtWE6g-mSlY-Yk64xsDO2XLdAVP7UfYRsmOCRQv_iEpAioM7a4ybaRhpxR-GJbRPcYLywb6B363mTGLLIyomUW76vTVd5tbeCA9ZsddkKl6BY=w704-h939-no"
    print(get_url_from_text(image_url))