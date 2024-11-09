 // App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [query, setQuery] = useState('');
    const [dbType, setDbType] = useState('LOCALDB');
    const [mysqlDetails, setMysqlDetails] = useState({ host: '', user: '', password: '', dbName: '' });
    const [apiKey, setApiKey] = useState('');
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'How can I help you?' }
    ]);

    const handleQuerySubmit = async () => {
        const payload = {
            query: query,
            db_uri: dbType,
            api_key: apiKey,
            mysql_host: mysqlDetails.host,
            mysql_user: mysqlDetails.user,
            mysql_password: mysqlDetails.password,
            mysql_db: mysqlDetails.dbName,
        };

        try {
            const response = await axios.post('http://127.0.0.1:5000/ask_sql', payload);
            console.log(response)
            setMessages([...messages, { role: 'user', content: query }, { role: 'assistant', content: response.data.response }]);
            setQuery('');
        } catch (error) {
            console.error("Error querying the database:", error);
        }
    };

    return (
        <div className="app">
            <h1>SQLMate</h1>
            <div className="sidebar">
                <h3>Database Configuration</h3>
                <select value={dbType} onChange={(e) => setDbType(e.target.value)}>
                    <option value="LOCALDB">Use SQLite 3 Database - Student.db</option>
                    <option value="MYSQL">Connect to MySQL Database</option>
                </select>
                
                {dbType === 'MYSQL' && (
                    <>
                        <input type="text" placeholder="MySQL Host" value={mysqlDetails.host} onChange={(e) => setMysqlDetails({ ...mysqlDetails, host: e.target.value })} />
                        <input type="text" placeholder="MySQL User" value={mysqlDetails.user} onChange={(e) => setMysqlDetails({ ...mysqlDetails, user: e.target.value })} />
                        <input type="password" placeholder="MySQL Password" value={mysqlDetails.password} onChange={(e) => setMysqlDetails({ ...mysqlDetails, password: e.target.value })} />
                        <input type="text" placeholder="MySQL Database" value={mysqlDetails.dbName} onChange={(e) => setMysqlDetails({ ...mysqlDetails, dbName: e.target.value })} />
                    </>
                )}
                
                <input type="password" placeholder="Groq API Key" value={apiKey} onChange={(e) => setApiKey(e.target.value)} />
            </div>

            <div className="chat-box">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.role}`}>
                        <p>{msg.content}</p>
                    </div>
                ))}
            </div>

            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask anything from the database"
            />
            <button onClick={handleQuerySubmit}>Submit</button>
        </div>
    );
}

export default App;
