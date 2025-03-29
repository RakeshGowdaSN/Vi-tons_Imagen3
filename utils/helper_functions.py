import logging
from utils.models import generate_image_with_imagen, generate_clothing_with_imagen
from utils.prompt_templates import generate_refined_prompt, generate_refined_prompt_for_image
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.DEBUG)

async def refine_user_prompt(user_input):
    """ Refine the user input prompt to improve results from the AI models """
    # Use a template-based approach to generate more specific prompts for AI models
    refined_prompt = generate_refined_prompt(user_input)
    logging.debug(f"Refined prompt: {refined_prompt}")
    return refined_prompt

async def refine_user_prompt_image(user_input):
    """ Refine the user input prompt to improve results from the AI models """
    # Use a template-based approach to generate more specific prompts for AI models
    refined_prompt = generate_refined_prompt_for_image(user_input)
    logging.debug(f"Refined prompt: {refined_prompt}")
    return refined_prompt

async def generate_human_model(refined_prompt: str):
    """ Generate a human model image based on refined prompt using Google Imagen """
    try:
        human_model_image_url = await generate_image_with_imagen(refined_prompt)
        return human_model_image_url
    except Exception as e:
        logging.error(f"Error generating human model: {str(e)}")
        raise Exception(f"Failed to generate human model image: {str(e)}")

async def generate_clothing(reference_image_path: str, refine_user_prompt_image: str):
    """ Generate clothing for the human model using refined prompt and Google Imagen """
    try:
        # refined_prompt = generate_refined_prompt_for_image(user_input,reference_image_path)
        clothing_image_url = await generate_clothing_with_imagen(reference_image_path, refine_user_prompt_image)
        return clothing_image_url
    except Exception as e:
        logging.error(f"Error generating clothing: {str(e)}")
        raise Exception(f"Failed to generate clothing image: {str(e)}")