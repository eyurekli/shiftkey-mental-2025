import './styles/App.css';
import Header from './components/Header';
import AudioVisualizer from './components/AudioVisualizer';
import Resources from './components/Resources';
import React, { useState } from 'react';
import axios from 'axios';
import Checklist from './components/Checklist';

function App() {
  const [message, setMessage] = useState('');
  const [audioUrl, setAudioUrl] = useState('');

  // Function to run the notebook
  const runNotebook = async () => {
    try {
      const response = await axios.get('http://localhost:5000/run_notebook');
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error running notebook');
    }
  };

  // Function to fetch the audio file
  const fetchAudio = async () => {
    try {
      const response = await axios.get('http://localhost:5000/audio', {
        responseType: 'blob', // Ensure the response is treated as a binary file
      });

      // Create an object URL for the audio file
      const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(audioUrl);
    } catch (error) {
      setMessage('Error fetching audio');
    }
  };

  return (
    <>
      <div style={{ position: 'relative' }}>
        <Header />
        <Resources />
        <Checklist />
      </div>

      <div className="center">
        <button className="button">Try Now</button>
        <div id="visualizer-bar">
          <AudioVisualizer />
        </div>
        <div>
          <button onClick={runNotebook}>Run Notebook</button>
          <p>{message}</p>
        </div>
        <div>
          <button onClick={fetchAudio}>Fetch and Play Audio</button>
          {audioUrl && (
            <audio controls>
              <source src={audioUrl} type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
          )}
        </div>
      </div>
    </>
  );
}

export default App;
