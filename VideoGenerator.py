import os
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Optional
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from pydub import AudioSegment
import textwrap
from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.AudioClip import concatenate_audioclips
from helper_functions import get_files

PATH = '/Users/dimitrispanouris/VisualStudioCodeProjects/video-generator/'
font_path = os.path.join(os.path.dirname(__file__), PATH + "fonts/SparkyStonesRegular.ttf")

class VideoGenerator:
    def __init__(self, input_images: list, input_voiceovers: list, story: list):
        self.input_images = input_images
        self.input_voiceovers = input_voiceovers
        self.story = story


    def _add_text_to_image(self, image_path: str, text: str, output_path: str, font_path: str = font_path, font_size: int = 48, text_position: Optional[Tuple[int, int]] = None, fill_color: Tuple[int, int, int] = (242, 143, 189)) -> None:
        """
        Takes the path to an image file and a text string as input, inserts the text into the image, and saves the new image to the specified output path.
        """
        # Load the image
        image = Image.open(image_path)

        # Create a drawing context
        draw = ImageDraw.Draw(image)

        # Load the font
        font = ImageFont.truetype(font_path, font_size)

        # Calculate the maximum width and height of the text
        max_width = int(image.width * 0.8)
        max_height = int(image.height * 0.8)

        # Wrap the text into multiple lines that fit within the maximum width of the image
        lines = textwrap.wrap(text, width=28)

        # Calculate the total height of the text
        total_height = len(lines) * font_size

        # Calculate the position to draw the text
        x = (image.width - max_width) / 2
        y = (image.height - total_height) / 1.3  # we change the height of text in the image here (<2 for down, >2 for up)

        # Draw each line of text on the image
        for line in lines:
            text_bbox = draw.textbbox((x, y), line, font=font)
            draw.text((x, y), line, font=font, fill=fill_color)
            y += font_size

        # Save the new image to the output path
        image.save(output_path, quality=100)


    def _add_voiceover_to_image(self, image_path: str, voiceover_path: str, output_path: str) -> None:
        """
        Takes the path to an image file and a voiceover file as input, combines them into a single video file, and saves the result to the specified output path.
        """
        # Load the image
        image = ImageClip(image_path)

        # Load the voiceover
        voiceover = AudioSegment.from_file(voiceover_path)

        # Create a video clip from the image with the duration of the voiceover
        # image_clip = image.set_duration(voiceover.duration_seconds)

        # Set the duration of the image clip to include the pause
        image_clip = image.set_duration(voiceover.duration_seconds + 0.5)


        # Convert the voiceover to an AudioFileClip object
        voiceover_clip = AudioFileClip(voiceover_path)


        # Add a pause between the image and the voiceover
        pause = AudioFileClip(PATH + '/silent_audio/silent_half-second.mp3')
        voiceover_clip = concatenate_audioclips([pause, voiceover_clip])


        # Combine the image clip and the voiceover clip
        video = CompositeVideoClip([image_clip.set_audio(voiceover_clip)])

        # Save the new video to the output path
        video.write_videofile(output_path, audio_codec="aac", codec="libx264", bitrate="5000k", fps=30)


    def _combine_videos(self, video_directory: str, background_music_path: str, output_path: str) -> None:
        """
        Takes a directory path and a path to a background music file as input, gets all video files in the directory, combines them into a single video file with a 0.5 second pause between each clip, adds the background music, and saves the result to the specified output path.
        """
        # Get all video files in the directory
        video_paths = [os.path.join(video_directory, f) for f in get_files(video_directory, extension='.mp4')]

        # Load the videos
        videos = [VideoFileClip(path) for path in video_paths]

        # Combine the videos
        final_video = concatenate_videoclips(videos)

        # Load the background music
        background_music = AudioFileClip(background_music_path)

        # Loop the background music to match the duration of the final video
        background_music = background_music.volumex(0.35)
        background_music = background_music.fx(vfx.loop, duration=final_video.duration)

        # Get the existing audio from the final video
        existing_audio = final_video.audio

        # Combine the existing audio with the background music
        new_audio = CompositeAudioClip([existing_audio, background_music])

        # Set the new audio for the final video
        final_video = final_video.set_audio(new_audio)

        # Save the final video
        final_video.write_videofile(output_path, audio_codec="aac", codec="libx264", bitrate="5000k", fps=30)

    def _generate_small_videos(self):
        for i in range(len(self.story)):
            self._add_text_to_image(PATH + 'images_input/' + self.input_images[i], self.story[i], PATH + 'images_text_output/' + self.input_images[i])
            self._add_voiceover_to_image(PATH + 'images_text_output/' + self.input_images[i], PATH + 'voiceover_input/' + self.input_voiceovers[i], PATH + 'videos_output/' + self.input_images[i].replace('.jpg', '.mp4'))

    def run(self, background_music: str, output_path: str):
        self._generate_small_videos()
        self._combine_videos(PATH + 'videos_output/', PATH + 'background_music/' + background_music, PATH + 'final_videos/' + output_path)
