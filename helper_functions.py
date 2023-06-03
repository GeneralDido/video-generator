import os
from VoiceoverGenerator import VoiceoverGenerator
from ImageGenerator import ImageGenerator
from natsort import natsorted

def generate_all_voiceovers(story: list):
    voiceoverGenerator = VoiceoverGenerator()
    voiceoverGenerator.generate_voiceovers(story)

def generate_all_images(prompts: list):
    imageGenerator = ImageGenerator()
    imageGenerator.run(prompts)

def get_files(directory, extension='.jpg'):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Filter the list to only include image files
    files_list = [f for f in files if f.endswith(extension)]

    return natsorted(files_list)
