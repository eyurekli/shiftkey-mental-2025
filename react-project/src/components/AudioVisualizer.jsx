import React, { useEffect, useRef } from "react";
import "../styles/visualizer.css"; // Corrected CSS import path

export default function AudioVisualizer() {
  const barsRef = useRef([]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      barsRef.current.forEach((bar) => {
        const randomHeight = Math.random();
        console.log(randomHeight); // Log random height for debugging
        bar.style.height = `${randomHeight * 100}%`; // Set random height
      });
    }, 100);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="visualizer">
      {Array.from({ length: 23 }).map((_, index) => (
        <div
          key={index}
          className="bar"
          ref={(el) => (barsRef.current[index] = el)}
        ></div>
      ))}
    </div>
  );
}
