from imagekitio import ImageKit
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
URL_ENDPOINT = os.getenv("URL_ENDPOINT")

imagekit = ImageKit(
    private_key=PRIVATE_KEY,
    public_key=PUBLIC_KEY,
    url_endpoint=URL_ENDPOINT,
)


def upload_image(filepath, filename):
    upload_status = imagekit.upload_file(
        file=open(filepath, "rb"),  # required
        file_name=filename,  # required
    )
    return upload_status


def purge_image(image_id):
    purge_status = imagekit.delete_file(image_id)
    return purge_status
