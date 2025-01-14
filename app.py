import streamlit as st
from openai import OpenAI
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Initialize the OpenAI client
client = OpenAI(api_key="your-openai-api-key")  # Replace with your OpenAI API key

# Streamlit App Title
st.title("AI Story Generator with Frames 🎨📖")

# Sidebar for user input
st.sidebar.header("Input Parameters")
characters = st.sidebar.text_input("Characters (e.g., Brave Knight, Cunning Dragon):")
setting = st.sidebar.text_input("Setting (e.g., Medieval Kingdom, Dark Cave):")
tone = st.sidebar.selectbox("Tone:", ["Adventurous", "Mysterious", "Humorous", "Dark"])
story_length = st.sidebar.slider("Story Length (in words):", 100, 500, 200)

# Generate Story Button
if st.sidebar.button("Generate Story"):
    # Create a prompt for GPT-4
    prompt = f"Write a {tone.lower()} story about {characters} in {setting}. The story should be {story_length} words long."
    
    # Call OpenAI GPT-4 API
    with st.spinner("Generating story..."):
        response = client.chat.completions.create(
            model="gpt-4",  # Use GPT-4 or "gpt-3.5-turbo" if GPT-4 is not available
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

    # Generate and display images for each scene
    for i, scene in enumerate(scenes):
        st.write(f"**Scene {i+1}:**")
        st.write(scene)

        # Generate an image for the scene using DALL·E 3
        with st.spinner(f"Generating image for Scene {i+1}..."):
            image_prompt = f"A scene from a story: {scene}"
            image_response = client.images.generate(
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = image_response.data[0].url
        
        # Display the generated image
        st.image(image_url, caption=f"Scene {i+1}", use_column_width=True)

        # Add text to the image (optional)
        with st.spinner(f"Adding text to Scene {i+1}..."):
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            draw.text((10, 10), f"Scene {i+1}", font=font, fill="white")
            st.image(img, caption=f"Scene {i+1} with Text", use_column_width=True)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Welcome to the AI Story Generator! Enter your details in the sidebar and click 'Generate Story'.")