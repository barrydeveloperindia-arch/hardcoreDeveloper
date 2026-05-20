from enum import Enum

class PrinterAlert(Enum):
    OK = 1
    CRITICAL_MIXER_OVERFILL = 2
    UNKNOWN_ERROR = 3

def check_printer_status(payload: dict) -> PrinterAlert:
    """
    Parses HP MJF 4200 local API payload and flags critical errors.
    """
    if payload.get("status") == "ERROR":
        error_code = payload.get("error_code")
        description = payload.get("description")
        
        if (error_code and "0051-0008-0001" in error_code) or \
           (description and "Mixer Overfill" in description):
            return PrinterAlert.CRITICAL_MIXER_OVERFILL
        return PrinterAlert.UNKNOWN_ERROR
    return PrinterAlert.OK
