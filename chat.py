from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp
import os
from typing import Dict, List, Any
import uvicorn
# --- CONFIGURAÇÃO ---
# É uma boa prática carregar chaves de variáveis de ambiente.
# Por agora, vamos deixar aqui, mas lembre-se de proteger sua chave.
OPENAI_API_KEY = "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" # Substitua pela sua chave real
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "BMG.csv")

# --- INICIALIZAÇÃO DA API ---
app = FastAPI(
    title="Chatbot API",
    description="API para o chatbot do Portal BHS",
    version="1.0.0"
)

# Adiciona o CORS Middleware. Isso é ESSENCIAL para permitir que seu
# site (frontend) se comunique com esta API (backend).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para o domínio do seu site
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# --- FUNÇÃO PRINCIPAL DA OPENAI (Reutilizada do seu código) ---
async def consultar_chatgpt_com_contexto(mensagens: List[Dict[str, str]]) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4-turbo",
        "messages": mensagens,
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    print(f"Erro da API OpenAI: {error_text}")
                    return "Desculpe, ocorreu um erro ao processar sua solicitação."
                
                data = await resp.json()
                return data["choices"][0]["message"]["content"].strip()
        except aiohttp.ClientError as e:
            print(f"Erro de conexão com a OpenAI: {e}")
            return "Desculpe, não consegui me conectar à inteligência artificial no momento."

# --- MODELOS DE DADOS (Para validação da requisição) ---
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# --- ENDPOINT DA API ---
@app.post("/api/chat", summary="Processa uma conversa e retorna a resposta do chatbot")
async def chat_endpoint(request: ChatRequest) -> Dict[str, Any]:
    """
    Recebe um histórico de mensagens e retorna a resposta do assistente.
    A lógica de adicionar o conteúdo do CSV é tratada aqui.
    """
    historico_mensagens = [msg.dict() for msg in request.messages]
    
    # Última mensagem enviada pelo usuário
    last_user_message = historico_mensagens[-1]['content']
    
    # Verifica se o contexto do BMG já foi adicionado ao histórico
    contexto_bmg_presente = any("BMG.csv" in m.get("content", "") for m in historico_mensagens)

    # Se "BMG" for mencionado e o contexto ainda não foi adicionado
    if "BMG" in last_user_message.upper() and not contexto_bmg_presente:
        try:
            with open(CSV_FILE_PATH, "r", encoding="utf-8") as f:
                conteudo_csv = f.read()
            
            # Insere o contexto do CSV logo após a primeira mensagem de "system"
            context_message = {
                "role": "system", 
                "content": f"Considere o seguinte conteúdo da base BMG.csv:\n\n{conteudo_csv}"
            }
            historico_mensagens.insert(1, context_message)

        except FileNotFoundError:
            print(f"AVISO: Arquivo {CSV_FILE_PATH} não encontrado.")
            # Opcional: informar ao usuário que o arquivo não foi encontrado
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV: {e}")

    resposta_gpt = await consultar_chatgpt_com_contexto(historico_mensagens)
    
    return {"role": "assistant", "content": resposta_gpt}

if __name__ == "__main__":
    uvicorn.run("chat:app", host="0.0.0.0", port=8000, reload=True)

