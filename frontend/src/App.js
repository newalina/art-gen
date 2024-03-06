import React from 'react';
import './App.css';
import Axios from 'axios';

import { BrowserRouter as Router, Route } from 'react-router-dom'
import SliderWithInput from './control-panel/components/SliderWithInput';
import MultipleChoice from './control-panel/components/MultipleChoice';

function App() {

  const handleGenerateArt = async() => {
    console.log("Art generated!");
    
    const url = "BACKEND_ENDPOINT_URL"; // put backend endpoint url here

    // Create an object with the data you want to send
    const data = {
      parameter1: 55.5,
      parameter2: 33.3,
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
            <MultipleChoice />
            <SliderWithInput />
            <SliderWithInput />
            <SliderWithInput />
            <SliderWithInput />

            <button className="generate-button" onClick={handleGenerateArt}>Create Art !</button>        
          </aside>

        </main>
      </div>
    </Router>
  );
}

export default App;
