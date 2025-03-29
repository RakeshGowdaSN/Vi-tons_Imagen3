def generate_refined_prompt(user_input):
    # Start building the refined description based on the user's input
    prompt = f"Create a high-fashion image of {user_input.gender if user_input.gender else 'a model'}, "

    if user_input.ethnicity:
        prompt += f"with {user_input.ethnicity} features, "
    if user_input.age:
        prompt += f"in their {user_input.age} years, "
    if user_input.body_type:
        prompt += f"with a {user_input.body_type} build. "
    else:
        prompt += "with an elegant build. "

    if user_input.mood:
        prompt += f"The model should be styled with {user_input.mood} expressions and "
    else:
        prompt += "The model should exude confidence and grace, "

    # Style and occasion
    if user_input.style:
        prompt += f"with a {user_input.style} fashion sense. "
    if user_input.occasion:
        prompt += f"The background should be realistic and sophisticated, matching the occasion of {user_input.occasion}. "
    else:
        prompt += "The background should be an elegant, neutral setting. "

    # Full-body pose description
    prompt += "The model should be posed in a front-facing full-body stance, showcasing the outfit from head to toe, with a natural, confident posture. "

    # Add clothing details if provided
    if user_input.top:
        prompt += f"The model is wearing a {user_input.top.color} {user_input.top.type} top, with refined details and high-quality fabric. "
    if user_input.bottom:
        prompt += f"Paired with {user_input.bottom.color} {user_input.bottom.type} bottoms that emphasize both comfort and luxury. "
    if user_input.accessories:
        prompt += f"Complete the look with {user_input.accessories.color} {user_input.accessories.type} accessories, adding an extra touch of elegance. "
    if user_input.footwear:
        prompt += f"The footwear is {user_input.footwear.color} and {user_input.footwear.type}, designed to complement the outfit's overall aesthetic. "

    # Model's appearance (eyes, hair)
    if user_input.eyes:
        prompt += f"The model's eyes are {user_input.eyes}, "
    if user_input.hair:
        prompt += f"and their hair is styled in a {user_input.hair} fashion."

    # Optionally add user custom prompt if available
    if user_input.additional_context:
        prompt += f"\n\nAdditional details: {user_input.additional_context}"

    return prompt

def generate_refined_prompt_for_image(user_input):
    """Generates a refined prompt for modifying clothing in a reference image while preserving the model's identity."""
    prompt = (
        "Modify the clothing of the person in the provided reference image. "
        "Keep the person's face, hair, body shape, pose, and overall appearance exactly the same. "
        "Only change the clothing items as described below: "
    )

    if user_input.top:
        prompt += f"Change the top to a {user_input.top.color} {user_input.top.type}. "
    if user_input.bottom:
        prompt += f"Change the bottoms to {user_input.bottom.color} {user_input.bottom.type}. "
    if user_input.accessories:
        prompt += f"Add {user_input.accessories.color} {user_input.accessories.type} accessories. "
    if user_input.footwear:
        prompt += f"Change the footwear to {user_input.footwear.color} {user_input.footwear.type}. "

    return prompt
