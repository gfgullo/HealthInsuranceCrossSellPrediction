from flask import jsonify, request
from . import api
from ..ml import predict


@api.route('/predict')
def predict_view():
    response, confidence = predict(request.json)
    return jsonify({"response": response, "confidence": confidence})
