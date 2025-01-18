import { useState } from 'react';
import './styles/App.css';
import Header from './components/Header';
import AudioVisualizer from './components/AudioVisualizer';
import Resources from './components/Resources';
import AudioPlayerWithWaveform from './components/AudioPlayerWithWaveform';

function App() {

  return (
    <>
      <Header/>  

      <Resources/>
      
      <div className="center">
        <button>Try Now</button>
        <AudioVisualizer></AudioVisualizer>
        <AudioPlayerWithWaveform audioSrc="audio/takethat.mp3"/>
      </div>
    </>
  );
}

export default App;
