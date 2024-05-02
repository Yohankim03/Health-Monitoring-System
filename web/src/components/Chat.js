import React, { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';

function ChatComponent({ user }) {
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState('');
    const [recipient, setRecipient] = useState('');
    const [recipients, setRecipients] = useState([]);

    // Fetch recipients when component mounts
    useEffect(() => {
        axios.get(`http://localhost:5000/users/possible_recipients`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
        }).then(response => {
            setRecipients(response.data);
        });
        

        const socket = io('ws://localhost:3000'); // Adjust this to your WebSocket server URL
        socket.on('new_message', message => {
            setMessages(prevMessages => [...prevMessages, message]);
        });

        return () => socket.disconnect(); // Clean up on unmount
    }, []);

    
    const handleSendMessage = async () => {
        if (message !== '' && recipient !== '') {
            try {
                const postData = {
                    sender_id: user.id,
                    receiver_id: recipient,
                    content: message
                };
                const response = await axios.post('http://localhost:5000/messages/send', postData, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
                });
                setMessages([...messages, response.data]); // Update local message list
                setMessage(''); // Clear message input
            } catch (error) {
                console.error('Failed to send message:', error);
            }
        } else {
            alert('Please select a recipient and enter a message.');
        }
    };

    return (
        <div>
            <h2>Chat</h2>
            <select value={recipient} onChange={e => setRecipient(e.target.value)}>
                <option value="">Select a Recipient</option>
                {recipients.map(r => (
                    <option key={r.id} value={r.id}>{r.name}</option>
                ))}
            </select>
            <ul>
                {messages.map((msg, index) => (
                    <li key={index}>{msg.sender_id === user.id ? 'You' : msg.sender_name}: {msg.content}</li>
                ))}
            </ul>
            <input type="text" value={message} onChange={e => setMessage(e.target.value)} />
            <button onClick={handleSendMessage}>Send</button>
        </div>
    );
}

export default ChatComponent;
