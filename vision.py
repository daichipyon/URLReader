import requests
import re
import settings

KEY_ms = settings.KEY_ms

def get_url_from_text(image_url=None, image=None):
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

    ocr_url = vision_base_url + "ocr"

    # Set image_url to the URL of an image that you want to analyze.
    if image_url:
        headers = {'Ocp-Apim-Subscription-Key': KEY_ms}
        params  = {'language': 'en', 'detectOrientation': 'true'}
        data    = {'url': image_url}
        response = requests.post(ocr_url, headers=headers, params=params, json=data)
        response.raise_for_status()

        data = response.json()
    elif image:
        headers = {'Ocp-Apim-Subscription-Key': KEY_ms}
        params  = {'language': 'en', 'detectOrientation': 'true'}
        response = requests.post(ocr_url, headers=headers, params=params, json=image)
        response.raise_for_status()
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

    return_text = "\n".join(text_li)
    return(return_text)

if __name__ == "__main__":
    image_url = "https://lh3.googleusercontent.com/YJbHjXluaLekcInMdg37L7hlScCmdO7OVzlZn8jaq0U2givLhKneOj29xw1Y6g4AedsuLr4I7lRs3QpfMBOslFlEgKuOR5X1PUAHqpnCDcOmEkMCunsedlMPRaDA3MOLQx4acwwiYK5qiEr7ye4Gfd7VBGmRGbSSKipljqR4T09kBJo0rHwxuABM8FXUYANmHc8xCUEypBNY4THOGLV0h3wyZPzqTlUpAf-13w2qw0daQIeqSmPK8ZDt-fNzIjylW70-_gBPAn1_ebt6QtYRYep0gR_gTcEuZK8yPzwj3Nn4JnyLt1jS_e4OXD3vj-5womIsqx6TRTunVEILg2oKjMsOzPAeBdr2oAiiSSXp41MF4aI-aKSEFdvfVf72P0dc-l_Qo9Y-f5YvrKg62Js4Cdxl8_kyKGh1h7OnEHVR4-KMx8QFpZjSI7ZKsEEAdvEZz-w1H_JanJwzORdfIEJ0MChbUG-TpXHm6ffxUf-tVmu-Ux9bpD0S60LYykfvsrOG9geHmoUiqpTFyI7Us_f0K4dqJffBXxcw79wOX-7Z9a-QsPp7Jf2Yw9y_ogphdj2EzckgmtKTsS2-KOEIjK__rklZnXxcLpmp-EUe6bNpgjKJVH54I6VrO9mUDbOfFkPN=w704-h939-no"
    subscription_key = "b66cd9efe0a5414fb8d8877a6b39816c"
    print(get_url_from_text(image_url, subscription_key))