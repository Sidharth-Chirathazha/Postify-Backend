import cloudinary
import cloudinary.uploader
import time
from django.conf import settings
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_upload_signature(request):
    timestamp = int(time.time())
    params_to_sign = {
        'timestamp': timestamp,
        'upload_preset': 'postify_uploads',
    }
    signature = cloudinary.utils.api_sign_request(params_to_sign, settings.CLOUDINARY_API_SECRET)

    return Response({
        'signature': signature,
        'timestamp': timestamp,
        'api_key': settings.CLOUDINARY_API_KEY,
        'cloud_name': settings.CLOUDINARY_CLOUD_NAME,
        'upload_preset': 'postify_uploads',
    })