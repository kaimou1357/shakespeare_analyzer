import requests
from xml.etree import ElementTree
#Author: Kai Mou

speaker_data = {}

def get_xml_data(link):
	r = requests.get(link, stream = True)
	if r.status_code == requests.codes.ok:
		print 'Getting speaker data!'
		get_speaker_data(r.content)
	else:
		print 'Could not connect to the source link provided'

def get_speaker_data(xml):
	#play/act/scene/speech
	tree = ElementTree.fromstring(xml)	

	for act in tree.findall('ACT'):
		for scene in act.findall('SCENE'):
			process_scene(scene)
	output_speaker_data()

def output_speaker_data():

	for speaker, num_lines in speaker_data.iteritems():
		print "{num_lines} : {speaker_data}".format(num_lines = num_lines, speaker_data = speaker.title())


def process_scene(scene):
	for speech in scene.findall('SPEECH'):
		speaker = speech.find('SPEAKER').text
		num_lines = len(speech.findall('LINE'))
		if speaker == 'ALL':
			#Skip the lines with speaker as "ALL"
			continue
		if speaker in speaker_data:
			#If speaker is in speaker_data, update the dictionary
			speaker_data[speaker] +=num_lines
		else:
			speaker_data[speaker] = num_lines
	

get_xml_data('http://www.ibiblio.org/xml/examples/shakespeare/macbeth.xml')
	