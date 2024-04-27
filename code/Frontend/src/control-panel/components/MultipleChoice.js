import React from 'react';
import './MultipleChoice.css';

function MultipleChoice({ value, onValueChange, optionList }) {

    const handleOptionChange = (newValue) => {
        onValueChange(newValue);
    };

    return (
        <div className="multiple-choice-container">
            <div className='choice'></div>
            <div className="circle-options">
                {optionList.map((option, index) => (
                    <div
                        key={index}
                        className={`circle ${value === index ? 'selected' : ''}`}
                        style={{ backgroundColor: option }}
                        onClick={() => handleOptionChange(index)}
                    />
                ))}
            </div>
        </div>
    );
}

export default MultipleChoice;
