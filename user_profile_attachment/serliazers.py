from rest_framework import serializers

from user_profile_attachment.models import UserProfileAttachment

class UserProfileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileAttachment
        fields = '__all__'