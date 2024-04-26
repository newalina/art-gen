import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Redirect, Switch } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google';

import Home from './home-page/pages/Home'
import ControlPanel from './control-panel/pages/control-panel';
import UserProfile from './user-profile/pages/UserProfile'
import NavBar from './navigation-bar/components/NavBar'
import Generator from './generator/pages/Generator'


const App = () => {

  return(
    <GoogleOAuthProvider clientId="778362968492-9u0tlr2tahg6bnbvelc16gdhib5ognhg.apps.googleusercontent.com">
      <Router>
        <div className="app-container">
        <NavBar />
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

          <Route path="/generator" exact>
            <Generator />
          </Route>

          <Redirect to="/home" />
        </Switch>
        </div>
      </Router>
    </GoogleOAuthProvider>
  );

};

export default App;
