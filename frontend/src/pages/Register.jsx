import React from 'react'
import { useState } from 'react';
import axios from 'axios';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    try {
      const response = await axios.post('http://localhost:5000/register', { username, password });
      // Handle successful login, store authentication token
    } catch (error) {
      // Handle login errors
    }
  };
  return (
    <div>
    <h2>register</h2>
    <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
    <button onClick={handleRegister}>Login</button>
  </div>
  )
}

export default Register