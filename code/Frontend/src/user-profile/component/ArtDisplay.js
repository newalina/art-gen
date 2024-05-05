import React from "react";
import "./ArtDisplay.css";

function ArtDisplay(props) {
  return props.isGrid ? (
    <div className="container">
      <div id="image-grid" className={`grid-container grid`}>
        {props.responseFromApi.map((artwork, index) => (
          <div
            key={index}
            className="grid-item"
            onClick={() => props.openMediaPopup(artwork[0], artwork[1], artwork[2])}
          >
            <img
              className="grid-item-img"
              src={artwork[0]}
              alt={`thumbnail ${index}`}
            />
          </div>
        ))}
      </div>
    </div>
  ) : (
    <div className="slider">
      <div id="px-8 slides" className="slide-track">
        {props.responseFromApi.map((artwork, index) => (
          <div
            key={index}
            className="px-8 slide text-center slider-item"
            onClick={() => props.openMediaPopup(artwork[0], artwork[1], artwork[2])}
          >
            <img
              className="slider-item-img"
              src={artwork[0]}
              alt={`thumbnail ${index}`}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default ArtDisplay;
