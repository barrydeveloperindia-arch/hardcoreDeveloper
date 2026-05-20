from enum import Enum

class Intent(Enum):
    RFQ_CAD = 1
    STATUS_CHECK = 2
    SPAM = 3
    UNKNOWN = 4

class GokuRouter:
    @staticmethod
    def classify_intent(email_payload: dict) -> Intent:
        """
        Mock AI Intent Classification. 
        In production, this wraps Gemini 2.5 Flash via LangGraph.
        """
        attachments = email_payload.get("attachment_names", [])
        if any(f.endswith(".step") or f.endswith(".stl") for f in attachments):
            return Intent.RFQ_CAD
            
        subject_body = email_payload.get("subject", "").lower() + email_payload.get("body", "").lower()
        if "status" in subject_body or "done" in subject_body:
            return Intent.STATUS_CHECK
            
        return Intent.UNKNOWN

    @staticmethod
    def route(intent: Intent) -> str:
        """
        Determines the next agent/node in the LangGraph workflow.
        """
        routing_table = {
            Intent.RFQ_CAD: "agent-cad-engineer",
            Intent.STATUS_CHECK: "agent-shopfloor"
        }
        return routing_table.get(intent, "human-fallback")
