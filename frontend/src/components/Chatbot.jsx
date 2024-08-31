import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async () => {
    try {
      const responseData = await axios.post('http://localhost:5000/generate-response', { input: inputText });
      setResponse(responseData.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} />
      <button onClick={handleSubmit}>Submit</button>
      <div>
        {response && (
          <div>
          <p><h2>Problem Summary</h2>: {response.problemSummary}</p>
          <p><h2>How Normal it is</h2>: {response.howNormal}</p>
          <p><h2>How it can be Improved</h2>: {response.howImproved}</p>
          <p><h2>Cause of the Problem</h2>: {response.causeOfProblem}</p>
          <p><h2>Potential Solutions</h2>: {response.potentialSolutions}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chatbot;
