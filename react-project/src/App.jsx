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
  const [audioBlob, setAudioBlob] = useState(null);
  const [newMessage, setNewMessage] = useState(false);
  const [startTransition, setStartTransition] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false); // State to track if processing is happening
  const audioRef = useRef(null);

  const sendAudioToServer = async () => {
    if (audioBlob) {
      setIsProcessing(true); // Set processing state to true

      const formData = new FormData();
      formData.append('audio', audioBlob, 'recordedAudio.wav');
      
      try {
        await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Audio uploaded successfully');
      } catch (error) {
        console.error('Error uploading audio:', error);
      }

      // Clear previous audio state and fetch new audio
      setAudioUrl('');
      setRecordedAudio(null);
      await fetchAudio();

      setIsProcessing(false); // Set processing state to false after fetching audio
    }
  };

  const fetchAudio = async () => {
    try {
      const response = await axios.get('http://localhost:5000/audio', {
        responseType: 'blob',
      });

      const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(audioUrl);

      setNewMessage(true);
      setTimeout(() => setNewMessage(false), 5000);
    } catch (error) {
      console.error('Error fetching audio:', error);
    }
  };

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
        setAudioBlob(audioBlob);
        const audioUrl = URL.createObjectURL(audioBlob);
        setRecordedAudio(audioUrl);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting the recording:', error);
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  const handleAudioPlay = () => {
    setStartTransition(true);
  };

  const handleAudioPause = () => {
    setStartTransition(false);
  };

  const handleAudioEnded = () => {
    setStartTransition(false);
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
          <AudioVisualizer startTransition={startTransition} />
        </div>

        <div>
          {/* Record buttons */}
          {!isRecording ? (
            <button onClick={startRecording}>Start Recording</button>
          ) : (
            <button onClick={stopRecording}>Stop Recording</button>
          )}

          <button onClick={sendAudioToServer}>Send Message</button>

          {/* Display "Processing..." message */}
          {isProcessing && (
            <div style={{ color: 'white', fontSize: '18px', fontWeight: 'bold' }}>
              Processing...
            </div>
          )}

          {/* Display "New Message!" alert */}
          {newMessage && (
            <div style={{ color: 'white', fontSize: '18px', fontWeight: 'bold' }}>
              New Message!
            </div>
          )}

          {/* Playback the recorded audio */}
          {recordedAudio && (
            <div>
              <h3>Recorded Audio:</h3>
              <audio
                ref={audioRef}
                controls
                autoPlay
                onPlay={handleAudioPlay}
                onPause={handleAudioPause}
                onEnded={handleAudioEnded}
              >
                <source src={recordedAudio} type="audio/wav" />
                Your browser does not support the audio element.
              </audio>
            </div>
          )}

          {/* Display the fetched audio */}
          {audioUrl && (
            <div>
              <h3>Fetched Audio:</h3>
              <audio
                ref={audioRef}
                controls
                autoPlay
                onPlay={handleAudioPlay}
                onPause={handleAudioPause}
                onEnded={handleAudioEnded}
              >
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
