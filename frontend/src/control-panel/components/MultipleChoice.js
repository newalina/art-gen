import React from 'react';
import './MultipleChoice.css';

function MultipleChoice({ value, onValueChange, optionList }) {

    const hanldeOptionChange = (e) => {
        onValueChange(e.target.value);
    };

    return(
        <div className="multiple-choice-container">

            <div className='choice'>Selected Database: {value}</div>
            <form>
                {optionList.map((option, index) => (
                    <label key={index} className="option-container">
                        <input
                            type="radio"
                            name="multipleChoice"
                            value={option}
                            checked={value === option}
                            onChange={hanldeOptionChange}                         
                        />
                        {option}
                    </label>
                ))}
            </form>
        </div>
    );
}

export default MultipleChoice;