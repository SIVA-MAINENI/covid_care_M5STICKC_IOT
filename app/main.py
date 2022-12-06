import flask
from flask import Flask, jsonify, request, send_from_directory
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

app = flask.Flask(__name__)
app.app_context().push()
app.config["DEBUG"] = True

def check_image(image_url):
    """
    checks whether the person
    is wearing mask or not
    """
    credential = {
    "API_KEY": "3e399461a9cb43bfaa223c55752c98a4",
    "END_POINT": "https://doverhackathon2022-computervisionapi.cognitiveservices.azure.com/"
    }
    api_key = credential['API_KEY']
    endpoint = credential['END_POINT']
    language = "en"
    max_descriptions = 20
    cv_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(api_key))
    result = cv_client.describe_image(image_url, max_descriptions, language)
    mask_present = False
    if len(result.captions) > 0:
        for caption in result.captions:
            if 'wearing' in caption.text and 'mask' in caption.text:
                mask_present = True
                break
    return mask_present


@app.route('/', methods=['GET'])
def home():
    return '''<h1>This is an Flask app </h1>
<p>Created for the IOT FInal project.</p>'''


@app.route('/api/check_image', methods=['POST', 'GET'])
def api_img_check():
    data = request.get_json()
    if check_image(data['image_url']):
        flag = {'flag': 'Yes' }
    else:
        flag = {'flag': 'No'}
    return jsonify(flag)

@app.route('/api/check_image_v2/<string:file>/', methods=['GET'])
def api_img_check_v2(file):
    print(type(file))
    image_url = 'https://raw.githubusercontent.com/SIVA-MAINENI/covid_care_M5STICKC_IOT/master/pictures/' + str(file)
    if check_image(image_url):
        flag = {'flag': 'Yes' }
    else:
        flag = {'flag': 'No'}
    return jsonify(flag)



if __name__ == "__main__":
    app.run(debug=True)