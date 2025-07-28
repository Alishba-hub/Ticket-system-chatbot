let currentState = 'welcome';
let ticketData = {};
let currentThreadId = null;
let backendState = {};

//API endpoints are hereeee
const API_BASE = window.location.origin;
const API_ENDPOINTS = {
    processTicket: `${API_BASE}/api/process_ticket`,
    processFollowup: `${API_BASE}/api/process_followup`
};

//Initialization hereee
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('messageInput');
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    input.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
});

function addMessage(content, isUser = false, isSystem = false) {
    const messagesContainer = document.getElementById('messages');
    const welcome = document.getElementById('welcome');
    
    if (welcome) {
        welcome.style.display = 'none';
    }

    const messageDiv = document.createElement('div');

    if (isSystem) {
        if (content.includes('✅')) {
            messageDiv.className = 'success-indicator';
        } else {
            messageDiv.className = 'step-indicator';
        }
        messageDiv.textContent = content;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return;
    }

    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.innerHTML = formatMessage(content);

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

    messageDiv.appendChild(bubbleDiv);
    messageDiv.appendChild(timeDiv);
    messagesContainer.appendChild(messageDiv);

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addErrorMessage(content) {
    const messagesContainer = document.getElementById('messages');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = content;
    messagesContainer.appendChild(errorDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function formatMessage(content) {
    return content
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
}

function showTyping() {
    document.getElementById('typing').style.display = 'block';
}

function hideTyping() {
    document.getElementById('typing').style.display = 'none';
}

function updateStatus(status, text) {
    const indicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    
    indicator.className = `status-badge status-${status}`;
    statusText.textContent = text;
}

function enableInput(placeholder = "Type your message here...") {
    const input = document.getElementById('messageInput');
    const button = document.getElementById('sendButton');
    
    input.disabled = false;
    input.placeholder = placeholder;
    button.disabled = false;
    input.focus();
}

function disableInput() {
    const input = document.getElementById('messageInput');
    const button = document.getElementById('sendButton');
    
    input.disabled = true;
    input.placeholder = "Please wait...";
    button.disabled = true;
}

function startNewTicket() {
    ticketData = {};
    currentThreadId = null;
    backendState = {};
    currentState = 'collecting_subject';
    
    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = '';

    addMessage("Step 1 of 2", false, true);
    addMessage("🎫 Welcome to our Professional Support System!\n\nTo provide you with the best assistance, please start by entering your ticket subject:", false);
    
    updateStatus('online', 'Creating new support ticket');
    enableInput("Enter your issue subject...");
}

function showSampleQuestions() {
    const samples = [
        "Application Login Problems",
        "Database Connection Issues",
        "System Performance Problems",
        "API Integration Errors",
        "User Account Management",
        "Software Installation Issues"
    ];
    
    addMessage("Here are some common support categories:\n\n" + 
              samples.map(s => `• ${s}`).join('\n') + 
              "\n\nPlease describe your specific issue for personalized assistance.", false);
}

async function callAPI(endpoint, data) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;

    input.value = '';
    input.style.height = 'auto';

    addMessage(message, true);
    
    if (currentState === 'collecting_subject') {
        if (message.toLowerCase() === 'exit') {
            addMessage("👋 Thank you for using our support system!", false);
            resetToWelcome();
            return;
        }
        
        ticketData.subject = message;
        currentState = 'collecting_description';
        
        disableInput();
        
        setTimeout(() => {
            addMessage("Step 2 of 2", false, true);
            addMessage("📝 Please provide a detailed description of your issue:", false);
            enableInput("Describe your technical issue in detail...");
        }, 1000);
        
    } else if (currentState === 'collecting_description') {
        if (message.toLowerCase() === 'exit') {
            addMessage("👋 Thank you for using our support system!", false);
            resetToWelcome();
            return;
        }
        
        ticketData.description = message;
        currentState = 'processing';
        
        disableInput();
        showTyping();
        updateStatus('processing', 'Analyzing your request');
        
        try {
            const result = await callAPI(API_ENDPOINTS.processTicket, {
                subject: ticketData.subject,
                description: ticketData.description
            });
            
            hideTyping();
            currentThreadId = result.thread_id;
            backendState = result.state;
            
            addMessage("✅ Support ticket processed successfully!", false, true);
            addMessage(result.response, false);
            
            currentState = 'chatting';
            updateStatus('online', 'Support session active');
            enableInput("Continue conversation or type 'new' for new ticket...");
            
        } catch (error) {
            hideTyping();
            addErrorMessage(`Error processing ticket: ${error.message}`);
            enableInput("Please try again or type 'exit' to return to main menu...");
        }
        
    } else if (currentState === 'chatting') {
        if (message.toLowerCase() === 'exit') {
            addMessage("👋 Thank you for using our support system!", false);
            resetToWelcome();
            return;
        }
        
        if (message.toLowerCase() === 'new') {
            startNewTicket();
            return;
        }
        
        disableInput();
        showTyping();
        
        try {
            const result = await callAPI(API_ENDPOINTS.processFollowup, {
                message: message,
                thread_id: currentThreadId,
                current_state: backendState
            });
            
            hideTyping();
            backendState = result.state;
            
            addMessage(result.response, false);
            enableInput("Continue conversation or type 'new' for new ticket...");
            
        } catch (error) {
            hideTyping();
            addErrorMessage(`Error processing follow-up: ${error.message}`);
            enableInput("Please try again or type 'new' for new ticket...");
        }
    }
}

function resetToWelcome() {
    currentState = 'welcome';
    ticketData = {};
    currentThreadId = null;
    backendState = {};
    
    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = `
        <div class="welcome-screen" id="welcome">
            <div class="welcome-icon">🎫</div>
            <h2>Technical Support</h2>
            <p>Welcome to our professional support system. Get expert assistance with your technical issues and questions through our intelligent ticket management system.</p>
            <div class="quick-actions">
                <button class="quick-action" onclick="startNewTicket()">Create Support Ticket</button>
                <button class="quick-action" onclick="showSampleQuestions()">Common Issues</button>
            </div>
        </div>
    `;
    
    updateStatus('online', 'Professional IT Support System');
    disableInput();
}