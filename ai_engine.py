# ai_engine.py
# Handles interaction with the LLM (e.g., GPT, Ollama, LocalAI)

from typing import Any

async def send_to_llm(message: str, params: dict = None) -> str:
    # Placeholder para futura integração com OpenAI, LocalAI, etc.
    response = f"LLM response to: {message}"
    return response

async def interpretar_intencao(mensagem: str) -> dict:
    mensagem = mensagem.lower()

    if "dados" in mensagem:
        return {
            "intencao": "obter_dados",
            "parametros": {}
        }
    elif "resumo" in mensagem or "resumir" in mensagem:
        return {
            "intencao": "resumo",
            "parametros": {}
        }
    else:
        # Fallback: decisão pode ser delegada ao LLM em casos futuros
        return {
            "intencao": "generico",
            "parametros": {"mensagem": mensagem}
        }
