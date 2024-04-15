import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './control-panel.module.css';
import SliderWithInput from '../components/SliderWithInput'
import MultipleChoice from '../components/MultipleChoice'

const ControlPanel = () => {
    // potential candidate databases:
    const databaseList = ['Database A', 'Database B', 'Database C', 'Database D'];
    const [selectedDatabase, setSelectedDatabase] = useState('None');
    // potential user input params:
    const [parameter1, setParameter1] = useState(20);
    const [parameter2, setParameter2] = useState(40);
    const [parameter3, setParameter3] = useState(80);

    const handleGenerateArt = async() => {

    };

    return (
        <div className={styles.container}>
            <h3>
                Current Database selection: {selectedDatabase}<br />
                Current Parameter selection:
                Param1: {parameter1}, Param2: {parameter2}, Param3: {parameter3}
            </h3>

            <MultipleChoice value={selectedDatabase} onValueChange={setSelectedDatabase} optionList={databaseList}/>
            <SliderWithInput value={parameter1} onValueChange={setParameter1}/>
            <SliderWithInput value={parameter2} onValueChange={setParameter2}/>
            <SliderWithInput value={parameter3} onValueChange={setParameter3}/> 

            <button className={styles.generateButton} onClick={handleGenerateArt}>generate</button>

        </div>
    );
};

export default ControlPanel;