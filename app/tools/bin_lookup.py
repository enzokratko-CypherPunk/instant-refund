import logging

logger = logging.getLogger(__name__)
import csv
import os
from typing import Dict, Any

BIN_DATA = {}

def load_bins():
    global BIN_DATA
    if BIN_DATA:
        return
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'binlist.csv')
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bin_key = str(row.get('bin', '')).strip().zfill(6)[:6]
                if bin_key:
                    BIN_DATA[bin_key] = {
                        'bank': row.get('bank', 'Unknown'),
                        'brand': row.get('brand', 'Unknown'),
                        'type': row.get('type', 'Unknown'),
                        'country': row.get('country_code', 'Unknown'),
                        'country_name': row.get('country_name', 'Unknown'),
                        'prepaid': row.get('prepaid', 'Unknown'),
                    }
    except Exception as e:
        pass

def get_bin_details(bin_code: str) -> Dict[str, Any]:
    load_bins()
    digits = ''.join([c for c in (bin_code or '') if c.isdigit()])
    clean_bin = digits[:6]
    if len(clean_bin) < 6:
        return {'status': 'error', 'error': 'BIN must contain at least 6 digits', 'bin': clean_bin}
    if clean_bin in BIN_DATA:
        data = BIN_DATA[clean_bin]
        return {
            'status': 'success',
            'bin': clean_bin,
            'bank': data['bank'],
            'brand': data['brand'],
            'type': data['type'],
            'country': data['country'],
            'country_name': data['country_name'],
            'prepaid': data['prepaid'],
        }
    return {'status': 'not_found', 'bin': clean_bin, 'message': 'BIN not found in database'}