import React, { useState } from 'react';
import './MultipleChoice.css';

function MultipleChoice() {

    const [selectedOption, setSelectedOption] = useState('None');
    const options = ['Database A', 'Database B', 'Database C', 'Database D'];

    const hanldeOptionChange = (e) => {
        setSelectedOption(e.target.value);
    };

    return(
        <div className="multiple-choice-container">

            <div className='choice'>Selected Database: {selectedOption}</div>
            <form>
                {options.map((option, index) => (
                    <label key={index} className="option-container">
                        <input
                            type="radio"
                            name="multipleChoice"
                            value={option}
                            checked={selectedOption === option}
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