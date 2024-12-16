import os
import yaml
import requests
from openai import OpenAI

# Initialize the OpenAI client
# Make sure to set the OPENAI_API_KEY environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def generate_image(prompt, model="dall-e-3", size="1792x1024", quality="hd", n=1):
    """
    Generates an image using the OpenAI DALL-E 3 API.

    Args:
        prompt: The text prompt for image generation.
        model: The model to use (default: "dall-e-3").
        size: The size of the generated image (default: "1792x1024" for landscape).
        quality: The quality of the image ("hd" for high quality).
        n: The number of images to generate (default: 1).

    Returns:
        A list of image URLs if successful, None otherwise.
    """
    try:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
        )

        image_urls = [img.url for img in response.data]
        return image_urls
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    config = load_config('config.yaml')
    prompts = config['prompts']
    model = config.get('model', 'dall-e-3')
    size = config.get('size', '1792x1024')
    quality = config.get('quality', 'hd')
    n = config.get('n', 1)
    if not os.path.exists('./gen-images'):
        os.makedirs('./gen-images')

    for i, prompt in enumerate(prompts):
        print(f"Generating image {i+1}...")
        image_urls = generate_image(prompt, model=model, size=size, quality=quality, n=n)

        if image_urls:
            for j, url in enumerate(image_urls):
                print(f"  Image {i+1}-{j+1} URL: {url}")
                response = requests.get(url)
                if response.status_code == 200:
                    with open(f'./gen-images/image_{i+1}_{j+1}.png', 'wb') as f:
                        f.write(response.content)
                else:
                    print(f"Failed to download image {i+1}-{j+1}.")
        else:
            print(f"Failed to generate image {i+1}.")