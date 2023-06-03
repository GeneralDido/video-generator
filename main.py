from dotenv import dotenv_values
from story_and_prompts import story, prompts
from VideoGenerator import VideoGenerator
from helper_functions import get_files, generate_all_images, generate_all_voiceovers

config = dotenv_values(".env")
PATH = '/Users/dimitrispanouris/VisualStudioCodeProjects/video-generator/'

generate_all_voiceovers(story)
generate_all_images(prompts)

input_images = get_files(PATH + 'images_input/')
input_voiceovers = get_files(PATH + 'voiceover_input/', '.mp3')

videoGenerator = VideoGenerator(input_images, input_voiceovers, story)
videoGenerator.run('magic-in-the-air.mp3' , 'final_video2.mp4')