from dotenv import dotenv_values
import requests
import time
import urllib.request

config = dotenv_values(".env")
PATH = '/Users/dimitrispanouris/VisualStudioCodeProjects/video-generator/'

class ImageGenerator:
    def __init__(self):
        self.generationIds = []
        leonardo_key = config.get('LEONARDO_API_KEY')
        if leonardo_key is not None:
            self.bearer = "Bearer " + leonardo_key
        else:
            self.bearer = "Bearer "
    
    def _generate_image(self, prompt: str) -> str:    
        url = "https://cloud.leonardo.ai/api/rest/v1/generations"
        
        payload = {
            "prompt": prompt,
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
            "width": 768,
            "height": 768,
            "num_images": 1,
            "num_inference_steps": 45,
            "guidance_scale": 7,
            "presetStyle": "LEONARDO",
            "promptMagic": True,
            "public": False
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.bearer
        }

        response = requests.post(url, json=payload, headers=headers)

        generation_response = response.json()
        generationId = generation_response['sdGenerationJob']['generationId']
        time.sleep(15)
        return generationId

    def _generate_images(self, prompts: list) -> list:
        for prompt in prompts:
            generationId = self._generate_image(prompt)
            self.generationIds.append(generationId)
        return self.generationIds

    def _download_image(self, generationId: str, image_name: str) -> None:
        url = "https://cloud.leonardo.ai/api/rest/v1/generations/" + generationId

        headers = {
            "accept": "application/json",
            "authorization": self.bearer
        }

        response = requests.get(url, headers=headers)
        image = response.json()
        # Get the URL of the image from the JSON response
        image_url = image["generations_by_pk"]["generated_images"][0]["url"]

        # Download the image and save it to a file
        urllib.request.urlretrieve(image_url, PATH + 'images_input/' + image_name + '.jpg')

    def _download_images(self) -> None:
        for i in range(len(self.generationIds)):
            print('Downloading image ' + str(i) + ' of generationId ' + str(self.generationIds[i]))
            self._download_image(self.generationIds[i], 'image_input_' + str(i))
            print('Image Downloaded')
    
    def run(self, prompts: list) -> None:
        self._generate_images(prompts)
        self._download_images()
