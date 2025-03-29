# Vi-Tons Imagen

Vi-Tons Imagen is an AI-powered virtual try-on application that allows users to generate realistic human models or edit reference images with customized clothing and accessories. The application leverages Imagen 3 model and integrates with Google Cloud Storage for seamless image processing and storage.

## Features

- **Generate Human Models:** Create realistic human models based on user-provided attributes like gender, ethnicity, age, body type, and clothing preferences.
- **Reference Image Editing:** Upload a reference image to apply custom clothing and accessories.
- **Dynamic Prompt Refinement:** Refine user inputs into AI-ready prompts for generating or editing images.
- **Google Cloud Storage Integration:** Store and retrieve generated images securely using Google Cloud Storage.
- **Image Download:** Serve generated images directly for download.

## Code Repository Structure

The repository is organized as follows:

```
vi-tons_imagen/
├── app.py                     # Main FastAPI application file
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── app.yaml                   # Configuration file for Google App Engine deployment
├── .env                       # Environment variables (not included in the repo)
├── prompts/                   # Directory for prompt templates
│   └── prompt_templates.py    # Predefined templates for AI prompts
├── utils/                     # Utility functions
│   ├── helper_functions.py    # Helper functions for AI model interactions and image processing
│   ├── constants.py           # Constants and configuration variables

```

## Setup

### Prerequisites

- Python 3.8 or higher
- Google Cloud account with access to Google Cloud Storage
- Google Cloud SDK installed
- A Google Cloud Storage bucket for storing generated images

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/vi-tons_imagen.git
    cd vi-tons_imagen
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root directory and add the following variables:

    ```plaintext
    GOOGLE_PROJECT_ID=your-google-project-id
    GCP_BUCKET_NAME=your-google-cloud-storage-bucket-name
    ```

5. Authenticate with Google Cloud:

    ```bash
    gcloud auth application-default login
    ```

## Usage

### Running the Application Locally

1. Start the FastAPI server:

    ```bash
    uvicorn app:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the Swagger UI and test the API endpoints.

### API Endpoints

#### **`POST /generate_tryon`**

Generate a try-on image based on user input or a reference image.

- **Request Parameters:**
  - `user_request` (Form): JSON string containing user input attributes.
  - `reference_image` (File, optional): Reference image with a full-body pose.

- **Response:**
  - If a reference image is provided: Returns the URL of the edited image.
  - If no reference image is provided: Returns the URL of the generated human model.

#### **`GET /download_image`**

Download a generated image from Google Cloud Storage.

- **Request Parameters:**
  - `image_url` (Query): The GCS URL of the image to download.

- **Response:**
  - Returns the image file for download.

### Example Requests

#### Generate Try-On Image (Without Reference Image)

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/generate_tryon' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'user_request={
        "user_input": {
            "gender": "male",
            "ethnicity": "Indian",
            "age": "30",
            "body_type": "athletic",
            "mood": "confident",
            "style": "casual",
            "top": {"color": "yellow", "type": "t-shirt"},
            "bottom": {"color": "black", "type": "jeans"},
            "footwear": {"color": "yellow", "type": "sneakers"},
            "accessories": {"colour": black", "type": "watch"}
        }
    }'
```

#### Generate Try-On Image (With Reference Image)

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/generate_tryon' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'user_request={
        "user_input": {
            "style": "formal",
            "top": {"color": "black", "type": "blazer"},
            "bottom": {"color": "black", "type": "trousers"}
        }
    }' \
  -F 'reference_image=@path_to_your_image.jpg'
```

#### Download Image

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/download_image?image_url=gs://your-bucket-name/path-to-image.jpg' \
  -H 'accept: application/json'
```

## Deployment

### Deploying to Google App Engine

1. **Create an `app.yaml` file** in the root directory with the following content:

    ```yaml
    runtime: python39
    entrypoint: uvicorn app:app --host 0.0.0.0 --port $PORT

    env_variables:
      GOOGLE_PROJECT_ID: your-google-project-id
      GCP_BUCKET_NAME: your-google-cloud-storage-bucket-name

    handlers:
    - url: /.*
      script: auto
    ```

2. Deploy the application:

    ```bash
    gcloud app deploy
    ```

3. Access the deployed application at the URL provided by Google App Engine.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.