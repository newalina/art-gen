import React, { useState } from 'react';
import './App.css';
import Axios from 'axios';
import { BrowserRouter as Router, Route, Redirect, Switch } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google';
import UserIconPopup from './user-profile/component/UserIconPopup'
import ImageUpload from './generator/components/ImageUpload';
import Home from './home-page/pages/Home'
import ControlPanel from './control-panel/pages/control-panel';
import UserProfile from './user-profile/pages/UserProfile'

const App = () => {

  return(
    <Router>
    <div className="app-container">
    <Switch>
      <Route path="/home" exact>
        <Home />
      </Route>

      <Route path="/controls" exact>
        <ControlPanel />
      </Route>

      <Route path="/art-play" exact>
        <h2>This is art display</h2>
      </Route>

      <Route path="/user" exact>
        <UserProfile />
      </Route>

      <Redirect to="/home" />
    </Switch>
    </div>
    </Router>
  );

};

export default App;


// function App() {
//   // potential candidate databases:
//   const databaseList = ['Database A', 'Database B', 'Database C', 'Database D'];
//   const [selectedDatabase, setSelectedDatabase] = useState('None');
//   // potential user input params:
//   const [parameter1, setParameter1] = useState(20);
//   const [parameter2, setParameter2] = useState(40);
//   const [parameter3, setParameter3] = useState(80);
//   const [file, setFile] = useState(null);
//   const [imageUrl, setImageUrl] = useState('');
//   const handleGenerateArt = async() => {
//     console.log("Art generated!");    
//     // const url = "BACKEND_ENDPOINT_URL"; // put backend endpoint url here
//     const url = "http://127.0.0.1:5000/api/slider1";   
//     // Create an object with the data you want to send
//     const data = {
//       selectedDatabase: selectedDatabase,
//       parameter1: parameter1,
//       parameter2: parameter2,
//       parameter3: parameter3
//       // other parameters goes on here...
//     };  
//     try{
//       const response = await Axios.post(url, data);
//       console.log(response);
//       setImageUrl(response.data);
//     } catch(error){
//       console.log(error);
//     }
//   }  
//   return (
//     <GoogleOAuthProvider clientId="778362968492-9u0tlr2tahg6bnbvelc16gdhib5ognhg.apps.googleusercontent.com">
//     <Router>
//       <div className="app-container">

//         <header className="header">
//           <UserIconPopup />
//           Art Generator
//         </header>

//         <article className='description'>
//           The Art Generator Project is a user-driven, web-based art generation product that provides its user with modified images 
//           and videos using real-time data centered around social causes. Users can provide input of live camera input or 
//           generic stock photos, which will be modified depending upon data relating to climate change including rising temperatures, 
//           ice melting, deforestation, rising sea levels, and wildlife exctinctions....
//         </article>

//         <main className="main-content">          

//           <section className="output">            
//             {/* Output image/video/cam will be here */}
//             {/* <h2>Upload Image Here!</h2> */}
//             {/* <ImageUpload  file={file} onFileChange={setFile}/> */}
//           </section>

//           <aside className="control-panel">

//             <h3>
//               Current Database selection: {selectedDatabase}<br />
//               Current Parameter selection:
//               Param1: {parameter1}, Param2: {parameter2}, Param3: {parameter3}
//             </h3>

//             <MultipleChoice value={selectedDatabase} onValueChange={setSelectedDatabase} optionList={databaseList}/>
//             <SliderWithInput value={parameter1} onValueChange={setParameter1}/>
//             <SliderWithInput value={parameter2} onValueChange={setParameter2}/>
//             <SliderWithInput value={parameter3} onValueChange={setParameter3}/>            

//             <button className="generate-button" onClick={handleGenerateArt}>Create Art !</button>        
//           </aside>

//         </main>
//       </div>
//     </Router>
//     </GoogleOAuthProvider>
//   );
// }

// export default App;


