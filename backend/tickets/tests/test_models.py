from django.test import TestCase
from django.utils import timezone

from tickets.models import Ticket


class TicketModelTests(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            subject="Zu Hilfe!",
            from_email="theo.tester@test.com",
            message="Bin in einem Testlabor gefangen!"
        )

    def test_ticket_is_created(self):
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(self.ticket.subject, "Zu Hilfe!")
        self.assertEqual(self.ticket.from_email, "theo.tester@test.com")
        self.assertEqual(self.ticket.message,
                         "Bin in einem Testlabor gefangen!")

    def test_default_category(self):
        self.assertEqual(self.ticket.category, Ticket.Category.OTHER)

    def test_default_priority(self):
        self.assertEqual(self.ticket.priority, Ticket.Priority.MEDIUM)

    def test_default_blank_fields(self):
        self.assertEqual(self.ticket.summary, "")
        self.assertEqual(self.ticket.suggested_reply, "")
        self.assertIsNone(self.ticket.feedback_accepted)

    def test_created_at(self):
        self.assertIsNotNone(self.ticket.created_at)
        self.assertLessEqual(self.ticket.created_at, timezone.now())
