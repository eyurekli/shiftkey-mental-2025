import './styles/App.css';
import Header from './components/Header';
import AudioVisualizer from './components/AudioVisualizer';
import Resources from './components/Resources';
import React, { useState } from 'react';
import axios from 'axios';
import Checklist from './components/Checklist';

function App() {
  
  const [message, setMessage] = useState('');

  const runNotebook = async () => {
    try {
      const response = await axios.get('http://localhost:5000/run_notebook');
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error running notebook');
    }
  };


  return (
    <>
      <div style={{ position: "relative" }}>
        <Header />  
        <Resources />
        <Checklist />
      </div>
      
      <div className="center">
        <button className="button">Try Now</button>
        <div id = "visualizer-bar">
        <AudioVisualizer />
        </div>
        <div>
          <button onClick={runNotebook}>Run Notebook</button>
          <p>{message}</p>
        </div>
      </div>


    </>
  );
}

export default App;
