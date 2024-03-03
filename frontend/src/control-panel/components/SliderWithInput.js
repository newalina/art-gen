import React, { useState } from 'react';
import './SliderWithInput.css';

function SliderWithInput() {
  
  const [value, setValue] = useState(50);

  // Handle change from the slider
  const handleSliderChange = (event) => {
    setValue(event.target.value);
  };

  // Handle change from the input box
  const handleInputChange = (event) => {
    // Ensure the value is within the 1 to 100 range
    const newValue = Math.max(1, Math.min(100, Number(event.target.value)));
    setValue(newValue);
  };

  return (
    <div className = "slider_container">
      {/* Display the current value */}
      <div className = "value_display">Parameter 1: {value}</div>
      
      {/* Slider */}
      <input
        type="range"
        min="1"
        max="100"
        value={value}
        className="slider"
        onChange={handleSliderChange}
      />
      
      {/* Input box */}
      <input
        type="number"
        value={value}
        className="number-input"
        onChange={handleInputChange}
        min="1"
        max="100"
      />
    </div>
  );
}

export default SliderWithInput;
