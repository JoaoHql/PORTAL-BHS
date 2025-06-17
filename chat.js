document.addEventListener("DOMContentLoaded", () => {
    // Seleciona os elementos do DOM
    const toggleButton = document.getElementById('chat-toggle-button');
    const closeButton = document.getElementById('chat-close-button');
    const chatWidget = document.getElementById('chat-widget');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const messagesContainer = document.getElementById('chat-messages');

    // URL da sua API (certifique-se que o backend está rodando)
    const API_URL = "http://127.0.0.1:8000/api/chat";

    // Histórico da conversa (essencial para o contexto da IA)
    let conversationHistory = [
        {
            role: "system",
            content: "Você é um assistente que responde perguntas sobre dados fornecidos. Seja breve e economize palavras"
        }
    ];

    // Função para mostrar/esconder o chat
    const toggleChat = () => {
        chatWidget.classList.toggle('hidden');
        if (!chatWidget.classList.contains('hidden')) {
            chatInput.focus();
        }
    };

    // Adiciona a funcionalidade aos botões
    toggleButton.addEventListener('click', toggleChat);
    closeButton.addEventListener('click', toggleChat);

    // Função para adicionar uma mensagem na interface
    const addMessageToUI = (sender, text) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender); // sender será 'user' ou 'assistant'
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        // Rola para a mensagem mais recente
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };
    
    // Função executada ao enviar o formulário
    const handleFormSubmit = async (event) => {
        event.preventDefault(); // Impede o recarregamento da página
        const userMessage = chatInput.value.trim();

        if (!userMessage) return; // Não faz nada se a mensagem estiver vazia

        // 1. Mostra a mensagem do usuário na tela
        addMessageToUI('user', userMessage);
        
        // 2. Adiciona a mensagem do usuário ao histórico
        conversationHistory.push({ role: 'user', content: userMessage });
        
        // 3. Limpa o campo de input
        chatInput.value = '';

        try {
            // 4. Envia o histórico completo para a API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ messages: conversationHistory })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const botResponse = await response.json();

            // 5. Mostra a resposta do bot na tela
            addMessageToUI('assistant', botResponse.content);

            // 6. Adiciona a resposta do bot ao histórico para manter o contexto
            conversationHistory.push(botResponse);

        } catch (error) {
            console.error("Falha ao comunicar com a API:", error);
            addMessageToUI('assistant', 'Desculpe, não consegui obter uma resposta. Tente novamente.');
        }
    };
    
    chatForm.addEventListener('submit', handleFormSubmit);

    // Adiciona uma mensagem de boas-vindas inicial
    addMessageToUI('assistant', 'Olá! Como posso ajudar você hoje?');
});