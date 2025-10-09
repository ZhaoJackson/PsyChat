let isRecording = false;
let mediaRecorder;
let audioChunks = [];
let recordCount = 0; // Record the number of times user completed recording

function toggleRecording() {
    let recordBtn = document.getElementById('record-btn');
    if (!isRecording) {
        startRecording();
        recordBtn.textContent = 'Stop';
        isRecording = true;
    } else {
        stopRecording();
        recordBtn.textContent = 'Record';
        isRecording = false;
    }
}


function stopRecording() {
    console.log("Stopping recording...");
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop(); // This will trigger 'stop' event and execute the logic below
    }
}

function startRecording() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.log("Browser does not support mediaDevices API, or website does not support Https.");
        return;
    }
    console.log("Starting recording...");
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = []; // Clear array for new recording

            mediaRecorder.start();

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = []; // Reset audio chunks array for next recording

                let formData = new FormData();
                formData.append("audio", audioBlob);

                // Get chat history
                const messages = document.querySelectorAll('.chat-container .message span');
                let history = Array.from(messages).map(m => m.innerText).join('\n');

                // Add chat history as string to form data
                formData.append("history", history);

                fetch("/api/audio_to_audio", {
                    method: "POST",
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Audio file sent", data);
                    addMessage('user', data.asrText);
                    addMessage('therapist', data.llm_response, true);
                    playTTSAudio(data.ttsAudio);
                })
                .catch(error => console.log("Audio file upload failed", error));
            });
        })
        .catch(error => console.log("Failed to get audio stream", error));
}

function playTTSAudio(audioUrl) {

    // Temporarily manually specified
    audioUrl = "/static/wavs/tts.wav";

    // Use fetch to get Blob
    fetch(audioUrl)
        .then(response => response.blob())
        .then(blob => {
            // Create Blob URL
            const blobUrl = URL.createObjectURL(blob);

            // Create audio element and play audio
            const audio = new Audio();
            audio.src = blobUrl;
            audio.play();

            // Can choose to release this Blob URL after playing, but usually we release it after user triggers some action
            // audio.onended = () => URL.revokeObjectURL(blobUrl);
        })
        .catch(error => console.error('Error playing TTS audio:', error));
}


function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== '') {
        addMessage('user', userInput);
        document.getElementById('user-input').value = ''; // Clear input box
        sendChatHistory(); // Send chat history
    }
}

// Function to scroll chat window to bottom for displaying latest messages
function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Save current chat history to local storage
function saveChatHistory() {
    // Select all message span elements
    const messages = document.querySelectorAll('.chat-container .message span');
    // Convert all message text content to array, then join into single string, one message per line
    let history = Array.from(messages).map(m => m.innerText).join('\n');
    // Use localStorage to save entire chat history as a string
    localStorage.setItem('chatHistory', history);
}

// Load chat history from local storage and display on chat interface
function loadChatHistory() {
    // Get saved chat history from localStorage
    const history = localStorage.getItem('chatHistory');
    // If chat history exists
    if (history) {
        // Split history string into individual messages
        const messages = history.split('\n');
        // Iterate through each message
        console.log("Loading chat history: ", messages);
        messages.forEach(msg => {
            const separatorIndex = msg.indexOf(': ');
            const senderLabel = msg.substring(0, separatorIndex);
            const text = msg.substring(separatorIndex + 2);
            const sender = senderLabel.includes('User') || senderLabel.includes('用户') ? 'user' : 'therapist';
            addMessage(sender, text, false);
        });
    }else{
        defaultMessage();
    }
}


// Restore chat history when page loads
window.onload = loadChatHistory;

// Save chat history when user closes page
window.addEventListener('beforeunload', function(event) {
    saveChatHistory();  // Call function to save chat history
});

function clearChat() {
    // Show confirmation dialog for user to confirm clearing chat history
    if (confirm("Are you sure you want to clear the chat history?")) {
        // Clear chat container content
        const chatContainer = document.getElementById('chat-container');
        chatContainer.innerHTML = ''; // Clear chat container
        console.log("Chat history cleared.");

        // Clear locally stored chat history
        localStorage.removeItem('chatHistory');
        console.log("Local chat history cleared.");

        // Clear audio cache
        if ('caches' in window) {
            caches.delete('audio-cache').then(function(deleted) {
                console.log('Audio cache deleted:', deleted);
            });
        }
        defaultMessage();
    } else {
        // If user clicks "Cancel", do not perform any action
        console.log("Cancelled clearing chat history.");
    }
}

function defaultMessage(){
    const messageText = "Hello, how can I help you?";
    addMessage('therapist', messageText, true);
    console.log("Added new therapist message.");
}


// Add a new message to chat container
function addMessage(sender, text, save = true) {
    const container = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    // Use current timestamp to generate unique ID
    const uniqueId = Date.now();
    // Set message content, including sender identifier (user or therapist), message text. And an audio play button, if sender is therapist, add play button; if user, don't add
    // messageDiv.innerHTML = `<span  class="message-text">${sender === 'user' ? '用户' : '咨询师'}: ${text}</span>` +
    //     (sender === 'therapist' ? `<audio controls id="audioPlayer" style="display:none"></audio><button class="audio-button" onclick="loadAudio('${sender}')">播放语音</button>` : '');

    // messageDiv.innerHTML = `<span class="message-text">${sender === 'user' ? '用户' : '咨询师'}: ${text}</span>` +
    //     (sender === 'therapist' ? `<audio controls id="audioPlayer${uniqueId}" style="display:none"></audio><button class="audio-button" id="audioButton${uniqueId}" onclick="toggleAudio('${uniqueId}')">播放语音</button>` : '');
    messageDiv.innerHTML = `<span class="message-text">${sender === 'user' ? 'User' : 'Therapist'}: ${text}</span>`;

    container.appendChild(messageDiv);
    scrollToBottom();
    // Call function to update locally stored chat history
    if (save)
        saveChatHistory();
}

async function toggleAudio(uniqueId) {
    const audioPlayer = document.getElementById(`audioPlayer${uniqueId}`);
    const audioButton = document.getElementById(`audioButton${uniqueId}`);

    if (!audioPlayer.src) { // Check if audio is already loaded
        try {
            const blob = await loadAndCacheAudio(); // Load and cache audio
            audioPlayer.src = URL.createObjectURL(blob);
        } catch (error) {
            console.error('Error fetching and playing audio:', error);
            return;
        }
    }

    // Listen for audio playback end event
    audioPlayer.onended = function() {
        audioButton.innerText = 'Play Audio'; // Update button text to "Play Audio"
    };

    if (audioPlayer.paused || audioPlayer.ended) {
        if (audioPlayer.ended) {
            audioPlayer.currentTime = 0; // Reset audio position
        }
        audioPlayer.play();
        audioButton.innerText = 'Stop Playing';
    } else {
        audioPlayer.pause();
        audioPlayer.currentTime = 0; // Reset audio position when stopping playback
        audioButton.innerText = 'Play Audio';
    }
}

function sendChatHistory() {
    const messages = document.querySelectorAll('.chat-container .message span');
    let history = Array.from(messages).map(m => m.innerText).join('\n');
    console.log("Sending chat history");

    // Send request to backend
    fetch("/api/text_to_audio", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',  // Specify sending JSON
        },
        body: JSON.stringify({text: history})  // Format data as JSON string
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Received response: ", data);
            // Display LLM response
            if (data.llm_response) {
                addMessage('therapist', data.llm_response, true);
            }
            // Play TTS audio
            if (data.ttsAudio) {
                playTTSAudio(data.ttsAudio);
            }
        })
        .catch(error => console.log("Failed to send chat history: ", error));
}

async function loadAndCacheAudio() {
    const audioUrl = '/api/text_converte_audio';

    // Try to use cache
    if ('caches' in window) {
        const cache = await caches.open('audio-cache');
        const cachedResponse = await cache.match(audioUrl);
        if (cachedResponse) {
            console.log('Loading from cache');
            return cachedResponse.blob();
        } else {
            console.log('Fetching and caching new item');
            const response = await fetch(audioUrl);
            cache.put(audioUrl, response.clone());
            return response.blob();
        }
    } else {
        // Cache not available, fetch directly from server
        console.log('Cache not supported, fetching directly');
        const response = await fetch(audioUrl);
        return response.blob();
    }
}

async function loadAudio() {
    try {
        const blob = await loadAndCacheAudio();
        const audioUrl = URL.createObjectURL(blob);
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.src = audioUrl;
        audioPlayer.play();
    } catch (error) {
        console.error('Error fetching and playing audio:', error);
    }
}



