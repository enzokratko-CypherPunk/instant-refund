from typing import Dict, Any
import httpx

CURRENCY_PRECISION: Dict[str, int] = {
    "BHD": 3, "IQD": 3, "JOD": 3, "KWD": 3, "LYD": 3, "OMR": 3, "TND": 3,
    "CLF": 4, "UYW": 4,
    "JPY": 0, "KRW": 0, "VND": 0, "IDR": 0, "HUF": 0, "ISK": 0, "PYG": 0, "RWF": 0, "UGX": 0,
}

CURRENCY_NAMES: Dict[str, str] = {
    "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound", "JPY": "Japanese Yen",
    "CAD": "Canadian Dollar", "AUD": "Australian Dollar", "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan", "HKD": "Hong Kong Dollar", "NZD": "New Zealand Dollar",
    "SEK": "Swedish Krona", "NOK": "Norwegian Krone", "DKK": "Danish Krone",
    "SGD": "Singapore Dollar", "MXN": "Mexican Peso", "BRL": "Brazilian Real",
    "INR": "Indian Rupee", "ZAR": "South African Rand", "AED": "UAE Dirham",
    "SAR": "Saudi Riyal", "KRW": "South Korean Won", "TRY": "Turkish Lira",
    "PLN": "Polish Zloty", "THB": "Thai Baht", "IDR": "Indonesian Rupiah",
    "HUF": "Hungarian Forint", "CZK": "Czech Koruna", "ILS": "Israeli Shekel",
    "MYR": "Malaysian Ringgit", "PHP": "Philippine Peso", "RON": "Romanian Leu",
    "CLP": "Chilean Peso", "ARS": "Argentine Peso", "COP": "Colombian Peso",
    "EGP": "Egyptian Pound", "NGN": "Nigerian Naira", "PKR": "Pakistani Rupee",
    "VND": "Vietnamese Dong", "BDT": "Bangladeshi Taka", "UAH": "Ukrainian Hryvnia",
    "KWD": "Kuwaiti Dinar", "QAR": "Qatari Riyal", "OMR": "Omani Rial",
    "JOD": "Jordanian Dinar", "BHD": "Bahraini Dinar",
}

async def convert_currency(from_currency: str, to_currency: str, amount: float) -> Dict[str, Any]:
    frm = from_currency.strip().upper()
    to = to_currency.strip().upper()

    if frm not in CURRENCY_NAMES:
        return {"status": "error", "error": f"Unknown currency: {frm}"}
    if to not in CURRENCY_NAMES:
        return {"status": "error", "error": f"Unknown currency: {to}"}
    if amount <= 0:
        return {"status": "error", "error": "Amount must be greater than zero"}

    url = f"https://open.er-api.com/v6/latest/{frm}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10)
        data = resp.json()

    if data.get("result") != "success":
        return {"status": "error", "error": "Exchange rate service unavailable"}

    if to not in data["rates"]:
        return {"status": "error", "error": f"Rate not available for {to}"}

    rate = data["rates"][to]
    precision = CURRENCY_PRECISION.get(to, 2)
    converted = round(amount * rate, precision)

    return {
        "status": "success",
        "from_currency": frm,
        "from_currency_name": CURRENCY_NAMES[frm],
        "to_currency": to,
        "to_currency_name": CURRENCY_NAMES[to],
        "amount": amount,
        "converted_amount": converted,
        "exchange_rate": rate,
        "precision_decimals": precision,
    }
