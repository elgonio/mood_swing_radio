from mido import MidiFile
import os

'''
returns a list containing a trio of notes 
and the durations and velocities of those notes
in the format: 
note3,note3_v,note3_t,type note2,note2_v,note2_t,type note1,note1_v,note1_t,type  note0,note0_v,note0_t,type 
'''
def get_states_vt(midi_file_name):
	output_list = []
	try:
		midi_file = MidiFile(midi_file_name)
	except Exception as e:
		return []
	count = 0
	total = 0
	# the following represent the current note and the 3 preceding notes
	note_3 = "0,0,0,0"
	note_2 = "0,0,0,0"
	note_1 = "0,0,0,0"
	note_0 = "0,0,0,0"
	for i, track in enumerate(midi_file.tracks):
		#print('=== Track {}\n'.format(i))	
		for message in track:
			#print(' {!r}\n'.format(message))
			fields = str(message).split(" ")		
			if fields[0] == "note_on" or fields[0] == "note_off":
				note_type = 1
				if fields[0] == "note_on":
					note_type = 1
				else:
					note_type = 0

				if message.time != 0 :
					count = count + 1
					note_3 = note_2
					note_2 = note_1
					note_1 = note_0
					note_0 = str(message.note) + ',' + str(message.velocity) + ',' + str(message.time) + ',' + str(note_type)
					output_string = str(note_3) + ',' + str(note_2) + ',' + str(note_1) + ' ' + str(note_0)
					output_string = output_string
					output_list.append(output_string)

	return output_list

print("obtaining list of files")
file_list = os.listdir("midi_files")
file_dict = dict()

states_list = []
print("generating states")
for file_name in file_list:
	try:
		states_list = states_list + get_states_vt("midi_files/"+file_name)
	except Exception as e:
		print("ERROR")
	
with open("states_list_vt.txt",'w+',encoding='utf8') as output_file:
	print("writing states to file")
	print(len(states_list), "records")
	for state in states_list:
		output_file.write(state + '\n')
		