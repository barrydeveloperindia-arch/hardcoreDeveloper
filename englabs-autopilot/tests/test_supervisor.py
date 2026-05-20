import pytest
from src.supervisor import GokuRouter, Intent

def test_goku_routes_rfq_to_cad():
    # Mocking an incoming email with a .step attachment
    email_payload = {
        "subject": "Quote for 100x Gears",
        "body": "Hi, please find attached the step file.",
        "has_attachments": True,
        "attachment_names": ["gear_complex.step"]
    }
    
    intent = GokuRouter.classify_intent(email_payload)
    assert intent == Intent.RFQ_CAD
    
    # Test routing destination
    next_node = GokuRouter.route(intent)
    assert next_node == "agent-cad-engineer"

def test_goku_routes_status_request():
    # Mocking an incoming email asking for print status
    email_payload = {
        "subject": "Status of order #1024",
        "body": "Is my print done?",
        "has_attachments": False
    }
    
    intent = GokuRouter.classify_intent(email_payload)
    assert intent == Intent.STATUS_CHECK
    
    next_node = GokuRouter.route(intent)
    assert next_node == "agent-shopfloor"
