import os
import logging
import uuid
from google.cloud import storage
import vertexai
from vertexai.preview.vision_models import Image, ImageGenerationModel
# from vertexai.preview.vision_models import RawReferenceImage
from vertexai.preview.vision_models import SubjectReferenceImage
from dotenv import load_dotenv
from utils.constants import IMAGEN_GENERATE_MODEL_NAME, IMAGEN_EDIT_MODEL_NAME

# from google.genai.types import SubjectReferenceImage


# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Google Cloud Storage Client
storage_client = storage.Client()
bucket = storage_client.bucket(os.getenv("GCP_BUCKET_NAME"))

# Initialize Vertex AI
vertexai.init(project=os.getenv("GOOGLE_PROJECT_ID"), location=os.getenv("LOCATION"))

# Generate an image using Imagen model
async def generate_image_with_imagen(refined_prompt: str):
    """Call to Imagen model to generate an image (e.g., human model)"""
    try:
        logger.debug(f"Generating content with refined prompt: {refined_prompt}")

        # Select the model
        model = ImageGenerationModel.from_pretrained(IMAGEN_GENERATE_MODEL_NAME)

        # Generate images using the model and prompt
        images = model.generate_images(
            prompt=refined_prompt,
            language="en",
            safety_filter_level="block_most",
            number_of_images=1,
            aspect_ratio="1:1",
            # Add more parameters if needed
        )

        # Save the image to Google Cloud Storage
        file_name = f"generated_images/{uuid.uuid4()}.jpg"
        blob = bucket.blob(file_name)
        # Assuming images[0]._image_bytes is valid byte data
        blob.upload_from_string(images[0]._image_bytes, content_type="image/jpeg")

        return f"gs://{bucket.name}/{file_name}"

    except Exception as e:
        logger.error(f"Failed to generate image with the following error: {str(e)}")
        logger.error(f"Request details: refined_prompt: {refined_prompt}")
        raise Exception(f"Error generating image with Imagen: {str(e)}")


async def generate_clothing_with_imagen(reference_image_path: str, refined_prompt: str):
    """Generate clothing for the human model using refined prompt and Google Imagen"""
    try:
        logger.debug(f"Generating content with refined prompt: {refined_prompt}")

        # Load the base image
        base_img = Image.load_from_file(location=reference_image_path)
        # raw_ref_image = RawReferenceImage(image=base_img, reference_id=0)

        subject_reference_image = SubjectReferenceImage(
            reference_id=1,
            image=base_img,
            subject_type="person",
            )

        # Select the model
        model = ImageGenerationModel.from_pretrained(IMAGEN_EDIT_MODEL_NAME)
        # model = IMAGEN_EDIT_MODEL_NAME

        # Generate images using the model and prompt
        images = model.edit_image(
            prompt=refined_prompt,
            language="en",
            number_of_images=1,
            # safety_filter_level="block_few",
            # aspect_ratio="1:1",
            # person_generation="allow_adult",
            
            edit_mode="default",
            reference_images=[subject_reference_image],
            # Add more parameters if needed
        )

        # Save the image to Google Cloud Storage
        file_name = f"generated_images/{uuid.uuid4()}.jpg"
        blob = bucket.blob(file_name)
        # Assuming images[0]._image_bytes is valid byte data
        blob.upload_from_string(images[0]._image_bytes, content_type="image/jpeg")

        return f"gs://{bucket.name}/{file_name}"

    except Exception as e:
        logger.error(f"Failed to generate clothing with the following error: {str(e)}")
        logger.error(f"Request details: refined_prompt: {refined_prompt}")
        raise Exception(f"Error generating clothing with Imagen: {str(e)}")