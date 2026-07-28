import React, { useState, useEffect, useRef } from 'react';
import { Send, User } from 'lucide-react';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [ws, setWs] = useState(null);
  const messagesEndRef = useRef(null);

  // Scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    fetchHistory();
    // Connect WebSocket
    // Client id could be from JWT, but we mock it for MVP
    const clientId = Math.floor(Math.random() * 1000); 
    // We updated main.py WS endpoint to just /ws
    const socket = new WebSocket(`ws://localhost:8000/api/v1/messages/ws`);
    
    socket.onopen = () => {
      console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // add new message to state
      setMessages(prev => [...prev, { id: Date.now(), ...data }]);
    };

    setWs(socket);

    return () => {
      socket.close();
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchHistory = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/messages/history');
      if (res.ok) {
        const data = await res.json();
        // format data to match websocket data
        const formatted = data.map(m => ({
          id: m.id,
          sender: m.sender_id === "00000000-0000-0000-0000-000000000000" ? "User" : "System/Other",
          text: m.content
        }));
        setMessages(formatted);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const sendMessage = (e) => {
    e.preventDefault();
    if (!input.trim() || !ws) return;
    
    ws.send(input);
    // Note: The websocket server is currently broadcasting to ALL including sender.
    // If it didn't echo back, we'd add it to local state here.
    setInput('');
  };

  return (
    <div className="chat-container">
      <div className="chat-header card">
        <h2>Global O'quvchilar Chati</h2>
        <p className="text-muted">Real vaqtda (WebSocket) barcha o'quvchilar va o'qituvchilar bilan muloqot qiling</p>
      </div>

      <div className="chat-messages-area card">
        {messages.length === 0 ? (
          <div className="empty-chat">
            <p>Hozircha xabarlar yo'q. Birinchi bo'lib yozing!</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={msg.id || idx} className={`chat-message ${msg.sender === 'System' ? 'system-msg' : (msg.sender === 'User' ? 'my-msg' : 'other-msg')}`}>
              <div className="chat-avatar">
                <User size={16} />
              </div>
              <div className="chat-bubble">
                <span className="chat-sender">{msg.sender}</span>
                <p className="chat-text">{msg.text}</p>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area card">
        <form onSubmit={sendMessage}>
          <input 
            type="text" 
            placeholder="Xabar yozing..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button type="submit" className="btn-primary btn-icon" disabled={!input.trim()}>
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default Chat;
