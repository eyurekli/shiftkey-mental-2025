import { useState } from 'react';
import './styles/App.css';
import Header from './components/Header';

function App() {

  return (
    <>
     <Header/>  
      <div className="center">

        <h3><a href="https://www.github.com" target="_blank">About Us</a></h3>
        <button>Try Now</button>
        <h3>Resources</h3>

      </div>
    </>
  );
}

export default App;
