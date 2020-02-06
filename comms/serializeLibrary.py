import numpy as np
import io, json
import pickle

def serializeNumpyArray(array):
	memfile = io.BytesIO()
	np.save(memfile, array)
	memfile.seek(0)
	return json.dumps(memfile.read().decode('latin-1'))

def serializeAsBytes(array):
	return pickle.dumps(array, protocol=0)


def deserializeNumpyArray(string):
	memfile = io.BytesIO()
	memfile.write(json.loads(string).encode('latin-1'))
	memfile.seek(0)
	return np.load(memfile)


