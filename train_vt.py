#from mido import Message, MidiFile, MidiTrack
#import mido
import pickle
import random
#import numpy as np 
#from pprint import pprint

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def read_file_into_dict(filename):
	length = file_len(filename)
	result = dict()
	with open(filename,'r') as input_file:
		count = 0
		for line in input_file:
			count = count+1
			print("progress = ",count/length)
			line = line.strip()
			curr_state = line.split(",")[0]+','+line.split(",")[1]+','+line.split(",")[2]
			curr_state = curr_state.strip()
			if curr_state in result:
				pass
			else:
				result[curr_state]= dict()

			next_state = line.split(",")[3]
			if next_state in result[curr_state]:
				result[curr_state][next_state] += 1
			else:
				result[curr_state][next_state] = 1

			for key in result:
				total = sum(result[key].values())
				for inner_key in result[key]:
					result[key][inner_key] = float(result[key][inner_key])/total
				#print(key, result[key])

	return result		

def read_file_into_dict_vt(filename):
	length = file_len(filename)
	result = dict()
	with open(filename,'r') as input_file:
		count = 0
		for line in input_file:
			count = count+1
			print("progress = ",count/length)
			line = line.strip()
			curr_state = line.split(" ")[0]
			if curr_state in result:
				pass
			else:
				result[curr_state]= dict()

			next_state = line.split(" ")[1]
			if next_state in result[curr_state]:
				result[curr_state][next_state] += 1
			else:
				result[curr_state][next_state] = 1

			for key in result:
				total = sum(result[key].values())
				for inner_key in result[key]:
					result[key][inner_key] = float(result[key][inner_key])/total
				#print(key, result[key])

	return result		


def predict(note_3,note_2,note_1,states_dict):
	key = str(note_3)+','+str(note_2)+','+str(note_1)
	if key in states_dict:
		states = states_dict[key]
	else:
		states = states_dict["0,0,0"]
	
	elements = []
	weights  = []
	for k in states:
		elements.append(k)
		weights.append(states[k])

	try:
		result = np.random.choice(elements,p=weights)
	except Exception as e:
		print("elements:", len(elements))
		print("weights:", len(weights))
		result = str(random.randint(0,127)) + " " + "512"
	
	return result

def predict_vt(note_3,note_2,note_1,states_dict):
	key = str(note_3)+','+str(note_2)+','+str(note_1)
	if key in states_dict.keys():
		states = states_dict[key]
	else:
		print("ERROR")
		print(key)
		default = np.random.choice(list(states_dict.keys()))
		states = states_dict[default]
		#pprint(states)
	
	elements = []
	weights  = []
	for k in states:
		elements.append(k)
		weights.append(states[k])

	try:
		result = np.random.choice(elements,p=weights)
	except Exception as e:
		print("elements:", len(elements))
		print("weights:", len(weights))
		result = "0,0,0,0"
	
	return result

def predict_message(message_3,message_2,message_1,states_dict):
	key = str(message_3)+','+str(message_2)+','+str(message_1)
	if key in states_dict:
		states = states_dict[key]
	else:
		print("ERROR")
		states = states_dict["note_on channel=0 note=74 velocity=0 time=94,note_on channel=0 note=81 velocity=0 time=0,note_on channel=0 note=74 velocity=110 time=2"]
	
	elements = []
	weights  = []
	for k in states:
		elements.append(k)
		weights.append(states[k])

	try:
		result = np.random.choice(elements,p=weights)
	except Exception as e:
		print("elements:", len(elements))
		print("weights:", len(weights))
		result = str(random.randint(0,127)) + " " + "512"
	
	return result


def test():
	print("constructing states from file")
	states_dict = read_file_into_dict("states_list_sample_m.txt")
	save_obj(states_dict,"sample_dict")
	#print(states_dict["67,72,72"])
	#print("reading states from pickle file")
	#states_dict = load_obj("full_dict")
	#print(states_dict["<meta message track_name name='Piano Template' time=0>,<meta message track_name name='Piano Template' time=0>,<meta message track_name name='Piano Template' time=0>"])
	k = random.choice(list(states_dict.keys()))
	print(k, states_dict[k])
	'''
	for x in range(5):
		print(predict(67,72,72,states_dict))
	'''
def train(filename):
	states_dict = read_file_into_dict(filename)
	save_obj(states_dict,filename[:-4])

def train_vt(filename):
	states_dict = read_file_into_dict_vt(filename)
	save_obj(states_dict,filename[:-4])
	
#test()
file = "states_list_vt"
train_vt(file+".txt")
#states_dict = load_obj(file)
#print("keys",len(list(states_dict.keys())))
#pprint(list(states_dict.keys()))
#print("constructing song")
#alt_construct_song(states_dict)


