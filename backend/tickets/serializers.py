from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "url",
            "id",
            "subject",
            "from_email",
            "message",
            "created_at",
            "category",
            "priority",
            "summary",
            "suggested_reply",
            "feedback_accepted",
        ]
