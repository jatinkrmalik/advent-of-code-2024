import os
from openai import OpenAI

# Initialize the OpenAI client
# Make sure to set the OPENAI_API_KEY environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
    prompts = [
        "A colorful, vibrant arcade scene, slightly blurred in the background. In the foreground, on the left side, a detailed, realistic claw machine. The claw machine is brightly lit. Translucent mathematical equations and symbols are subtly overlaid on the claw machine and extend slightly into the background. The overall style is photorealistic with bright, contrasting colors.",
        "A close-up view from inside a claw machine, looking up towards the claw. The claw is the central element. The background is a blur of colorful plush toys. Various mathematical symbols and equations float around the claw, rendered in a slightly glowing style.",
        "An illustrated, cartoon-style image of a brightly colored claw machine with a playful, exaggerated design. The claw machine is positioned on the right side of the frame. To the left of the claw machine is a large, prominent question mark. The background is a solid, dark blue color. The image has a fun, engaging style."
    ]

    for i, prompt in enumerate(prompts):
        print(f"Generating image {i+1}...")
        image_urls = generate_image(prompt)

        if image_urls:
            for j, url in enumerate(image_urls):
                print(f"  Image {i+1}-{j+1} URL: {url}")
                # Display the image in an IPython environment (like Jupyter Notebook)
                # display(Image(url=url))
        else:
            print(f"Failed to generate image {i+1}.")