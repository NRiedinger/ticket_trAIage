from unittest.mock import patch, Mock
from django.http import QueryDict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tickets.models import Ticket


class ApiRootTests(APITestCase):
    def test_api_root(self):
        url = reverse("api-root")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tickets", response.data)


def mock_agent_response():
    final_output = Mock()
    final_output.category = Ticket.Category.BUG
    final_output.priority = Ticket.Priority.MEDIUM
    final_output.summary = "This is a mocked summary of the subject and message"
    final_output.suggested_reply = "This is a mocked suggested reply."

    result = Mock()
    result.final_output = final_output
    return result


class TicketViewSetTests(APITestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            subject="Zu Hilfe!",
            from_email="theo.tester@test.com",
            message="Bin in einem Testlabor gefangen!"
        )
        self.tickets_url = reverse("ticket-list")

    def test_list_tickets(self):
        response = self.client.get(self.tickets_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["subject"], self.ticket.subject)
        self.assertEqual(
            response.data[0]["from_email"], self.ticket.from_email)
        self.assertEqual(response.data[0]["message"], self.ticket.message)

    @patch("tickets.views.TicketAgent.run")
    def test_create_ticket_with_agent_mock(self, mock_run):
        mock_run.return_value = mock_agent_response()

        data = {
            "subject": "Zu Hilfe!",
            "from_email": "theo.tester@test.com",
            "message": "Bin in einem Testlabor gefangen!"
        }
        data_qd = QueryDict("", mutable=True)
        data_qd.update(data)

        response = self.client.post(self.tickets_url, data_qd)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 2)

        ticket = Ticket.objects.latest("id")

        mock_run.assert_called_once_with(data_qd)

        self.assertEqual(ticket.category, Ticket.Category.BUG)
        self.assertEqual(ticket.priority, Ticket.Priority.MEDIUM)
        self.assertEqual(
            ticket.summary, "This is a mocked summary of the subject and message")
        self.assertEqual(ticket.suggested_reply,
                         "This is a mocked suggested reply.")

    def test_retrieve_ticket(self):
        url = reverse("ticket-detail", args=[self.ticket.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["subject"], self.ticket.subject)

    def test_update_ticket(self):
        url = reverse("ticket-detail", args=[self.ticket.id])

        response = self.client.patch(url, {"subject": "updated subject"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.subject, "updated subject")

    def test_delete_ticket(self):
        url = reverse("ticket-detail", args=[self.ticket.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ticket.objects.count(), 0)
