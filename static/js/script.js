// Declaration of global variables to be accessed by other scripts
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
    const rebuildIndexBtn = document.getElementById('rebuild-index-btn');
    
    // Store chat history
    let chatHistory = [];
    
    // Auto-resize textarea based on content
    chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = (chatInput.scrollHeight) + 'px';
    });
    
    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const question = chatInput.value.trim();
        if (!question) return;
        
        // Add user message to chat
        window.addMessage(question, 'user');
        
        // Reset input
        chatInput.value = '';
        chatInput.style.height = 'auto';
        
        // Disable input during processing
        window.toggleInputState(false);
        
        // Show loading indicator
        const loadingIndicator = window.addLoadingIndicator();
        
        try {
            // Send request to server
            const response = await window.sendMessageToServer(question, chatHistory);
            
            // Remove loading indicator
            loadingIndicator.remove();
            
            // Add bot response to chat
            window.addMessage(response.answer, 'bot');
            
            // Update chat history
            chatHistory = response.history;
        } catch (error) {
            // Remove loading indicator
            loadingIndicator.remove();
            
            // Display error message
            window.addErrorMessage(error.message || 'An error occurred while processing your request.');
            console.error('Error:', error);
        } finally {
            // Re-enable input
            window.toggleInputState(true);
            chatInput.focus();
        }
    });
    
    // Handle rebuild index button click
    if (rebuildIndexBtn) {
        rebuildIndexBtn.addEventListener('click', async () => {
            if (confirm('Are you sure you want to update the knowledge base? This process may take some time.')) {
                try {
                    // Disable button and show loading state
                    rebuildIndexBtn.disabled = true;
                    rebuildIndexBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Updating...';
                    
                    // Call the rebuild index API
                    const response = await fetch('/api/rebuild-index', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    
                    const result = await response.json();
                    
                    if (!response.ok) {
                        throw new Error(result.error || 'Failed to rebuild knowledge base');
                    }
                    
                    // Show success message in chat
                    window.addMessage('Knowledge base has been successfully updated! Now I have the latest information about Udayana University.', 'bot');
                    
                } catch (error) {
                    console.error('Error rebuilding index:', error);
                    window.addErrorMessage('Failed to update knowledge base: ' + error.message);
                } finally {
                    // Reset button state
                    rebuildIndexBtn.disabled = false;
                    rebuildIndexBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Update Knowledge';
                }
            }
        });
    }
    
    // Function to send message to server
    window.sendMessageToServer = async function(question, history) {
        // Check if page is rendered by Flask
        const isFlaskRendered = document.querySelector('meta[name="rendered-by"][content="flask-server"]') !== null;
        
        // Demo mode only if file is opened directly (file:// protocol) or there's no Flask indicator
        if (window.location.protocol === 'file://' || !isFlaskRendered) {
            console.log("Demo mode detected: Page not rendered by Flask");
            // Simulate server response delay
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Demo response
            return {
                answer: "This is a demo response because you opened the page directly without a backend server. For full functionality, run the application with Flask using 'python run.py'.",
                history: [
                    { role: "user", content: question },
                    { role: "assistant", content: "This is a demo response because you opened the page directly without a backend server. For full functionality, run the application with Flask using 'python run.py'." }
                ]
            };
        }
        
        console.log("Sending request to Flask server");
        
        // Code for integration with Flask server
        try {
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
        } catch (error) {
            console.error("Error accessing API:", error);
            
            // If there's a network error, check if it's because the file was opened directly
            if (error.message.includes("Failed to fetch") || error.message.includes("NetworkError")) {
                return {
                    answer: "Cannot connect to the backend server. Make sure the Flask server is running correctly at http://localhost:5000.",
                    history: [
                        { role: "user", content: question },
                        { role: "assistant", content: "Cannot connect to the backend server. Make sure the Flask server is running correctly at http://localhost:5000." }
                    ]
                };
            }
            
            throw error; // Re-throw other errors
        }
    };
    
    // Function to add message to chat
    window.addMessage = function(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        // For text that may contain line breaks or paragraphs
        const formattedText = text
            .split('\n')
            .filter(line => line.trim() !== '')
            .map(line => `<p>${line}</p>`)
            .join('');
        
        messageContent.innerHTML = formattedText;
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Auto-scroll to the latest message
        window.scrollToBottom();
    };
    
    // Function to add error message
    window.addErrorMessage = function(text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot-message', 'error-message');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = `<p>❌ ${text}</p>`;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Auto-scroll to the latest message
        window.scrollToBottom();
    };
    
    // Function to add loading indicator
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
    
    // Function to toggle input state
    window.toggleInputState = function(enabled) {
        chatInput.disabled = !enabled;
        sendButton.disabled = !enabled;
    };
    
    // Function to auto-scroll to bottom
    window.scrollToBottom = function() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };
    
    // Handle enter key in textarea (send with Enter, new line with Shift+Enter)
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
});