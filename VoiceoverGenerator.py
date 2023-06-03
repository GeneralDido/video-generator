from elevenlabs import set_api_key
from dotenv import dotenv_values
from elevenlabs import voices, generate, save
config = dotenv_values(".env")
PATH = '/Users/dimitrispanouris/VisualStudioCodeProjects/video-generator/'

class VoiceoverGenerator:
    def __init__(self) -> None:
        self.api_key = config.get('ELEVEN_API_KEY')
        if self.api_key is not None:
            set_api_key(self.api_key)

    def generate_voiceover(self, audio_text: str, voiceover_name: str) -> None:

        voice_list = voices()
        audio = generate(api_key=self.api_key, text=audio_text, voice=voice_list[-1])

        save(audio, PATH + 'voiceover_input/' + voiceover_name + '.mp3') # type: ignore
        print('Voiceover generated for text: ' + audio_text)
    
    def generate_voiceovers(self, story_list) -> None:
        for i in range(len(story_list)):
            self.generate_voiceover(story_list[i], 'voiceover_' + str(i))
