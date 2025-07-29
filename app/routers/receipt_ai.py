import json
import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, File, HTTPException, UploadFile
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI

load_dotenv()

router = APIRouter()


def extract_text_from_image(file: UploadFile) -> str:
    """Extrai texto da imagem usando OCR.Space"""
    API_KEY = os.getenv('OCR_SPACE_API_KEY')

    image_bytes = file.file.read()
    response = requests.post(
        'https://api.ocr.space/parse/image',
        files={'file': (file.filename, image_bytes)},
        data={'apikey': API_KEY, 'language': 'por'},
    )

    try:
        result = response.json()
        return result['ParsedResults'][0]['ParsedText']
    except (KeyError, IndexError):
        return ''


def interpret_text_with_ai(text: str) -> dict:
    """Usa LangChain + OpenAI para interpretar o texto ou imagem do pagamento"""
    prompt = PromptTemplate.from_template(
        """
Extraia as informações do texto do comprovante Pix abaixo.

Texto do comprovante:
{text}

Retorne em formato JSON com as seguintes chaves:
- valor (float)
- data (formato dd/mm/yyyy)
- hora (formato HH:MM:SS)
- destinatario
- pagador
- banco
"""
    )

    llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
    chain = LLMChain(llm=llm, prompt=prompt)

    result = chain.run(text=text)
    return result


router = APIRouter(tags=['IA Despesas'])


@router.post('/upload-payment', summary='Processa comprovante de pagamento')
async def process_pix_receipt(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400, detail='Arquivo precisa ser uma imagem'
        )

    text = extract_text_from_image(file)
    if not text.strip():
        raise HTTPException(
            status_code=422, detail='Texto não reconhecido na imagem'
        )

    try:
        structured_data = interpret_text_with_ai(text)
        return {'dados_extraidos': json.loads(structured_data)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Erro ao interpretar: {str(e)}'
        )
