import gradio as gr
import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image

genai.configure(api_key="AIzaSyCNyET5fRqFBRl26iS1_-nZyGu-5eSqyng") 

LANGUAGES = ["Tamil", "Hindi", "Telugu", "Kannada", "Malayalam", "Bengali", "Gujarati", "Marathi", "Punjabi", "Odia"]

def image_to_poem(image, target_language):
    """Generates a short English poem and its translation based on the uploaded image."""
    try:
        
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        image_b64 = base64.b64encode(img_bytes).decode('utf-8')

        
        model = genai.GenerativeModel("gemini-1.5-pro")

        
        description_prompt = "Describe this image briefly in one sentence."
        description_response = model.generate_content([
            {"mime_type": "image/png", "data": image_b64},
            description_prompt
        ])
        description = description_response.text.strip()

       
        poem_prompt = f"Based on this image description: '{description}', write a short 4-line poem in English."
        poem_response = model.generate_content(poem_prompt)
        english_poem = poem_response.text.strip()

       
        translate_prompt = (
            f"Translate the following English poem into {target_language}. "
            f"Only return the translated poem:\n\n{english_poem}"
        )
        translation_response = model.generate_content(translate_prompt)
        translated_poem = translation_response.text.strip()

        
        return f"📜 **English Poem**:\n{english_poem}\n\n🌐 **Translated in {target_language}**:\n{translated_poem}"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


interface = gr.Interface(
    fn=image_to_poem,
    inputs=[
        gr.Image(type="pil", label="Upload an Image"),
        gr.Dropdown(choices=LANGUAGES, label="Choose Translation Language", value="Tamil")
    ],
    outputs=gr.Textbox(label="Generated Poem"),
    title="🖼️ AI-Powered Poem Generator",
    description="Upload an image. The AI will create a short English poem based on the image and translate it into your selected Indian language."
)

if __name__ == "__main__":
    interface.launch()
