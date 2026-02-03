from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from tickets.models import Ticket
from tickets.serializers import TicketSerializer


class TicketSerializerTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.ticket = Ticket.objects.create(
            subject="Zu Hilfe!",
            from_email="theo.tester@test.com",
            message="Bin in einem Testlabor gefangen!"
        )
        self.request = self.factory.get("/")

    def test_serializer_output_fields(self):
        serializer = TicketSerializer(instance=self.ticket, context={
                                      "request": self.request})

        data = serializer.data
        expected_fields = {
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
        }

        self.assertEqual(set(data.keys()), expected_fields)

    def test_default_fields_are_serialized(self):
        serializer = TicketSerializer(instance=self.ticket, context={
                                      "request": self.request})

        data = serializer.data
        self.assertEqual(data["category"], Ticket.Category.OTHER)
        self.assertEqual(data["priority"], Ticket.Priority.MEDIUM)
        self.assertEqual(data["summary"], "")
        self.assertEqual(data["suggested_reply"], "")
        self.assertIsNone(data["feedback_accepted"])

    def test_serializer_accepts_valid_inpput(self):
        serializer = TicketSerializer(
            data={
                "subject": "Zu Hilfe!",
                "from_email": "theo.tester@test.com",
                "message": "Bin in einem Testlabor gefangen!"
            },
            context={"request", self.request}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        ticket = serializer.save()

        self.assertEqual(ticket.subject, "Zu Hilfe!")
        self.assertEqual(ticket.from_email, "theo.tester@test.com")
        self.assertEqual(ticket.message, "Bin in einem Testlabor gefangen!")

    def test_missing_required_fields(self):
        serializer = TicketSerializer(
            data={"subject": "Zu Hilfe!"},
            context={"request": self.request}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("from_email", serializer.errors)
        self.assertIn("message", serializer.errors)
