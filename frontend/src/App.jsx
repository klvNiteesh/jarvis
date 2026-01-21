import { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m Jarvis, your personal AI assistant powered by LLaMA. I can help you with questions, store knowledge, and provide contextual responses. How can I assist you today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    // Always scroll to bottom when messages change
    scrollToBottom();
  }, [messages]);

  // Check backend connection
  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        setConnectionStatus('connected');
      } else {
        setConnectionStatus('disconnected');
      }
    } catch (error) {
      setConnectionStatus('disconnected');
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          history: messages
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      const assistantMessage = {
        role: 'assistant',
        content: data.response
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: '⚠️ Sorry, I couldn\'t connect to the backend server. Please make sure the Python server is running on http://localhost:8000'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);

    for (const file of files) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://localhost:8000/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          setUploadedFiles(prev => [...prev, { name: file.name, id: data.id }]);

          // Add confirmation message
          const confirmMessage = {
            role: 'assistant',
            content: `✓ Successfully processed "${file.name}" and added it to my knowledge base!`
          };
          setMessages(prev => [...prev, confirmMessage]);
        }
      } catch (error) {
        console.error('Upload error:', error);
        const errorMessage = {
          role: 'assistant',
          content: `⚠️ Failed to upload "${file.name}". Please ensure the backend is running.`
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    }
  };

  const removeFile = (index) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-content">
          <div className="logo-container">
            <div className="logo-icon">🤖</div>
            <h1 className="app-title">JARVIS</h1>
          </div>
          <p className="app-subtitle">Your Personal AI Assistant - Powered by LLaMA & Pinecone</p>
        </div>
      </header>

      <main className="main-content">
        <aside className="sidebar">
          <div className="info-card">
            <h3><span className="icon">⚡</span> System Status</h3>
            <div className="status-indicator">
              <span className="status-dot" style={{
                background: connectionStatus === 'connected' ? '#00f2fe' :
                  connectionStatus === 'checking' ? '#f5576c' : '#666'
              }}></span>
              <span>
                {connectionStatus === 'connected' ? 'Backend Connected' :
                  connectionStatus === 'checking' ? 'Checking...' : 'Backend Offline'}
              </span>
            </div>
            <div className="status-indicator">
              <span className="status-dot" style={{ background: '#00f2fe' }}></span>
              <span>LLaMA Model Ready</span>
            </div>
            <div className="status-indicator">
              <span className="status-dot" style={{ background: '#00f2fe' }}></span>
              <span>Vector DB Active</span>
            </div>
          </div>

          <div className="info-card">
            <h3><span className="icon">🎯</span> Capabilities</h3>
            <ul className="feature-list">
              <li>Natural Language Understanding</li>
              <li>Contextual Conversations</li>
              <li>Knowledge Base Storage</li>
              <li>Document Processing</li>
              <li>Semantic Search</li>
            </ul>
          </div>

          <div className="info-card">
            <h3><span className="icon">📚</span> Knowledge Base</h3>
            <div className="knowledge-base">
              <div className="kb-upload">
                <div className="file-input-wrapper">
                  <input
                    type="file"
                    id="file-upload"
                    className="file-input"
                    multiple
                    accept=".txt,.pdf,.doc,.docx"
                    onChange={handleFileUpload}
                  />
                  <label htmlFor="file-upload" className="file-input-label">
                    <span>📎</span>
                    <span>Upload Documents</span>
                  </label>
                </div>
                {uploadedFiles.length > 0 && (
                  <div className="uploaded-files">
                    {uploadedFiles.map((file, index) => (
                      <div key={index} className="file-item">
                        <span>📄 {file.name}</span>
                        <button onClick={() => removeFile(index)}>×</button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </aside>

        <div className="chat-container">
          <div className="chat-messages">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.role}`}>
                <div className="message-avatar">
                  {message.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  <div className="message-text">{message.content}</div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-container">
            <div className="chat-input-wrapper">
              <input
                type="text"
                className="chat-input"
                placeholder="Ask me anything..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
              />
              <button
                className="send-button"
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
              >
                {isLoading ? 'Thinking...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
