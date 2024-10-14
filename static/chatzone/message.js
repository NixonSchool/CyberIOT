// message.js

const currentUserId = document.body.getAttribute('data-user-id');
let currentChatUserId = null;
let lastMessageId = 0;
let isPolling = false;
let pollingInterval;

document.addEventListener('DOMContentLoaded', function() {
    // Friend list click event
    document.querySelectorAll('.friend-list-item').forEach(item => {
        item.addEventListener('click', function() {
            const userId = this.getAttribute('data-user-id');
            const username = this.getAttribute('data-username');
            loadChat(userId, username);
        });
    });

    // Back button
    document.getElementById('back-button').addEventListener('click', closeChatArea);

    // Delete chat button
    document.getElementById('delete-chat').addEventListener('click', function() {
        if (currentChatUserId) {
            deleteChat(currentChatUserId);
        }
    });

    // Send message button
    document.getElementById('send-button').addEventListener('click', sendMessage);

    // Modified the keypress event listener for the message input
    document.getElementById('message-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    // Restore chat state on page load
    const storedChatUserId = localStorage.getItem('currentChatUserId');
    const storedChatUsername = localStorage.getItem('currentChatUsername');
    if (storedChatUserId && storedChatUsername) {
        loadChat(storedChatUserId, storedChatUsername);
    }

    // Friend request buttons
    setupFriendRequestButtons();
});

function loadChat(userId, username) {
    currentChatUserId = userId;

    // Update UI elements
    document.getElementById('chat-header').querySelector('h2').textContent = `Chat with ${username}`;
    document.getElementById('back-button').style.display = 'inline-block';
    document.getElementById('delete-chat').style.display = 'inline-block';
    document.getElementById('chat-input').style.display = 'flex';
    document.getElementById('chat-messages').innerHTML = '';

    // Store current chat state
    localStorage.setItem('currentChatUserId', userId);
    localStorage.setItem('currentChatUsername', username);

    // Fetch messages
    fetch(`/chatzone/load_chat/${userId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            data.messages.forEach(function(msg) {
                appendMessage(msg.content, msg.timestamp, msg.is_sender);
            });
            scrollToBottom();
            if (data.messages.length > 0) {
                lastMessageId = data.messages[data.messages.length - 1].id;
            }
            startPolling();
        })
        .catch(error => {
            console.error('Error loading chat:', error);
            alert('Failed to load chat messages. Please try again.');
        });
}

function closeChatArea() {
    document.getElementById('chat-header').querySelector('h2').textContent = 'Select a chat to start messaging';
    document.getElementById('back-button').style.display = 'none';
    document.getElementById('delete-chat').style.display = 'none';
    document.getElementById('chat-input').style.display = 'none';
    document.getElementById('chat-messages').innerHTML = '';
    currentChatUserId = null;

    // Clear stored chat state
    localStorage.removeItem('currentChatUserId');
    localStorage.removeItem('currentChatUsername');

    stopPolling();
}

function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (!message || !currentChatUserId) {
        return;
    }

    // Clear the input immediately to prevent double sending
    messageInput.value = '';

    const tempId = 'temp-' + Date.now();
    appendMessage(message, new Date().toLocaleTimeString(), true, tempId);
    scrollToBottom();

    fetch(`/chatzone/send_message/${currentChatUserId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `content=${encodeURIComponent(message)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update the temporary message with the confirmed one
            const tempMessage = document.getElementById(tempId);
            if (tempMessage) {
                tempMessage.id = `msg-${data.message.id}`;
                tempMessage.querySelector('.message-timestamp').textContent = data.message.timestamp;
            }
            lastMessageId = data.message.id;
        } else {
            // Remove the temporary message if sending failed
            document.getElementById(tempId)?.remove();
            alert('Failed to send message. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById(tempId)?.remove();
        alert('An error occurred while sending the message.');
    });
}

function pollNewMessages() {
    if (!currentChatUserId) return;

    fetch(`/chatzone/get_new_messages/${currentChatUserId}/?last_message_id=${lastMessageId}`)
        .then(response => response.json())
        .then(data => {
            data.messages.forEach(msg => {
                const existingMsg = document.getElementById(`msg-${msg.id}`);
                if (!existingMsg) {
                    appendMessage(msg.content, msg.timestamp, msg.sender_id == currentUserId, `msg-${msg.id}`);
                    lastMessageId = Math.max(lastMessageId, msg.id);
                }
            });
            if (data.messages.length > 0) {
                scrollToBottom();
            }
        })
        .catch(error => console.error('Error polling messages:', error));
}

function appendMessage(content, timestamp, isSender, id = null) {
    const messageClass = isSender ? 'sender' : 'receiver';
    const message = `
        <div id="${id || ''}" class="message ${messageClass}">
            <p>${content}</p>
            <span class="message-timestamp">${timestamp}</span>
        </div>
    `;
    document.getElementById('chat-messages').insertAdjacentHTML('beforeend', message);
}


//Polling, fetching the messages and displaying them to the user
function startPolling() {
    stopPolling();  // Clear any existing interval
    pollingInterval = setInterval(pollNewMessages, 1000);  // Poll every 1 second
    longPoll();  // Start long-polling
}

function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
    }
    isPolling = false;
}

function pollNewMessages() {
    if (!currentChatUserId || isPolling) return;

    isPolling = true;
    fetch(`/chatzone/get_new_messages/${currentChatUserId}/?last_message_id=${lastMessageId}`)
        .then(response => response.json())
        .then(data => {
            data.messages.forEach(msg => {
                const existingMsg = document.getElementById(`msg-${msg.id}`);
                if (!existingMsg) {
                    appendMessage(msg.content, msg.timestamp, msg.sender_id == currentUserId, `msg-${msg.id}`);
                    lastMessageId = Math.max(lastMessageId, msg.id);
                }
            });
            if (data.messages.length > 0) {
                scrollToBottom();
            }
        })
        .catch(error => console.error('Error polling messages:', error))
        .finally(() => {
            isPolling = false;
        });
}

function longPoll() {
    if (!currentChatUserId) return;

    fetch(`/chatzone/long_poll/${currentChatUserId}/?last_message_id=${lastMessageId}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.messages && data.messages.length > 0) {
            data.messages.forEach(msg => {
                const existingMsg = document.getElementById(`msg-${msg.id}`);
                if (!existingMsg) {
                    appendMessage(msg.content, msg.timestamp, msg.sender_id == currentUserId, `msg-${msg.id}`);
                    lastMessageId = Math.max(lastMessageId, msg.id);
                }
            });
            scrollToBottom();
        }
        // Immediately start a new long-polling request
        longPoll();
    })
    .catch(error => {
        console.error('Long-polling error:', error);
        // If there's an error, wait a bit before trying again
        setTimeout(longPoll, 5000);
    });
}



function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function deleteChat(userId) {
    if (confirm("Are you sure you want to delete this chat?")) {
        fetch(`/chatzone/delete_chat/${userId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const friendListItem = document.querySelector(`.friend-list-item[data-user-id="${userId}"]`);
                if (friendListItem) {
                    friendListItem.remove();
                }
                closeChatArea();
                updateFriendshipStatus(userId, 'not_friends');
            } else {
                alert('Failed to delete chat. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the chat.');
        });
    }
}

function updateFriendshipStatus(userId, status) {
    const friendListItem = document.querySelector(`.friend-list-item[data-user-id="${userId}"]`);
    if (friendListItem) {
        const username = friendListItem.getAttribute('data-username');
        friendListItem.outerHTML = `
            <div class="friend-list-item" data-user-id="${userId}" data-username="${username}">
                <img src="../../static/images/default.png" alt="${username}" class="friend-avatar">
                <div class="friend-info">
                    <h3>${username}</h3>
                    <button onclick="sendFriendRequest(${userId})">Send Friend Request</button>
                </div>
            </div>
        `;
    }
}

function setupFriendRequestButtons() {
    document.querySelectorAll('.send-request').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.getAttribute('data-user-id');
            sendFriendRequest(userId);
        });
    });

    document.querySelectorAll('.cancel-request').forEach(button => {
        button.addEventListener('click', function() {
            const requestId = this.getAttribute('data-request-id');
            cancelFriendRequest(requestId);
        });
    });

    document.querySelectorAll('.accept-request').forEach(button => {
        button.addEventListener('click', function() {
            const requestId = this.getAttribute('data-request-id');
            acceptFriendRequest(requestId);
        });
    });

    document.querySelectorAll('.decline-request').forEach(button => {
        button.addEventListener('click', function() {
            const requestId = this.getAttribute('data-request-id');
            declineFriendRequest(requestId);
        });
    });
}

function sendFriendRequest(userId) {
    fetch(`/chatzone/send_friend_request/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const button = document.querySelector(`.send-request[data-user-id="${userId}"]`);
            button.textContent = 'Request Sent';
            button.classList.remove('btn-primary', 'send-request');
            button.classList.add('btn-secondary');
            button.disabled = true;
        }
    })
    .catch(error => console.error('Error:', error));
}

function cancelFriendRequest(requestId) {
    if (confirm("Are you sure you want to cancel the friend request?")) {
        fetch(`/chatzone/cancel_friend_request/${requestId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateFriendshipStatus(requestId, 'not_friends');
            } else {
                alert('Failed to cancel the friend request. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while canceling the friend request.');
        });
    }
}

function acceptFriendRequest(requestId) {
    fetch(`/chatzone/accept_friend_request/${requestId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            updateFriendshipStatus(requestId, 'friends');
        } else {
            alert('Failed to accept the friend request. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while accepting the friend request.');
    });
}

function declineFriendRequest(requestId) {
    fetch(`/chatzone/decline_friend_request/${requestId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            updateFriendshipStatus(requestId, 'not_friends');
        } else {
            alert('Failed to decline the friend request. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while declining the friend request.');
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}