from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import shutil
from fastapi.responses import JSONResponse
import logging
import os
import uuid
from pydantic import BaseModel, Field
from typing import Optional
from utils.helper_functions import generate_human_model, generate_clothing, refine_user_prompt, refine_user_prompt_image
from google.cloud import storage
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Google Cloud Storage Client
storage_client = storage.Client()

# Load environment variables
load_dotenv()

# Fetch environment variables
project_id = os.getenv('GOOGLE_PROJECT_ID')
google_storage_bucket = os.getenv("GCP_BUCKET_NAME")

app = FastAPI()

# Define data models for user input
class ClothingItem(BaseModel):
    color: Optional[str] = Field(None, description="Color of the clothing item")
    type: Optional[str] = Field(None, description="Type or style of the clothing item")

class UserInputModel(BaseModel):
    """ Pydantic model to handle user input JSON """
    gender: Optional[str] = Field(None, description="Gender of the model")
    ethnicity: Optional[str] = Field(None, description="Ethnicity of the model")
    age: Optional[str] = Field(None, description="Age of the model")
    body_type: Optional[str] = Field(None, description="Body type of the model")
    mood: Optional[str] = Field(None, description="Mood or expression of the model")
    
    style: Optional[str] = Field(None, description="Overall style of the model")
    occasion: Optional[str] = Field(None, description="Occasion or setting for the model")

    top: Optional[ClothingItem] = Field(None, description="Details of the top clothing item")
    bottom: Optional[ClothingItem] = Field(None, description="Details of the bottom clothing item")
    accessories: Optional[ClothingItem] = Field(None, description="Details of the accessories")
    footwear: Optional[ClothingItem] = Field(None, description="Details of the footwear")
    
    eyes: Optional[str] = Field(None, description="Eye color or style of the model")
    hair: Optional[str] = Field(None, description="Hair color or style of the model")
    
    additional_context: Optional[str] = Field(None, description="Additional context or details to enhance the image (e.g., background, setting, atmosphere)")

class UserRequest(BaseModel):
    user_input: UserInputModel

@app.post("/generate_tryon")
async def generate_tryon(
    user_request: str = Form(...),
    reference_image: Optional[UploadFile] = File(None, description="Reference image with full body pose")
):
    """ Handle user input to generate try-on images, optionally with a reference image """
    try:
        # Parse the JSON string back into a dictionary and then into your Pydantic model
        user_request_dict = json.loads(user_request)
        user_input_model = UserInputModel(**user_request_dict["user_input"])

        refined_prompt_human = await refine_user_prompt_image(user_input_model)
        logging.debug(f"Refined human prompt in clothing: {refined_prompt_human}")

        # Check if reference image is uploaded
        if reference_image:
            # If reference image is uploaded, skip the model-related inputs
            if any([user_input_model.gender, user_input_model.ethnicity, user_input_model.age, 
                    user_input_model.body_type, user_input_model.mood]):
                raise HTTPException(status_code=400, detail="Model-related inputs are not required when a reference image is provided.")
            
            logging.debug("Reference image is provided. Skipping model-related inputs.")
            
            # Save the reference image locally (you may want to store it in cloud storage)
            reference_image_path = f"/tmp/{uuid.uuid4().hex}_{reference_image.filename}"
            with open(reference_image_path, "wb") as f:
                shutil.copyfileobj(reference_image.file, f)
            logging.debug(f"Reference image saved at: {reference_image_path}")
            
            # Generate a refined prompt for clothing and edit the reference image
            result_image_url = await generate_clothing(reference_image_path, refined_prompt_human)
            logging.debug(f"Generated image URL with reference image: {result_image_url}")
            
            # Return the result from reference image processing
            return JSONResponse({
                "generated_image_url": result_image_url,
            })

        else:
            # If no reference image is uploaded, process as usual using `generate_human_model`
            refined_prompt_human = await refine_user_prompt(user_input_model)
            logging.debug(f"Refined human prompt: {refined_prompt_human}")

            # Call the original function to generate the human model image
            human_model_image_url = await generate_human_model(refined_prompt_human)
            logging.debug(f"Generated human model image URL: {human_model_image_url}")

            return JSONResponse({
                "human_model_image_url": human_model_image_url,
            })

    except Exception as e:
        logging.error(f"Error generating try-on: {str(e)}")
        logging.error(f"Request details: {user_request}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/download_image")
async def download_image(image_url: str):
    """Serve the image directly for download."""
    try:
        # Ensure the URL starts with gs://
        if not image_url.startswith("gs://"):
            raise HTTPException(status_code=400, detail="Invalid GCS URL format. Must start with 'gs://'")

        # Extract bucket name and file path from the GCS URL
        bucket_name = image_url.split("/")[2]
        file_path = image_url.replace("gs://" + bucket_name + "/", "")

        # Fetch the blob from GCS
        blob = storage_client.bucket(bucket_name).blob(file_path)

        # Check if the blob exists
        if not blob.exists():
            raise HTTPException(status_code=404, detail="File not found in GCS")

        # Generate a unique temporary file path to avoid conflict
        temp_file_path = f"/tmp/temp_image_{uuid.uuid4().hex}.jpg"  # Unique temp filename

        # Download the file to the temporary location
        blob.download_to_filename(temp_file_path)

        # Dynamically determine MIME type based on file extension
        file_extension = os.path.splitext(file_path)[-1].lower()
        if file_extension in [".jpg", ".jpeg"]:
            media_type = 'image/jpeg'
        elif file_extension == ".png":
            media_type = 'image/png'
        elif file_extension == ".gif":
            media_type = 'image/gif'
        else:
            media_type = 'application/octet-stream'  # Default for unrecognized types

        # Return the file as a response to the user
        return FileResponse(temp_file_path, media_type=media_type, filename="generated_image" + file_extension)

    except Exception as e:
        logging.error(f"Error downloading image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading image: {str(e)}")
