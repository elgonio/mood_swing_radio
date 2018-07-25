from mido import Message, MidiFile, MidiTrack
import mido
import pickle
import random
import numpy as np 
from pprint import pprint

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

def predict_vt(note_3,note_2,note_1,states_dict):
	key = str(note_3)+','+str(note_2)+','+str(note_1)
	if key in states_dict.keys():
		states = states_dict[key]
		success = True
		print("SUCCESS")
	else:
		success = False
		print("ERROR")
		#print(key)
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
	
	return result,success

def construct_song_vt(states_dict):
	#note_3 = "50,110,2,1"
	#note_2 = "50,0,142,1"
	#note_1 = "55,110,2,1"
	#note_0 = "55,0,94,1"

	seed = np.random.choice(list(states_dict.keys())).split(",")

	note_3 = seed[0] + "," + seed[1] + "," +seed[2] + "," +seed[3]
	note_2 = seed[4] + "," + seed[5] + "," +seed[6] + "," +seed[7]
	note_1 = seed[8] + "," + seed[9] + "," +seed[10] + "," +seed[11]
	note_0,success = predict_vt(note_3,note_2,note_1,states_dict)
	mid = MidiFile()
	track = MidiTrack()
	mid.tracks.append(track)

	track.append(Message('program_change', program=0, time=0))
	num_notes = 500
	success_rate = 0
	for x in range(num_notes):
		note_0,success = predict_vt(note_3,note_2,note_1,states_dict)
		
		if success == True:
			success_rate = success_rate + 1
		else:
			seed = np.random.choice(list(states_dict.keys())).split(",")

			note_3 = seed[0] + "," + seed[1] + "," +seed[2] + "," +seed[3]
			note_2 = seed[4] + "," + seed[5] + "," +seed[6] + "," +seed[7]
			note_1 = seed[8] + "," + seed[9] + "," +seed[10] + "," +seed[11]
			note_0,success = predict_vt(note_3,note_2,note_1,states_dict)

		#print(note_0)	
		note_3 = note_2
		note_2 = note_1
		note_1 = note_0
		note_x = int(note_0.split(",")[0]) 
		v = int(note_0.split(",")[1])
		t = int(note_0.split(",")[2])
		note_type = int(note_0.split(",")[3])
		#print(note_x)
		
		if note_type == 1:
			track.append(Message('note_on', note=note_x, velocity=v, time=t))
		else:
			track.append(Message('note_off', note=note_x, velocity=v, time=t))
		
	mid.save('new_song_vt.mid')
	print("success rate", success_rate/num_notes)

def train_vt(filename):
	states_dict = read_file_into_dict_vt(filename)
	save_obj(states_dict,filename[:-4])
	
file = "states_list_vt"
#train_vt(file+".txt")
states_dict = load_obj(file)
print("constructing song")
construct_song_vt(states_dict)


