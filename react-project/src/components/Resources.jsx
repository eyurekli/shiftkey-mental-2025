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
    {
      id: 1,
      text: "BounceBack Program",
      blurb: "A free, guided self-help program designed to help individuals aged 15+ manage low mood, anxiety, and stress with coaching and tools.",
      link: "https://bounceback.cmha.ca/",
    },
    {
      id: 2,
      text: "Therapists in Nova Scotia",
      blurb: "A comprehensive directory to find licensed therapists specializing in anxiety, stress, and other mental health concerns.",
      link: "https://www.psychologytoday.com/ca/therapists/nova-scotia",
    },
    {
      id: 3,
      text: "Study Focus Strategies",
      blurb: "Provides free online programs to help students develop better focus, time management, and study habits.",
      link: "https://mylearningcoach.ca/service-areas/nova-scotia/",
    },
  ];

  return (
    <>
      <nav id="resources">
        <h3>Resources</h3>
        {resources.map((resource) => (
          <div key={resource.id} className="resource-item">
            <div className="resource-header" onClick={() => toggleBlurb(resource.id)}>
              <a
                href={resource.link}
                target="_blank"
                rel="noopener noreferrer"
                className="resource-link"
              >
                {resource.text}
              </a>
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
