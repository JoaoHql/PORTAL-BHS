# tasks.py

from typing import Any
from ai_engine import send_to_llm

async def process_message(message: str, user_id: Any = None):
    # Essa função pode ser usada para fallback ou lógica genérica
    response = await send_to_llm(message)
    return response

async def obter_dados(params: dict) -> str:
    # Lógica real pode consultar um banco, API ou cache
    return "Aqui estão os dados solicitados."

async def gerar_resumo(params: dict) -> str:
    # Pode usar o LLM ou lógica local
    return "Este é um resumo gerado da sua solicitação."
