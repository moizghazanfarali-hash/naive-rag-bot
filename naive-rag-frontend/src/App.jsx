import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, UploadCloud, Bot, User, Loader2, CheckCircle2 } from 'lucide-react';

const BACKEND_URL = 'http://127.0.0.1:8000';

function App() {
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'Hi! Upload a document and ask me anything about it.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setUploadStatus('Uploading and indexing...');

    try {
      const response = await axios.post(`${BACKEND_URL}/api/ingest`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      if (response.data.success) {
        setUploadStatus(`Success: ${file.name}`);
        setMessages(prev => [...prev, { role: 'bot', content: `📁 Document "${file.name}" has been successfully indexed. Ask away!` }]);
      }
    } catch (error) {
      console.error(error);
      setUploadStatus('Upload failed.');
    } finally {
      setUploading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userQuestion = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userQuestion }]);
    setLoading(true);

    try {
      const response = await axios.post(`${BACKEND_URL}/api/chat`, { question: userQuestion });
      if (response.data.success) {
        setMessages(prev => [...prev, { role: 'bot', content: response.data.answer }]);
      }
    } catch (error) {
      console.error(error);
      setUploadStatus('Error sending message.');
    } finally {
      setLoading(false);
    }
  };
return (
    <div className="app-container">
      
      {/* SIDEBAR */}
      <div className="sidebar">
        <div>
          <div className="logo-area">
            <Bot size={28} color="#818cf8" />
            <span>Naive RAG Bot</span>
          </div>
          
          <div className="upload-box" style={{ borderColor: uploadStatus.includes('Success') ? '#10b981' : uploadStatus.includes('failed') ? '#ef4444' : '#334155' }}>
            <input type="file" accept=".pdf,.txt" onChange={handleFileUpload} disabled={uploading} />
            <UploadCloud size={36} color={uploading ? "#818cf8" : "#94a3b8"} style={{ marginBottom: '10px' }} />
            
            {/* dynamic text inside upload box */}
            <div style={{ fontSize: '14px', fontWeight: '500' }}>
              {uploading ? "Processing File..." : "Click to upload file"}
            </div>
            <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>
              {!uploadStatus ? "PDF, TXT" : ""}
            </div>

            {/* Status indicators inside the box */}
            {uploadStatus && (
              <div style={{ marginTop: '12px', fontSize: '13px', color: uploadStatus.includes('Success') ? '#10b981' : '#cbd5e1', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                {uploading ? <Loader2 size={14} className="animate-spin" /> : <CheckCircle2 size={14} color={uploadStatus.includes('Success') ? "#10b981" : "#ef4444"} />}
                <span style={{ maxWidth: '180px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {uploadStatus}
                </span>
              </div>
            )}
          </div>
        </div>

        <div style={{ fontSize: '12px', color: '#475569', textAlign: 'center' }}>
          Jina AI & Groq LLaMA 3
        </div>
      </div>

      {/* CHAT AREA */}
      <div className="chat-area">
        <div className="messages-screen">
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.role === 'user' ? 'user' : 'bot'}`}>
              <div className="avatar">
                {msg.role === 'user' ? <User size={16} color="#fff" /> : <Bot size={16} color="#818cf8" />}
              </div>
              <div className="message-bubble">
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message-wrapper bot">
              <div className="avatar"><Bot size={16} color="#818cf8" /></div>
              <div className="message-bubble" style={{ color: '#94a3b8' }}>Thinking...</div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* FOOTER INPUT */}
        <div className="footer-form">
          <form onSubmit={handleSendMessage} className="input-container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about your documents..."
              className="chat-input"
              disabled={loading}
            />
            <button type="submit" className="send-btn" disabled={loading || !input.trim()}>
              <Send size={18} />
            </button>
          </form>
        </div>

      </div>
    </div>
  );
}

export default App;
