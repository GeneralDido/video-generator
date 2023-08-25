
# Video Generator Documentation

## Overview

The Video Generator app creates video content based on given story prompts. It leverages LeonardoAI API for image generation and ElevenlabsAPI for voice and GPT4 for writing small stories. It generates everything automatically in a few seconds to generate images and voiceovers. The app then combines these elements, adding text and background music to generate a final video.
You can see a working example video here:
https://drive.google.com/file/d/1ZPxZwSx4nt9OKAaPQwfZuiwAWM-h-2bT/view


## Table of Contents

1. [How to Use](#how-to-use)
2. [Dependencies](#dependencies)
3. [Modules](#modules)
    - [ImageGenerator.py](#imagegeneratorpy)
    - [VideoGenerator.py](#videogeneratorpy)
    - [VoiceoverGenerator.py](#voiceovergeneratorpy)
    - [helper_functions.py](#helper_functionspy)
    - [main.py](#mainpy)
    - [story_and_prompts.py](#story_and_promptspy)

## How to Use

1. Set up your environment variables in a `.env` file in the root directory. This file should contain your `LEONARDO_API_KEY` and `ELEVEN_API_KEY`.
2. Modify the `story` and `prompts` lists in `story_and_prompts.py` as required.
3. Run `main.py` to generate the video based on the story and prompts provided.

## Dependencies

- `dotenv`: For loading environment variables.
- `requests`: For making HTTP requests to external services.
- `PIL`: For image manipulation.
- `moviepy`: For video generation and editing.
- `pydub`: For audio manipulation.
- `elevenlabs`: For generating voiceovers.
- `natsorted`: For natural sorting of files.

## Modules

### -ImageGenerator.py

Generates images based on prompts using the Leonardo service.

#### Class `ImageGenerator`:

- `__init__()`: Initializes the class and sets the Leonardo API key.
- `_generate_image(prompt: str)`: Generates an image for a given prompt.
- `_generate_images(prompts: list)`: Generates multiple images for a list of prompts.
- `_download_image(generationId: str, image_name: str)`: Downloads an image by its generation ID and saves it.
- `_download_images()`: Downloads all generated images.
- `run(prompts: list)`: Generates and downloads images for a list of prompts.

### -VideoGenerator.py

Combines images, voiceovers, and text to produce video clips.

#### Class `VideoGenerator`:

- `__init__(input_images: list, input_voiceovers: list, story: list)`: Initializes the class.
- Various private methods to add text to images, voiceovers to images, and combine multiple video clips.
- `run(background_music: str, output_path: str)`: Generates small video clips and then combines them with background music to produce the final video.

### -VoiceoverGenerator.py

Generates voiceovers based on story text using the Eleven Labs service.

#### Class `VoiceoverGenerator`:

- `__init__()`: Initializes the class and sets the Eleven Labs API key.
- `generate_voiceover(audio_text: str, voiceover_name: str)`: Generates a voiceover for a given text.
- `generate_voiceovers(story_list)`: Generates multiple voiceovers for a list of storylines.

### -helper_functions.py

Provides utility functions for the main app.

- `generate_all_voiceovers(story: list)`: Generates voiceovers for the entire story.
- `generate_all_images(prompts: list)`: Generates images for all prompts.
- `get_files(directory, extension='.jpg')`: Returns a naturally sorted list of files with a given extension from a directory.

### -main.py

Main execution file for the app.

- Sets up the environment variables.
- Generates voiceovers and images based on the `story` and `prompts`.
- Combines the generated content into a final video.

### -story_and_prompts.py

Contains the `story` and `prompts` data lists. Modify these lists as required to generate content based on different stories and image prompts.
