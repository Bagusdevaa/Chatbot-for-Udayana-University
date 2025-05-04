document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendButton = document.getElementById('send-button');
    
    // Menyimpan history chat
    let chatHistory = [];
    
    // Auto-resize textarea berdasarkan konten
    chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = (chatInput.scrollHeight) + 'px';
    });
    
    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const question = chatInput.value.trim();
        if (!question) return;
        
        // Tambahkan pesan user ke chat
        addMessage(question, 'user');
        
        // Reset input
        chatInput.value = '';
        chatInput.style.height = 'auto';
        
        // Disable input during processing
        toggleInputState(false);
        
        // Tampilkan loading indicator
        const loadingIndicator = addLoadingIndicator();
        
        try {
            // Kirim permintaan ke server
            const response = await sendMessageToServer(question, chatHistory);
            
            // Hapus loading indicator
            loadingIndicator.remove();
            
            // Tambahkan respon bot ke chat
            addMessage(response.answer, 'bot');
            
            // Update history chat
            chatHistory = response.history;
        } catch (error) {
            // Hapus loading indicator
            loadingIndicator.remove();
            
            // Tampilkan pesan error
            addErrorMessage(error.message || 'Terjadi kesalahan saat memproses permintaan Anda.');
            console.error('Error:', error);
        } finally {
            // Re-enable input
            toggleInputState(true);
            chatInput.focus();
        }
    });
    
    // Fungsi untuk mengirim pesan ke server
    async function sendMessageToServer(question, history) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question,
                history
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Server error');
        }
        
        return await response.json();
    }
    
    // Fungsi untuk menambahkan pesan ke chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        // Untuk teks yang mungkin berisi line breaks atau paragraf
        const formattedText = text
            .split('\n')
            .filter(line => line.trim() !== '')
            .map(line => `<p>${line}</p>`)
            .join('');
        
        messageContent.innerHTML = formattedText;
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Auto-scroll ke pesan terbaru
        scrollToBottom();
    }
    
    // Fungsi untuk menambahkan pesan error
    function addErrorMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot-message', 'error-message');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = `<p>❌ ${text}</p>`;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Auto-scroll ke pesan terbaru
        scrollToBottom();
    }
    
    // Fungsi untuk menambahkan loading indicator
    function addLoadingIndicator() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'bot-message', 'loading-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            loadingDiv.appendChild(dot);
        }
        
        chatMessages.appendChild(loadingDiv);
        scrollToBottom();
        
        return loadingDiv;
    }
    
    // Fungsi untuk toggle state input
    function toggleInputState(enabled) {
        chatInput.disabled = !enabled;
        sendButton.disabled = !enabled;
    }
    
    // Fungsi untuk auto-scroll ke bawah
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Handle enter key pada textarea (kirim dengan Enter, baris baru dengan Shift+Enter)
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
});