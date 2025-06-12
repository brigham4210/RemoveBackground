import gradio as gr
from rembg import remove
from PIL import Image, ImageEnhance
import io


def process_image(image: Image.Image) -> Image.Image:
    # Convert to bytes and remove background
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    output_bytes = remove(img_bytes.getvalue())
    output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    return output_image


demo = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="pil", label="Upload Image"),
    outputs=gr.Image(type="pil", label="Processed Image"),
    title="Background Remover",
    description="Removes background"
)

if __name__ == "__main__":
    demo.launch()
