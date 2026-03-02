from typing import Dict, Any

DECLINE_CODES: Dict[str, Dict[str, str]] = {
    "00": {"meaning": "Approved", "action": "Transaction successful", "retry": "No"},
    "01": {"meaning": "Refer to Card Issuer", "action": "Customer should contact their bank", "retry": "No"},
    "02": {"meaning": "Refer to Card Issuer - Special Condition", "action": "Customer should contact their bank", "retry": "No"},
    "03": {"meaning": "Invalid Merchant", "action": "Check merchant ID configuration", "retry": "No"},
    "04": {"meaning": "Pick Up Card", "action": "Do not return card to customer. Contact issuer.", "retry": "No"},
    "05": {"meaning": "Do Not Honor", "action": "Customer should contact their bank. Most common generic decline.", "retry": "Yes - after 24 hours"},
    "06": {"meaning": "Error", "action": "Retry transaction. If persistent, contact processor.", "retry": "Yes - immediately"},
    "07": {"meaning": "Pick Up Card - Special Condition", "action": "Do not return card. Possible fraud.", "retry": "No"},
    "08": {"meaning": "Honor with ID", "action": "Verify cardholder identity and retry", "retry": "Yes - with verification"},
    "10": {"meaning": "Partial Approval", "action": "Only part of the amount was approved. Complete with another payment method.", "retry": "No"},
    "12": {"meaning": "Invalid Transaction", "action": "Check transaction type is supported by this card", "retry": "No"},
    "13": {"meaning": "Invalid Amount", "action": "Check amount formatting. Must be greater than zero.", "retry": "Yes - with corrected amount"},
    "14": {"meaning": "Invalid Card Number", "action": "Customer entered wrong card number. Re-enter.", "retry": "Yes - with correct number"},
    "15": {"meaning": "No Such Issuer", "action": "Card number does not match any known issuer", "retry": "No"},
    "19": {"meaning": "Re-enter Transaction", "action": "System error. Retry the transaction.", "retry": "Yes - immediately"},
    "21": {"meaning": "No Action Taken", "action": "Issuer could not process. Retry or use different card.", "retry": "Yes - after delay"},
    "25": {"meaning": "Unable to Locate Record", "action": "Transaction record not found. Check reference number.", "retry": "No"},
    "28": {"meaning": "File Temporarily Not Available", "action": "Issuer system down. Retry later.", "retry": "Yes - after 30 minutes"},
    "41": {"meaning": "Lost Card - Pick Up", "action": "Card reported lost. Do not return.", "retry": "No"},
    "43": {"meaning": "Stolen Card - Pick Up", "action": "Card reported stolen. Do not return.", "retry": "No"},
    "51": {"meaning": "Insufficient Funds", "action": "Customer does not have enough balance. Try smaller amount or different card.", "retry": "Yes - smaller amount or later"},
    "52": {"meaning": "No Checking Account", "action": "Card not linked to checking account", "retry": "No"},
    "53": {"meaning": "No Savings Account", "action": "Card not linked to savings account", "retry": "No"},
    "54": {"meaning": "Expired Card", "action": "Card is expired. Customer needs new card.", "retry": "No"},
    "55": {"meaning": "Incorrect PIN", "action": "Customer entered wrong PIN. Retry with correct PIN.", "retry": "Yes - with correct PIN"},
    "57": {"meaning": "Transaction Not Permitted to Cardholder", "action": "Card type not allowed for this transaction type", "retry": "No"},
    "58": {"meaning": "Transaction Not Permitted to Terminal", "action": "Terminal not configured for this transaction type", "retry": "No"},
    "59": {"meaning": "Suspected Fraud", "action": "Issuer suspects fraud. Customer must contact bank.", "retry": "No"},
    "61": {"meaning": "Exceeds Withdrawal Amount Limit", "action": "Over daily limit. Try smaller amount or wait until tomorrow.", "retry": "Yes - smaller amount or next day"},
    "62": {"meaning": "Restricted Card", "action": "Card has restrictions. Customer should contact issuer.", "retry": "No"},
    "63": {"meaning": "Security Violation", "action": "Card flagged for security. Customer must contact bank.", "retry": "No"},
    "65": {"meaning": "Exceeds Withdrawal Frequency Limit", "action": "Too many transactions today. Try again tomorrow.", "retry": "Yes - next day"},
    "70": {"meaning": "Contact Card Issuer", "action": "Generic - customer must call their bank", "retry": "No"},
    "71": {"meaning": "PIN Not Changed", "action": "PIN change request failed", "retry": "Yes - retry PIN change"},
    "75": {"meaning": "Allowable PIN Tries Exceeded", "action": "Too many wrong PIN attempts. Card may be locked.", "retry": "No"},
    "76": {"meaning": "Invalid/Nonexistent Account", "action": "Account number not valid. Verify card details.", "retry": "No"},
    "78": {"meaning": "No Account", "action": "Referenced account does not exist", "retry": "No"},
    "80": {"meaning": "Visa Transactions - Credit Issuer Unavailable", "action": "Visa network issue. Retry.", "retry": "Yes - after delay"},
    "81": {"meaning": "PIN Cryptographic Error", "action": "PIN encryption failed. Terminal issue.", "retry": "Yes - after terminal reset"},
    "82": {"meaning": "Negative CAM/dCVV/iCVV/CVV Results", "action": "Card verification failed. Possible counterfeit.", "retry": "No"},
    "85": {"meaning": "No Reason to Decline", "action": "Card verification successful (not a transaction)", "retry": "No"},
    "86": {"meaning": "Cannot Verify PIN", "action": "PIN validation not possible. Try signature instead.", "retry": "Yes - without PIN"},
    "91": {"meaning": "Authorization System Offline", "action": "Issuer system down. Retry later.", "retry": "Yes - after 15 minutes"},
    "92": {"meaning": "Unable to Route Transaction", "action": "Network routing error. Retry.", "retry": "Yes - immediately"},
    "93": {"meaning": "Transaction Cannot Be Completed - Violation of Law", "action": "Transaction violates regulations. Cannot process.", "retry": "No"},
    "94": {"meaning": "Duplicate Transmission Detected", "action": "Same transaction sent twice. Check if first went through.", "retry": "No"},
    "96": {"meaning": "System Error", "action": "Processor system error. Retry.", "retry": "Yes - immediately"},
    "N3": {"meaning": "Cash Service Not Available", "action": "Cash back not available at this terminal", "retry": "Yes - without cash back"},
    "N4": {"meaning": "Cash Back Request Exceeds Issuer Limit", "action": "Reduce cash back amount", "retry": "Yes - smaller cash back"},
    "R0": {"meaning": "Stop Recurring Payment", "action": "Customer requested to stop recurring charge. Cancel subscription.", "retry": "No"},
    "R1": {"meaning": "Revocation of Authorization for All Recurring", "action": "Customer revoked all recurring authorizations", "retry": "No"},
    "CV": {"meaning": "Card Type Verification Error", "action": "CVV/CVC mismatch. Re-enter security code.", "retry": "Yes - correct CVV"},
}

def interpret_decline_code(code: str) -> Dict[str, Any]:
    clean = code.strip().upper()

    if clean in DECLINE_CODES:
        data = DECLINE_CODES[clean]
        return {
            "status": "success",
            "code": clean,
            "meaning": data["meaning"],
            "recommended_action": data["action"],
            "retryable": data["retry"],
        }

    return {
        "status": "not_found",
        "code": clean,
        "meaning": "Unknown decline code",
        "recommended_action": "Contact payment processor for details",
        "retryable": "Unknown",
    }
