from typing import Dict, Any, Optional
import json

MTI_DEFINITIONS = {
    "0100": {"name": "Authorization Request", "direction": "Issuer", "category": "Authorization"},
    "0110": {"name": "Authorization Response", "direction": "Acquirer", "category": "Authorization"},
    "0120": {"name": "Authorization Advice", "direction": "Issuer", "category": "Authorization"},
    "0121": {"name": "Authorization Advice Repeat", "direction": "Issuer", "category": "Authorization"},
    "0130": {"name": "Authorization Advice Response", "direction": "Acquirer", "category": "Authorization"},
    "0200": {"name": "Financial Transaction Request", "direction": "Issuer", "category": "Financial"},
    "0210": {"name": "Financial Transaction Response", "direction": "Acquirer", "category": "Financial"},
    "0220": {"name": "Financial Transaction Advice", "direction": "Issuer", "category": "Financial"},
    "0221": {"name": "Financial Transaction Advice Repeat", "direction": "Issuer", "category": "Financial"},
    "0230": {"name": "Financial Transaction Advice Response", "direction": "Acquirer", "category": "Financial"},
    "0400": {"name": "Reversal Request", "direction": "Issuer", "category": "Reversal"},
    "0410": {"name": "Reversal Response", "direction": "Acquirer", "category": "Reversal"},
    "0420": {"name": "Reversal Advice", "direction": "Issuer", "category": "Reversal"},
    "0421": {"name": "Reversal Advice Repeat", "direction": "Issuer", "category": "Reversal"},
    "0430": {"name": "Reversal Advice Response", "direction": "Acquirer", "category": "Reversal"},
    "0600": {"name": "Administrative Request", "direction": "Issuer", "category": "Administrative"},
    "0610": {"name": "Administrative Response", "direction": "Acquirer", "category": "Administrative"},
    "0800": {"name": "Network Management Request", "direction": "Issuer", "category": "Network"},
    "0810": {"name": "Network Management Response", "direction": "Acquirer", "category": "Network"},
    "0820": {"name": "Network Management Advice", "direction": "Issuer", "category": "Network"},
}

FIELD_DEFINITIONS = {
    1:  {"name": "Secondary Bitmap", "type": "b", "length": 8},
    2:  {"name": "Primary Account Number (PAN)", "type": "llvar", "max": 19},
    3:  {"name": "Processing Code", "type": "fixed", "length": 6},
    4:  {"name": "Transaction Amount", "type": "fixed", "length": 12},
    5:  {"name": "Settlement Amount", "type": "fixed", "length": 12},
    6:  {"name": "Cardholder Billing Amount", "type": "fixed", "length": 12},
    7:  {"name": "Transmission Date and Time", "type": "fixed", "length": 10},
    8:  {"name": "Cardholder Billing Fee Amount", "type": "fixed", "length": 8},
    9:  {"name": "Settlement Conversion Rate", "type": "fixed", "length": 8},
    10: {"name": "Cardholder Billing Conversion Rate", "type": "fixed", "length": 8},
    11: {"name": "Systems Trace Audit Number (STAN)", "type": "fixed", "length": 6},
    12: {"name": "Local Transaction Time", "type": "fixed", "length": 6},
    13: {"name": "Local Transaction Date", "type": "fixed", "length": 4},
    14: {"name": "Expiration Date", "type": "fixed", "length": 4},
    15: {"name": "Settlement Date", "type": "fixed", "length": 4},
    16: {"name": "Currency Conversion Date", "type": "fixed", "length": 4},
    17: {"name": "Capture Date", "type": "fixed", "length": 4},
    18: {"name": "Merchant Type (MCC)", "type": "fixed", "length": 4},
    19: {"name": "Acquiring Institution Country Code", "type": "fixed", "length": 3},
    20: {"name": "PAN Extended Country Code", "type": "fixed", "length": 3},
    21: {"name": "Forwarding Institution Country Code", "type": "fixed", "length": 3},
    22: {"name": "POS Entry Mode", "type": "fixed", "length": 3},
    23: {"name": "Card Sequence Number", "type": "fixed", "length": 3},
    24: {"name": "Function Code / NII", "type": "fixed", "length": 3},
    25: {"name": "POS Condition Code", "type": "fixed", "length": 2},
    26: {"name": "POS PIN Capture Code", "type": "fixed", "length": 2},
    27: {"name": "Authorization ID Response Length", "type": "fixed", "length": 1},
    28: {"name": "Transaction Fee Amount", "type": "fixed", "length": 9},
    29: {"name": "Settlement Fee Amount", "type": "fixed", "length": 9},
    30: {"name": "Transaction Processing Fee Amount", "type": "fixed", "length": 9},
    31: {"name": "Settlement Processing Fee Amount", "type": "fixed", "length": 9},
    32: {"name": "Acquiring Institution ID Code", "type": "llvar", "max": 11},
    33: {"name": "Forwarding Institution ID Code", "type": "llvar", "max": 11},
    34: {"name": "PAN Extended", "type": "llvar", "max": 28},
    35: {"name": "Track 2 Data", "type": "llvar", "max": 37},
    36: {"name": "Track 3 Data", "type": "lllvar", "max": 104},
    37: {"name": "Retrieval Reference Number", "type": "fixed", "length": 12},
    38: {"name": "Authorization ID Response (Approval Code)", "type": "fixed", "length": 6},
    39: {"name": "Response Code", "type": "fixed", "length": 2},
    40: {"name": "Service Restriction Code", "type": "fixed", "length": 3},
    41: {"name": "Card Acceptor Terminal ID", "type": "fixed", "length": 8},
    42: {"name": "Card Acceptor ID Code", "type": "fixed", "length": 15},
    43: {"name": "Card Acceptor Name/Location", "type": "fixed", "length": 40},
    44: {"name": "Additional Response Data", "type": "llvar", "max": 25},
    45: {"name": "Track 1 Data", "type": "llvar", "max": 76},
    46: {"name": "Additional Data ISO", "type": "lllvar", "max": 999},
    47: {"name": "Additional Data National", "type": "lllvar", "max": 999},
    48: {"name": "Additional Data Private", "type": "lllvar", "max": 999},
    49: {"name": "Transaction Currency Code", "type": "fixed", "length": 3},
    50: {"name": "Settlement Currency Code", "type": "fixed", "length": 3},
    51: {"name": "Cardholder Billing Currency Code", "type": "fixed", "length": 3},
    52: {"name": "PIN Data", "type": "fixed", "length": 8},
    53: {"name": "Security Related Control Information", "type": "fixed", "length": 16},
    54: {"name": "Additional Amounts", "type": "lllvar", "max": 120},
    55: {"name": "ICC Data (EMV)", "type": "lllvar", "max": 999},
    56: {"name": "Reserved ISO", "type": "lllvar", "max": 999},
    57: {"name": "Reserved National", "type": "lllvar", "max": 999},
    58: {"name": "Reserved National", "type": "lllvar", "max": 999},
    59: {"name": "Reserved National", "type": "lllvar", "max": 999},
    60: {"name": "Reserved Private", "type": "lllvar", "max": 999},
    61: {"name": "Reserved Private", "type": "lllvar", "max": 999},
    62: {"name": "Reserved Private", "type": "lllvar", "max": 999},
    63: {"name": "Reserved Private", "type": "lllvar", "max": 999},
    64: {"name": "Message Authentication Code (MAC)", "type": "fixed", "length": 8},
    90: {"name": "Original Data Elements", "type": "fixed", "length": 42},
    95: {"name": "Replacement Amounts", "type": "fixed", "length": 42},
    102: {"name": "Account Identification 1", "type": "llvar", "max": 28},
    103: {"name": "Account Identification 2", "type": "llvar", "max": 28},
}

PROCESSING_CODE_MAP = {
    "00": "Purchase", "01": "Withdrawal (ATM)", "09": "Purchase with Cashback",
    "20": "Credit/Refund", "28": "Load Prepaid", "30": "Balance Inquiry",
    "31": "Balance Inquiry (ATM)", "38": "PIN Change", "40": "Transfer",
    "50": "Payment", "90": "Ministatement", "99": "Administrative",
}

RESPONSE_CODE_MAP = {
    "00": "Approved", "01": "Refer to Card Issuer", "02": "Refer to Card Issuer (Special)",
    "03": "Invalid Merchant", "04": "Pick Up Card", "05": "Do Not Honor",
    "06": "Error", "07": "Pick Up Card (Special)", "08": "Honor with ID",
    "10": "Partial Approval", "12": "Invalid Transaction", "13": "Invalid Amount",
    "14": "Invalid Card Number", "15": "No Such Issuer", "19": "Re-enter Transaction",
    "21": "No Action Taken", "25": "Unable to Locate Record", "28": "File Temporarily Unavailable",
    "30": "Format Error", "33": "Expired Card", "34": "Suspected Fraud",
    "36": "Restricted Card", "37": "Call Issuer Security", "38": "PIN Tries Exceeded",
    "39": "No Credit Account", "40": "Function Not Supported", "41": "Lost Card",
    "42": "No Universal Account", "43": "Stolen Card", "51": "Insufficient Funds",
    "52": "No Checking Account", "53": "No Savings Account", "54": "Expired Card",
    "55": "Incorrect PIN", "57": "Transaction Not Permitted to Cardholder",
    "58": "Transaction Not Permitted to Terminal", "59": "Suspected Fraud",
    "61": "Exceeds Withdrawal Amount Limit", "62": "Restricted Card",
    "63": "Security Violation", "65": "Exceeds Withdrawal Frequency Limit",
    "68": "Response Received Too Late", "75": "PIN Tries Exceeded",
    "76": "Invalid/Nonexistent Account", "77": "Invalid/Nonexistent Account",
    "78": "No Account", "80": "Invalid Date", "85": "No Reason to Decline",
    "91": "Issuer Unavailable", "92": "Unable to Route", "93": "Cannot Complete",
    "94": "Duplicate Transmission", "96": "System Malfunction",
}

POS_ENTRY_MODE_MAP = {
    "010": "Manual (No Terminal)", "011": "Manual (MOTO)", "020": "Magnetic Stripe Read",
    "021": "Magnetic Stripe (Unverified)", "022": "Magnetic Stripe (Verified)",
    "051": "ICC (Chip) Read", "071": "Contactless (EMV)", "075": "Contactless (Magnetic Stripe)",
    "081": "e-Commerce", "082": "Contactless (NFC)", "090": "Magnetic Stripe (Full Track)",
    "091": "Contactless Magnetic Stripe", "101": "Credential on File",
}

def _parse_bitmap(bitmap_hex: str) -> list:
    bits = []
    for char in bitmap_hex:
        val = int(char, 16)
        for i in range(3, -1, -1):
            bits.append((val >> i) & 1)
    return bits

def _parse_fields(data: str, fields_present: list) -> Dict:
    pos = 0
    parsed = {}
    for field_num in fields_present:
        if field_num == 1:
            continue
        if field_num not in FIELD_DEFINITIONS:
            parsed[field_num] = {"name": f"Field {field_num}", "value": "Unknown field", "raw": ""}
            continue
        defn = FIELD_DEFINITIONS[field_num]
        try:
            if defn["type"] == "fixed":
                length = defn["length"]
                value = data[pos:pos+length]
                pos += length
            elif defn["type"] == "llvar":
                length = int(data[pos:pos+2])
                pos += 2
                value = data[pos:pos+length]
                pos += length
            elif defn["type"] == "lllvar":
                length = int(data[pos:pos+3])
                pos += 3
                value = data[pos:pos+length]
                pos += length
            elif defn["type"] == "b":
                value = data[pos:pos+16]
                pos += 16
            else:
                value = ""
            parsed[field_num] = {"name": defn["name"], "value": value.strip()}
        except Exception:
            parsed[field_num] = {"name": defn["name"], "value": "parse_error"}
    return parsed

def _enrich_fields(fields: Dict) -> Dict:
    enriched = {}
    for k, v in fields.items():
        entry = dict(v)
        val = entry.get("value", "")
        if k == 3 and len(val) == 6:
            txn_type = val[:2]
            entry["transaction_type"] = PROCESSING_CODE_MAP.get(txn_type, f"Unknown ({txn_type})")
            entry["from_account"] = val[2:4]
            entry["to_account"] = val[4:6]
        elif k == 39:
            entry["meaning"] = RESPONSE_CODE_MAP.get(val, f"Unknown ({val})")
        elif k == 22:
            entry["meaning"] = POS_ENTRY_MODE_MAP.get(val, f"Unknown ({val})")
        elif k == 4 and val:
            try:
                entry["formatted"] = f"{int(val) / 100:.2f}"
            except Exception:
                pass
        elif k == 14 and len(val) == 4:
            entry["formatted"] = f"20{val[:2]}/{val[2:]}"
        elif k == 7 and len(val) == 10:
            entry["formatted"] = f"Month:{val[:2]} Day:{val[2:4]} Time:{val[4:6]}:{val[6:8]}:{val[8:10]}"
        enriched[str(k)] = entry
    return enriched

def parse_iso8583(message: str) -> Dict[str, Any]:
    msg = message.strip().replace(" ", "").upper()

    if len(msg) < 20:
        return {"status": "error", "error": "Message too short to be a valid ISO 8583 message"}

    mti = msg[:4]
    if not mti.isdigit():
        return {"status": "error", "error": f"Invalid MTI: {mti}. Must be 4 digits."}

    mti_info = MTI_DEFINITIONS.get(mti, {"name": "Unknown MTI", "direction": "Unknown", "category": "Unknown"})

    bitmap_hex = msg[4:20]
    try:
        bits = _parse_bitmap(bitmap_hex)
    except Exception:
        return {"status": "error", "error": f"Invalid primary bitmap: {bitmap_hex}"}

    has_secondary = bits[0] == 1
    data_start = 20

    if has_secondary:
        secondary_hex = msg[20:36]
        try:
            secondary_bits = _parse_bitmap(secondary_hex)
            bits = bits + secondary_bits
            data_start = 36
        except Exception:
            return {"status": "error", "error": f"Invalid secondary bitmap: {secondary_hex}"}

    fields_present = [i+1 for i, b in enumerate(bits) if b == 1]
    raw_data = msg[data_start:]
    parsed_fields = _parse_fields(raw_data, fields_present)
    enriched_fields = _enrich_fields(parsed_fields)

    return {
        "status": "success",
        "mti": mti,
        "mti_name": mti_info["name"],
        "mti_direction": mti_info["direction"],
        "mti_category": mti_info["category"],
        "has_secondary_bitmap": has_secondary,
        "fields_present": fields_present,
        "field_count": len(fields_present),
        "fields": enriched_fields
    }
