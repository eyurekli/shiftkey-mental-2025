import './styles/App.css';
import Header from './components/Header';
import AudioVisualizer from './components/AudioVisualizer';
import Resources from './components/Resources';
import React, { useState, useRef } from 'react';
import axios from 'axios';
import Checklist from './components/Checklist';

function App() {
  const [audioUrl, setAudioUrl] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recordedAudio, setRecordedAudio] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const [audioBlob, setAudioBlob] = useState(null); // New state to store the audioBlob


  const sendAudioToServer = async () => {
    if (audioBlob) {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recordedAudio.wav');
      
      try {
        const response = await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Audio uploaded successfully:', response.data);
      } catch (error) {
        console.error('Error uploading audio:', error);
      }
    }
  };

  
  // Function to fetch the audio file (existing functionality)
  const fetchAudio = async () => {
    try {
      const response = await axios.get('http://localhost:5000/audio', {
        responseType: 'blob', // Ensure the response is treated as a binary file
      });

      const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(audioUrl); // Set the audio URL state to trigger audio playback
    } catch (error) {
      console.error('Error fetching audio:', error);
    }
  };

  // Start recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setAudioBlob(audioBlob); // Save the audioBlob in the state
        const audioUrl = URL.createObjectURL(audioBlob);
        setRecordedAudio(audioUrl); // Set the recorded audio URL for playback
      };

      mediaRecorderRef.current.start();
      setIsRecording(true); // Update the recording state
    } catch (error) {
      console.error('Error starting the recording:', error);
    }
  };

  // Stop recording
  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setIsRecording(false); // Update the recording state
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
          {/* Button to trigger fetching pre-recorded audio */}
          <button onClick={fetchAudio}>Talk Now</button>

          {/* Record buttons */}
          {!isRecording ? (
            <button onClick={startRecording}>Start Recording</button>
          ) : (
            <button onClick={stopRecording}>Stop Recording</button>
          )}

          <button onClick={sendAudioToServer}>Send Audio to Server</button>


          {/* Playback the recorded audio */}
          {recordedAudio && (
            <div>
              <h3>Recorded Audio:</h3>
              <audio controls autoPlay>
                <source src={recordedAudio} type="audio/wav" />
                Your browser does not support the audio element.
              </audio>
            </div>
          )}

          {/* Display the fetched audio */}
          {audioUrl && (
            <div>
              <h3>Fetched Audio:</h3>
              <audio controls autoPlay>
                <source src={audioUrl} type="audio/mpeg" />
                Your browser does not support the audio element.
              </audio>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default App;
