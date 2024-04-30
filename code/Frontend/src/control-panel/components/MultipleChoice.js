import React from 'react';
import './MultipleChoice.css';

function MultipleChoice({ value, onValueChange, optionList }) {

    const colors = ["blue", "red", "green", "orange", "purple"];

    const handleOptionChange = (newValue) => {
        onValueChange(newValue);
    };

    return (
        <div className="multiple-choice-container">
            <div className="circle-options">
                {optionList.map((option, index) => (
                    <div key={index} className={`circle-container ${value === option ? 'selected' : ''}`} onClick={() => handleOptionChange(option)}>
                        <div
                            className="circle"
                            style={{ backgroundColor: colors[index % colors.length] }} // Apply color based on index
                        />
                        <div className="option-name">{option}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default MultipleChoice;
