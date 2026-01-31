from rest_framework import serializers
from .models import ContactUs, Review
from utils.forget_email import send_mail_for_support, thanks_mail_for_getting_support
import logging
from threading import Thread

logger = logging.getLogger(__name__)

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'reviewer', 'reviewer_name', 'rating', 'comment', 'date']

    def get_reviewer_name(self, obj):
        user = getattr(obj, 'reviewer', None)
        if not user:
            return ""
        try:
            full = user.account.get_name()
        except Exception:
            full = None
        if full:
            return full
        name = getattr(user.account, 'name') or ''
        if name:
            return name.strip()
        return getattr(user, 'name', None) or getattr(user, 'email', '') or ''



class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def _send_emails_async(self, subject, message, name, email):
        try:
            send_mail_for_support(subject_=subject, message=message, name=name, email=email)
            thanks_mail_for_getting_support(subject_    =subject, name=name, email=email)
        except Exception:
            logger.exception("Failed to send contact-us emails for %s <%s>", name, email)

    def create(self, validated_data):
        instance = super().create(validated_data)

        subject = validated_data['subject']
        message = validated_data['message']
        name = validated_data['name']
        email = validated_data['email']

        Thread(target=self._send_emails_async, args=(subject, message, name, email), daemon=True).start()

        return instance

