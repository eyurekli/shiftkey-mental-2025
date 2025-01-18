import { useState } from 'react';
import './styles/App.css';
import Header from './components/Header';
import AudioVisualizer from './components/AudioVisualizer';
import Resources from './components/Resources';

function App() {

  return (
    <>
      <Header/>  

      <Resources/>
      
      <div className="center">
        <button>Try Now</button>
        <AudioVisualizer></AudioVisualizer>

      </div>
    </>
  );
}

export default App;
