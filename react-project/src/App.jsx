import './styles/App.css';
import Header from './components/Header';
import AudioVisualizer from './components/AudioVisualizer';
import Resources from './components/Resources';
import React, { useState } from 'react';
import axios from 'axios';
import Checklist from './components/Checklist';

function App() {
  const [audioUrl, setAudioUrl] = useState('');

  // Function to fetch the audio file
  const fetchAudio = async () => {
    try {
      const response = await axios.get('http://localhost:5000/audio', {
        responseType: 'blob', // Ensure the response is treated as a binary file
      });

      // Create an object URL for the audio file
      const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(audioUrl); // Set the audio URL state to trigger audio playback
    } catch (error) {
      console.error('Error fetching audio:', error);
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
        <div id="visualizer-bar">
          <AudioVisualizer />
        </div>
        <div>
          <button onClick={fetchAudio}>Talk Now</button>
          {audioUrl && (
            <audio controls autoPlay>
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
