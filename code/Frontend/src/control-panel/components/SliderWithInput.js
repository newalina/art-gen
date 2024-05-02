import React from "react";
import "./SliderWithInput.css";

function SliderWithInput({ name, value, min, max, onValueChange }) {
  // Handle change from the slider
  const handleSliderChange = (event) => {
    onValueChange(event.target.value);
  };
  return (
    <div className="slider-container">
      <div className="value-display">
        {name}: {value}
      </div>

      <div className="slider-box">
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          className="slider"
          onChange={handleSliderChange}
        />
      </div>
    </div>
  );
}

export default SliderWithInput;
