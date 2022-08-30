from flask import Flask, request, Response, jsonify
import numpy as np
import pymongo
import json
from create_feature_usecase import create_feature_usecase
from bson.objectid import ObjectId
import simplejson

app = Flask(__name__)

try:
	mongo = pymongo.MongoClient(
		host="localhost",
		port=27017,
		serverSelectionTimeoutMS = 1000
	)
	db = mongo.nest
	mongo.server_info()
except:
	print('Erro connecting to mongo')

@app.route('/save_feature', methods=['POST'])
def saveFeature():
	try:
		request_data = request.get_json()
		create_feature_usecase(db, request_data)
		response = Response(
			response = json.dumps({
				"message": "feature created",
			}),
			status = 201,
			mimetype = 'application/json'
		)
		return response
	except Exception as ex:
		print(ex)
		response = Response(
			response = json.dumps({
				"error": "something went wrong",
			}),
			status = 500,
			mimetype = 'application/json'
		)
		return response
	
@app.route('/get_features', methods=['GET'])
def getFeatures():
	try:
		print(request.args.get('id'))
		datasetIds = request.args.get('id').split(",")
		print(datasetIds)
		data = list(db.features.find({
			"datasetId": {"$in": datasetIds}
		}))
		for feature in data:
			feature["_id"] = str(feature["_id"])

		print(data)
		response = Response(
			response = simplejson.dumps(data, ignore_nan=True),
			status = 201,
			mimetype = 'application/json'
		)
		return response
	except Exception as ex:
		print(ex)
		response = Response(
			response = json.dumps({
				"error": "something went wrong",
			}),
			status = 500,
			mimetype = 'application/json'
		)
		return response