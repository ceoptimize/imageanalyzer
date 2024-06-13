import os
import base64
import requests
from dotenv import load_dotenv

class GPTImageAnalyzer:
    def __init__(self, dotenv_path='venv/.env'):
        load_dotenv(dotenv_path=dotenv_path)
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("API Key not found")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def create_payload_for_images(self, image_paths, prompt):
        content = [{"type": "text", "text": prompt}]
        
        for image_path in image_paths:
            base64_image = self.encode_image(image_path)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        
        return {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "max_tokens": 2048
        }
    
    def create_payload_for_single_image(self, image_path, prompt):
        base64_image = self.encode_image(image_path)
        return {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
    
    def analyze_multiple_images(self, image_folder, prompt, output_folder, output_file):
        image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpeg') or f.endswith('.png')])
        payload = self.create_payload_for_images(image_files, prompt)
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                message_content = response_data['choices'][0]['message']['content']
            else:
                message_content = "No valid response received."
        else:
            message_content = f"Request failed with status code: {response.status_code}"
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        output_path = os.path.join(output_folder, output_file)
        with open(output_path, 'w') as file:
            file.write(message_content)
        
        print("All images processed. Output saved to", output_path)
    
    def analyze_single_image(self, image_path, prompt, output_folder, output_file):
        payload = self.create_payload_for_single_image(image_path, prompt)
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                message_content = response_data['choices'][0]['message']['content']
            else:
                message_content = "No valid response received."
        else:
            message_content = f"Request failed with status code: {response.status_code}"
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        output_path = os.path.join(output_folder, output_file)
        with open(output_path, 'w') as file:
            file.write(message_content)
        
        print("Image processed. Output saved to", output_path)

