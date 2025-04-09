# from diffusers import StableDiffusionPipeline
# import torch

# # Load the model (first time will download)
# pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", 
#                                                torch_dtype=torch.float16)
# pipe = pipe.to("c")  # Use GPU

# # Generate image
# prompt = "a futuristic city in space, artstation style"
# image = pipe(prompt).images[0]

# # Save image
# image.save("output.png")


import requests
import os
API_KEY = os.getenv('Huggingface_Image_Generation')
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {API_KEY}"}

data = {
    "inputs": "Generate an image of a dog, sketch art."
}

response = requests.post(API_URL, headers=headers, json=data)

# Save image
if response.status_code == 200:
    with open("image.png", "wb") as f:
        f.write(response.content)
else:
    print("Error:", response.text)

