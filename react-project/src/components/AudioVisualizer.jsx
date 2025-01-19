import React, { useEffect, useRef } from "react";
import "../styles/visualizer.css"; // Corrected CSS import path

export default function AudioVisualizer({ startTransition, startAnimation, stopAnimation }) {
  const barsRef = useRef([]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      if (startTransition) {
        // If the animation is active, update the bar heights randomly
        barsRef.current.forEach((bar) => {
          const randomHeight = Math.random();
          bar.style.height = `${randomHeight * 60}%`; // Set random height on transition
        });
      } else {
        // If the animation is stopped, reset the height to 10px
        barsRef.current.forEach((bar) => {
          bar.style.height = "10px"; // Reset to default height
        });
      }
    }, 100);

    return () => clearInterval(intervalId); // Clean up the interval when the component unmounts or startTransition changes
  }, [startTransition]);

  return (
    <div>
      {/* Buttons to start and stop the animation 
      <button onClick={startAnimation}>Start Animation</button>
      <button onClick={stopAnimation}>Stop Animation</button>*/}
      
      <div className="visualizer">
        {Array.from({ length: 30 }).map((_, index) => (
          <div
            key={index}
            className="bar"
            ref={(el) => (barsRef.current[index] = el)}
            style={{ height: "10px" }} // Initially set height to 10px
          ></div>
        ))}
      </div>
    </div>
  );
}
