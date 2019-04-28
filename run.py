#!/usr/bin/python
from flask import Flask, request, jsonify, make_response

from background_remover import remove

from base64 import b64decode, b64encode, decode

app = Flask(__name__)
path_to_save = "/home/vlad/changer_server/pictures/received/"
path_to_send = "/home/vlad/changer_server/pictures/send/"

@app.route("/", methods=['POST'])
def main():
    if request.method == 'POST':
        # get image from the android app
        content = request.get_json()
        string_image = content['image']
        name_image = content['name']
        # save image on the server
        file1 = open(path_to_save + name_image, "wb")
        file1.write(b64decode(string_image))
        file1.close()
        # remove background
        remove.run(name_image)
        # read image with removed background
        name_image = name_image[:len(name_image) - 4] + '.png'
        file2 = open(path_to_send + name_image, "rb")
        # parse to string
        string_image = b64encode(file2.read())
        string_image = string_image.decode('ascii')
        file2.close()
        # send image with name as a json
        return jsonify({"image" : string_image}), 201

if __name__ == '__main__':
    app.run(host='10.42.0.1', port=8000)
#192.168.100.17
