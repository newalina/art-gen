import React, { useState } from 'react';
import './App.css';
import Axios from 'axios';

import { BrowserRouter as Router, Route } from 'react-router-dom'
import SliderWithInput from './control-panel/components/SliderWithInput';
import MultipleChoice from './control-panel/components/MultipleChoice';

function App() {

  // potential candidate databases:
  const databaseList = ['Database A', 'Database B', 'Database C', 'Database D'];

  const [selectedDatabase, setSelectedDatabase] = useState('None');

  // potential user input params:
  const [parameter1, setParameter1] = useState(20);
  const [parameter2, setParameter2] = useState(40);
  const [parameter3, setParameter3] = useState(80);

  const handleGenerateArt = async() => {
    console.log("Art generated!");
    
    const url = "BACKEND_ENDPOINT_URL"; // put backend endpoint url here

    // Create an object with the data you want to send
    const data = {
      selectedDatabase: selectedDatabase,
      parameter1: parameter1,
      parameter2: parameter2,
      parameter3: parameter3
      // other parameters goes on here...
    };
  
    try{
      const response = await Axios.post(url, data);
      console.log(response);
    } catch(error){
      console.log(error);
    }

  }

  return (
    <Router>
      <div className="app-container">

        <header className="header">
          Art Generator
        </header>

        <article className='description'>
          The Art Generator Project is a user-driven, web-based art generation product that provides its user with modified images 
          and videos using real-time data centered around social causes. Users can provide input of live camera input or 
          generic stock photos, which will be modified depending upon data relating to climate change including rising temperatures, 
          ice melting, deforestation, rising sea levels, and wildlife exctinctions....
        </article>

        <main className="main-content">          

          <section className="output">            
            {/* Output image/video/cam will be here */}
          </section>

          <aside className="control-panel">

            <h3>
              Current Database selection: {selectedDatabase}<br />
              Current Parameter selection:
              Param1: {parameter1}, Param2: {parameter2}, Param3: {parameter3}
            </h3>

            <MultipleChoice value={selectedDatabase} onValueChange={setSelectedDatabase} optionList={databaseList}/>
            <SliderWithInput value={parameter1} onValueChange={setParameter1}/>
            <SliderWithInput value={parameter2} onValueChange={setParameter2}/>
            <SliderWithInput value={parameter3} onValueChange={setParameter3}/>            

            <button className="generate-button" onClick={handleGenerateArt}>Create Art !</button>        
          </aside>

        </main>
      </div>
    </Router>
  );
}

export default App;
