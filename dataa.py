import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from fpdf import FPDF
from streamlit_lottie import st_lottie
import json

# Initialize the OpenAI client
import os

# Load environment variables from .env file using os.environ
with open('.env') as f:
    for line in f:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])  # Use OpenAI API key from environment variable

# Function to load Lottie animation from a URL
def load_lottie(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Function to generate an image using DALL·E 3
def generate_image(prompt, output_file="output.png"):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1
        )
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        image.save(output_file)
        return output_file
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

# Function to save story and images as PDF
def save_to_pdf(story, image_files, output_file="story.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, story)
    for image_file in image_files:
        pdf.add_page()
        pdf.image(image_file, x=10, y=10, w=180)
    pdf.output(output_file)

# Streamlit App
def main():
    st.title("AI Story Generator with Lottie Animations 🎨📖")

    # Load Lottie animation
    lottie_url = "https://assets10.lottiefiles.com/packages/lf20_0yfsb3a1.json"  # Example Lottie animation URL
    lottie_animation = load_lottie(lottie_url)

    if lottie_animation:
        st_lottie(lottie_animation, height=300, key="animation")

    # User input for story generation
    st.sidebar.header("Input Parameters")
    characters = st.sidebar.text_input("Characters (e.g., Brave Knight, Cunning Dragon):")
    setting = st.sidebar.text_input("Setting (e.g., Medieval Kingdom, Dark Cave):")
    tone = st.sidebar.selectbox("Tone:", ["Adventurous", "Mysterious", "Humorous", "Dark"])
    story_length = st.sidebar.slider("Story Length (in words):", 100, 500, 200)

    if st.sidebar.button("Generate Story"):
        # Generate story using GPT-4
        prompt = f"Write a {tone.lower()} story about {characters} in {setting}. The story should be {story_length} words long."
        with st.spinner("Generating story..."):
            response = client.chat.completions.create(
                model="gpt-4",  # Use GPT-4
                messages=[
                    {"role": "system", "content": "You are a creative storyteller."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=story_length + 100,
                temperature=0.7
            )
            story = response.choices[0].message.content.strip()

        # Display the generated story
        st.subheader("Generated Story 📖")
        st.write(story)

        # Split the story into scenes for frames
        scenes = story.split("\n\n")  # Split by paragraphs
        st.subheader("Story Frames 🖼️")

        image_files = []
        # Generate and display images for each scene
        for i, scene in enumerate(scenes):
            st.write(f"**Scene {i+1}:**")
            st.write(scene)

            # Generate an image for the scene using DALL·E 3
            with st.spinner(f"Generating image for Scene {i+1}..."):
                image_prompt = f"A scene from a story: {scene}"
                image_file = generate_image(image_prompt, f"scene_{i+1}.png")
                if image_file:
                    st.image(image_file, caption=f"Scene {i+1}", use_container_width=True)
                    image_files.append(image_file)

        # Save story and images as PDF
        with st.spinner("Saving story as PDF..."):
            save_to_pdf(story, image_files, "story.pdf")
            st.success("Story saved as PDF!")

        # Display Lottie animation again
        if lottie_animation:
            st_lottie(lottie_animation, height=300, key="animation_end")

        # Provide download link for the PDF
        with open("story.pdf", "rb") as f:
            st.download_button(
                label="Download Story as PDF",
                data=f,
                file_name="story.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()