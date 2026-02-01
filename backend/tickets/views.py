from .models import Ticket
from .serializers import TicketSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from agents import Agent, Runner
from pydantic import BaseModel
import json


class TicketAgentReply(BaseModel):
    category: str
    priority: str
    summary: str
    suggested_reply: str


agent_instructions = """You are a ticket assistant who helps a customer support team triage inbound messages.
Each time a support ticket is created, you take the ticket data as JSON and generate the following fields:
- category ("Billing", "Bug", "Feature", "Account", "Other")
- priority ("Low", "Medium", "High")
- summary (summarize the ticket)
- suggested_reply (suggest a reply to the ticket, the customer support team can use))"""
agent = Agent(
    name="Ticket-Assistant",
    instructions=agent_instructions,
    output_type=TicketAgentReply
)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "tickets": reverse("ticket-list", request=request, format=format),
        }
    )


class TicketViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        ticket_json_stripped = {
            "subject": self.request.data.get('subject'),
            "message": self.request.data.get('message'),
        }
        agent_result = Runner.run_sync(agent, json.dumps(ticket_json_stripped))

        serializer.save(category=agent_result.final_output.category)
        serializer.save(priority=agent_result.final_output.priority)
        serializer.save(summary=agent_result.final_output.summary)
        serializer.save(
            suggested_reply=agent_result.final_output.suggested_reply)

        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
