import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class CloudinaryUploader:
    """
    Helper class for uploading files to Cloudinary
    """

    def __init__(self):
        # Cloudinary is already configured in settings.py
        pass

    def upload_file(self, file, folder="", resource_type="auto"):
        """
        Upload file to Cloudinary

        Args:
            file: File object to upload
            folder: Folder name in Cloudinary (optional)
            resource_type: Type of resource (auto, image, video, raw)

        Returns:
            str: URL of uploaded file or None if failed
        """
        try:
            upload_options = {
                'resource_type': resource_type,
                'use_filename': True,
                'unique_filename': True,
                'overwrite': False
            }

            if folder:
                upload_options['folder'] = folder

            result = cloudinary.uploader.upload(file, **upload_options)

            logger.info(f"File uploaded successfully to Cloudinary: {result.get('secure_url')}")
            return result.get('secure_url')

        except Exception as e:
            logger.error(f"Error uploading file to Cloudinary: {e}")
            return None

    def upload_audio(self, file, folder="audio"):
        """Upload audio file to Cloudinary"""
        return self.upload_file(file, folder=folder, resource_type="auto")

    def upload_video(self, file, folder="video"):
        """Upload video file to Cloudinary"""
        return self.upload_file(file, folder=folder, resource_type="video")

    def upload_image(self, file, folder="images"):
        """Upload image file to Cloudinary"""
        return self.upload_file(file, folder=folder, resource_type="image")

    def delete_file(self, url_or_public_id, resource_type="auto"):
        """
        Delete file from Cloudinary

        Args:
            url_or_public_id: URL or public_id of the file
            resource_type: Type of resource (auto, image, video, raw)

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            # If it's a URL, extract public_id
            if url_or_public_id.startswith('http'):
                public_id = self.extract_public_id_from_url(url_or_public_id)
            else:
                public_id = url_or_public_id

            if not public_id:
                return False

            result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)

            if result.get('result') == 'ok':
                logger.info(f"File deleted successfully from Cloudinary: {public_id}")
                return True
            else:
                logger.warning(f"File not found or already deleted: {public_id}")
                return False

        except Exception as e:
            logger.error(f"Error deleting file from Cloudinary: {e}")
            return False

    def extract_public_id_from_url(self, url):
        """
        Extract public_id from Cloudinary URL

        Args:
            url: Cloudinary URL

        Returns:
            str: public_id or None if extraction failed
        """
        try:
            if not url or 'cloudinary.com' not in url:
                return None

            # Cloudinary URL format:
            # https://res.cloudinary.com/{cloud_name}/{resource_type}/upload/{transformations}/{public_id}.{format}
            parts = url.split('/')

            # Find the upload part
            upload_index = -1
            for i, part in enumerate(parts):
                if part == 'upload':
                    upload_index = i
                    break

            if upload_index == -1 or upload_index >= len(parts) - 1:
                return None

            # Get public_id (could have folder structure)
            public_id_parts = parts[upload_index + 1:]

            # Remove transformations (starts with v1234567890 or similar)
            if public_id_parts and public_id_parts[0].startswith('v') and public_id_parts[0][1:].isdigit():
                public_id_parts = public_id_parts[1:]

            if not public_id_parts:
                return None

            # Join back and remove file extension
            public_id = '/'.join(public_id_parts)
            if '.' in public_id:
                public_id = public_id.rsplit('.', 1)[0]

            return public_id

        except Exception as e:
            logger.error(f"Error extracting public_id from URL {url}: {e}")
            return None

    def get_file_info(self, public_id, resource_type="auto"):
        """
        Get information about a file from Cloudinary

        Args:
            public_id: Public ID of the file
            resource_type: Type of resource

        Returns:
            dict: File information or None if not found
        """
        try:
            result = cloudinary.api.resource(public_id, resource_type=resource_type)
            return result
        except Exception as e:
            logger.error(f"Error getting file info from Cloudinary: {e}")
            return None