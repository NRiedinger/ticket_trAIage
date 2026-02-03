from .models import Ticket
from .serializers import TicketSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from .ticket_agent import TicketAgent


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "tickets": reverse("ticket-list", request=request, format=format),
        }
    )


class TicketViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        agent_result = TicketAgent.run(self.request.data)

        serializer.save(category=agent_result.final_output.category)
        serializer.save(priority=agent_result.final_output.priority)
        serializer.save(summary=agent_result.final_output.summary)
        serializer.save(
            suggested_reply=agent_result.final_output.suggested_reply)
