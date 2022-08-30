from pymfe.mfe import MFE
import arff

def create_feature_usecase(db, request_data):
	print(request_data)
	features = extract_features(request_data["path"])
	datasetId = request_data["datasetId"]
	print(features, datasetId)
	insert_extracted_features(db, datasetId, features)
	return

def extract_features(path):
	# Getting data from ARFF format:
	data = arff.load(open(path, 'r'))['data']
	X = [i[:4] for i in data]
	y = [i[-1] for i in data]

	# Extract all available measures
	mfe = MFE(groups="all")
	mfe.fit(X, y)
	ft = mfe.extract()

	for index, line in enumerate(ft[1]):
		ft[1][index] = float(line)

	return ft

def insert_extracted_features(db, datasetId, features):
	try:
		db.features.insert_one({
			"datasetId": datasetId,
			"keys": features[0],
			"values": features[1]
		})
	except Exception as ex:
		print(ex)
	return
