import React, { useState } from "react";
import "../styles/Resources.css";

export default function Resources() {
  const [openBlurbs, setOpenBlurbs] = useState({}); // Tracks which blurbs are open

  const toggleBlurb = (key) => {
    setOpenBlurbs((prevState) => ({
      ...prevState,
      [key]: !prevState[key], // Toggle the visibility of the selected blurb
    }));
  };

  const resources = [
    { id: 1, text: "", blurb: "A suite of online mental health resources available for free to post-secondary students, complementing on-campus services."},
    { id: 2, text: "Study Strategies", blurb: "Learn effective strategies to improve focus and productivity while studying." },
    { id: 3, text: "", blurb: "Explore meditation techniques to reduce stress and enhance mindfulness." },
  ];

  return (
    <>
      <nav id="resources">
        <h3>Resources</h3>
        {resources.map((resource) => (
          <div key={resource.id} className="resource-item">
            <div className="resource-header" onClick={() => toggleBlurb(resource.id)}>
              <span>{resource.text}</span>
              <span className={`arrow ${openBlurbs[resource.id] ? "open" : ""}`}>▶</span>
            </div>
            {openBlurbs[resource.id] && (
              <p className="blurb">{resource.blurb}</p>
            )}
          </div>
        ))}
      </nav>
    </>
  );
}
