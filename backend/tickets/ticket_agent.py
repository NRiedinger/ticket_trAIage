import json
from agents import Agent, Runner
from pydantic import BaseModel


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


class TicketAgent():
    def run(data):
        ticket_json_stripped = {
            "subject": data.get('subject'),
            "message": data.get('message'),
        }
        return Runner.run_sync(agent, json.dumps(ticket_json_stripped))
