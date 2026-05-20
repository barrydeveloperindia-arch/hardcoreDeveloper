import pytest
from src.shopfloor_worker import check_printer_status, PrinterAlert

def test_mixer_overfill_triggers_alert():
    # Mock JSON payload from HP MJF 4200 API
    mock_payload = {
        "status": "ERROR",
        "error_code": "0051-0008-0001",
        "description": "Mixer Overfill Detected by Baumer LC-001"
    }
    
    alert = check_printer_status(mock_payload)
    assert alert == PrinterAlert.CRITICAL_MIXER_OVERFILL

def test_normal_status_no_alert():
    mock_payload = {
        "status": "PRINTING",
        "error_code": None,
        "description": "Layer 1250/3000"
    }
    
    alert = check_printer_status(mock_payload)
    assert alert == PrinterAlert.OK
