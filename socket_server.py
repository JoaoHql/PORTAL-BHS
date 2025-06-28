from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager
from tasks import obter_dados, gerar_resumo
from ai_engine import interpretar_intencao
import asyncio

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Mensagem recebida de {websocket.client}: {data}")
            asyncio.create_task(handle_message(data, websocket))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Ocorreu um erro no WebSocket: {e}")
        manager.disconnect(websocket)

async def handle_message(data, websocket):
    try:
        resultado = await interpretar_intencao(data)
        intencao = resultado.get("intencao")
        parametros = resultado.get("parametros", {})

        if intencao == "obter_dados":
            resposta = await obter_dados(parametros)
        elif intencao == "resumo":
            resposta = await gerar_resumo(parametros)
        else:
            resposta = "Desculpe, não consegui entender o que você deseja."

        await manager.send_personal_message(
            {"role": "assistant", "content": resposta}, websocket
        )
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
