import React, { useState, useEffect, useRef, useContext } from 'react';
import { Send, User } from 'lucide-react';
import { api, WS_URL } from '../../api';
import { AuthContext } from '../../context/AuthContext';
import './Chat.css';

const Chat = ({ courseId = null }) => {
  const { user } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [ws, setWs] = useState(null);
  const messagesEndRef = useRef(null);

  const myName = user?.full_name || user?.email;

  // Scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    setMessages([]);
    fetchHistory();
    // Connect WebSocket (backend JWT ni query param orqali talab qiladi)
    const token = localStorage.getItem('token');
    if (!token) return;
    const url = `${WS_URL}/messages/ws?token=${token}${courseId ? `&course_id=${courseId}` : ''}`;
    const socket = new WebSocket(url);

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
  }, [courseId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchHistory = async () => {
    try {
      const data = await api(`/messages/history${courseId ? `?course_id=${courseId}` : ''}`);
      const formatted = data.map(m => ({
        id: m.id,
        sender: m.sender ?? '—',
        text: m.content
      }));
      setMessages(formatted);
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
        <h2>{courseId ? 'Kurs Chati' : "Global O'quvchilar Chati"}</h2>
        <p className="text-muted">
          {courseId
            ? "Faqat shu kursga yozilgan o'quvchilar va o'qituvchilar bilan muloqot"
            : "Real vaqtda (WebSocket) barcha o'quvchilar va o'qituvchilar bilan muloqot qiling"}
        </p>
      </div>

      <div className="chat-messages-area card">
        {messages.length === 0 ? (
          <div className="empty-chat">
            <p>Hozircha xabarlar yo'q. Birinchi bo'lib yozing!</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={msg.id || idx} className={`chat-message ${msg.sender === 'System' ? 'system-msg' : (msg.sender === myName ? 'my-msg' : 'other-msg')}`}>
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
