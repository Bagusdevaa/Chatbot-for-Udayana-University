// Deklarasi variabel global untuk bisa diakses oleh script lain
window.addMessage = null;
window.addErrorMessage = null;
window.addLoadingIndicator = null;
window.sendMessageToServer = null;
window.toggleInputState = null;
window.scrollToBottom = null;

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
        window.addMessage(question, 'user');
        
        // Reset input
        chatInput.value = '';
        chatInput.style.height = 'auto';
        
        // Disable input during processing
        window.toggleInputState(false);
        
        // Tampilkan loading indicator
        const loadingIndicator = window.addLoadingIndicator();
        
        try {
            // Kirim permintaan ke server
            const response = await window.sendMessageToServer(question, chatHistory);
            
            // Hapus loading indicator
            loadingIndicator.remove();
            
            // Tambahkan respon bot ke chat
            window.addMessage(response.answer, 'bot');
            
            // Update history chat
            chatHistory = response.history;
        } catch (error) {
            // Hapus loading indicator
            loadingIndicator.remove();
            
            // Tampilkan pesan error
            window.addErrorMessage(error.message || 'Terjadi kesalahan saat memproses permintaan Anda.');
            console.error('Error:', error);
        } finally {
            // Re-enable input
            window.toggleInputState(true);
            chatInput.focus();
        }
    });
    
    // Fungsi untuk mengirim pesan ke server
    window.sendMessageToServer = async function(question, history) {
        // Mode demo untuk "Go Live" tanpa server backend
        if (window.location.protocol === 'file:' || 
            window.location.hostname === '127.0.0.1' || 
            window.location.hostname === 'localhost') {
            // Simulasi delay respons server
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Respons demo
            return {
                answer: "Ini adalah respons demo karena Anda membuka halaman secara langsung tanpa server backend. Untuk fungsionalitas penuh, jalankan aplikasi dengan Flask menggunakan 'python run.py'.",
                history: [
                    { role: "user", content: question },
                    { role: "assistant", content: "Ini adalah respons demo karena Anda membuka halaman secara langsung tanpa server backend. Untuk fungsionalitas penuh, jalankan aplikasi dengan Flask menggunakan 'python run.py'." }
                ]
            };
        }
        
        // Kode untuk integrasi dengan server Flask
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
    };
    
    // Fungsi untuk menambahkan pesan ke chat
    window.addMessage = function(text, sender) {
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
        window.scrollToBottom();
    };
    
    // Fungsi untuk menambahkan pesan error
    window.addErrorMessage = function(text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot-message', 'error-message');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = `<p>❌ ${text}</p>`;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Auto-scroll ke pesan terbaru
        window.scrollToBottom();
    };
    
    // Fungsi untuk menambahkan loading indicator
    window.addLoadingIndicator = function() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'bot-message', 'loading-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            loadingDiv.appendChild(dot);
        }
        
        chatMessages.appendChild(loadingDiv);
        window.scrollToBottom();
        
        return loadingDiv;
    };
    
    // Fungsi untuk toggle state input
    window.toggleInputState = function(enabled) {
        chatInput.disabled = !enabled;
        sendButton.disabled = !enabled;
    };
    
    // Fungsi untuk auto-scroll ke bawah
    window.scrollToBottom = function() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };
    
    // Handle enter key pada textarea (kirim dengan Enter, baris baru dengan Shift+Enter)
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
});