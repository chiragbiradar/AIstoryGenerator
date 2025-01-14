import os
os.environ['OPENAI_API_KEY'] = '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'

from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# Initialize the OpenAI client
client = OpenAI()

def generate_consistent_character(prompt, output_file="output.png"):
    """
    Generate a consistent character using DALL·E 3 with a detailed prompt.
    
    Args:
        prompt (str): The detailed prompt describing the character and scene.
        output_file (str): The filename to save the generated image.
    """
    try:
        # Generate the image using DALL·E 3
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1
        )
        
        # Get the image URL
        image_url = response.data[0].url
        
        # Download and save the image
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        image.save(output_file)
        print(f"Image saved as {output_file}")
        
    except Exception as e:
        print(f"Error generating image: {e}")

# Example usage
if __name__ == "__main__":
    # Define a detailed prompt for the initial character
    initial_prompt = """
    A young woman with curly black hair, wearing a red dress, and holding a book. 
    She has green eyes and a mole on her left cheek. She is standing in a library.
    """
    
    # Generate the initial character image
    generate_consistent_character(initial_prompt, "initial_character.png")
    
    # Define a detailed prompt for the consistent character in a new scene
    new_prompt = """
    The same young woman with curly black hair, wearing a red dress, and holding a cup of coffee. 
    She has green eyes and a mole on her left cheek. She is smiling and sitting in a cozy café.
    """
    
    # Generate the consistent character image
    generate_consistent_character(new_prompt, "consistent_character.png")