import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()


def parse_expense_from_text(text: str):
    text = text.lower()
    match = re.search(
        r'(\d+(?:[\.,]\d{1,2})?)\s*(reais|r\$)?\s*(em|no|na)?\s*([\w\s]+)',
        text,
    )
    if match:
        valor = float(match.group(1).replace(',', '.'))
        categoria = match.group(4).strip()
        return {'valor': valor, 'categoria': categoria}
    return None


async def parse_expense_from_image(image_file):
    API_KEY = os.getenv('OCR_SPACE_API_KEY')

    url = 'https://api.ocr.space/parse/image'
    files = {'file': (image_file.filename, await image_file.read())}
    data = {'apikey': API_KEY, 'language': 'por', 'isOverlayRequired': False}

    response = requests.post(url, files=files, data=data)
    result = response.json()

    try:
        text = result['ParsedResults'][0]['ParsedText']
        return parse_expense_from_text(text)
    except (KeyError, IndexError):
        return None
