import React, { useState, useEffect } from "react";
import "../styles/Checklist.css";
import Confetti from "react-confetti";

export default function Checklist() {
  const [showConfetti, setShowConfetti] = useState(false);

  const [items, setItems] = useState([
    { id: 1, text: "Meditate for 10 minutes", checked: false },
    { id: 2, text: "Practice breathing exercises", checked: false },
    { id: 3, text: "Take a walk outside", checked: false },
    { id: 4, text: "Offer a compliment to someone", checked: false },
    { id: 5, text: "Introduce yourself to a new person", checked: false },
    { id: 6, text: "Join a group activity or event", checked: false },
    
  ]);

  const [points, setPoints] = useState(0); // Total points
  const pointsPerLevel = 10; // Points required to level up
  const [previousLevel, setPreviousLevel] = useState(1); // Track the previous level

  const handleCheck = (id) => {
    setItems((prevItems) =>
      prevItems.map((item) =>
        item.id === id ? { ...item, checked: true } : item
      )
    );

    // Add points for completing a task
    setPoints((prevPoints) => prevPoints + 4);

    // Remove the item after a delay
    setTimeout(() => {
      setItems((prevItems) => prevItems.filter((item) => item.id !== id));
    }, 300);
  };

  const level = Math.floor(points / pointsPerLevel) + 1; // Dynamically calculate the level
  const progressPercentage = (points % pointsPerLevel) * (100 / pointsPerLevel);

  // Detect level up and trigger confetti
  useEffect(() => {
    if (level > previousLevel) {
      setShowConfetti(true); // Show confetti when leveling up
      setPreviousLevel(level); // Update the previous level
      setTimeout(() => setShowConfetti(false), 3000); // Hide confetti after 3 seconds
    }
  }, [level, previousLevel]);

  return (
    <nav id="checklist">
      {/* Confetti Effect */}
      {showConfetti && <Confetti width={window.innerWidth} height={window.innerHeight} />}

      <h3>Checklist</h3>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <label className="item">
              <input
                type="checkbox"
                onChange={() => handleCheck(item.id)}
                disabled={item.checked}
              />
              {item.text}
            </label>
          </li>
        ))}
      </ul>

      {/* Level and Progress Bar */}
      <div className="progress-container">
        <h4>Level: {level}</h4>
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progressPercentage}%` }}
          ></div>
        </div>
        <p>{progressPercentage.toFixed(0)}% to next level</p>
      </div>
    </nav>
  );
}
