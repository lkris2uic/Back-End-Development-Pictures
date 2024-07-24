from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        abort(404, description="Picture not found")

######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    if any(item["id"] == picture["id"] for item in data):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.get_json()
    for i, picture in enumerate(data):
        if picture["id"] == id:
            data[i] = updated_picture
            return jsonify(updated_picture), 200
    abort(404, description="Picture not found")

######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        data = [item for item in data if item["id"] != id]
        return '', 204
    else:
        abort(404, description="Picture not found")
