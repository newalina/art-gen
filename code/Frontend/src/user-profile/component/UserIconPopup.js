import React, { useState, useRef, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode";
import './UserIconPopup.css';
import SignupIcon from './SignupIcon'
import UserIcon from './userIcon';

function UserIconPopup() {
  const history = useHistory();
  const [showPopup, setShowPopup] = useState(false);
  const [isSignedIn, setIsSignedIn] = useState(false);
  const [userInfo, setUserInfo] = useState({});
  const popupRef = useRef();

  useEffect(() => {
    function handleClickOutside(event) {
      if (popupRef.current && !popupRef.current.contains(event.target)) {
        setShowPopup(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [popupRef]);

  const handleLoginSuccess = (credentialResponse) => {
    const decodedCredential = jwtDecode(credentialResponse.credential);
    // console.log(decodedCredential);    
    setIsSignedIn(true);
    setUserInfo({
      name: decodedCredential.name,
      email: decodedCredential.email,
    });
  };

  const handleLoginFailure = () => {
    console.log('Login Failed');
    // Handle login failure 
  };

  const handleSignOut = () => {
    // Here you would also ideally clear the authentication session
    setIsSignedIn(false);
    setUserInfo({});
  };

  const handleGoHome = () => {
    history.push('/user');
  }

  return (
    <div className="user-icon-container">
      <div className="user-icon" onClick={() => { setShowPopup(!showPopup); }}>
        {isSignedIn ? <UserIcon /> : <SignupIcon />}
      </div>
      {showPopup && (
        <div className={`user-popup ${isSignedIn ? 'largeVersion' : 'smallVersion'}`} ref={popupRef}>
          {isSignedIn ? (<h3>My Account:</h3>) : (<h3>Use Gmail to Sign in</h3>)}
          {isSignedIn ? (
            <div>
              <div>Name: {userInfo.name}</div>
              <div>Email: {userInfo.email}</div>
              <button onClick={handleSignOut} style={{ marginTop: '10px', borderRadius: '10px'}}>Sign Out</button>
              <button onClick={handleGoHome} style={{ marginTop: '10px', borderRadius: '10px'}}>Home</button>
            </div>
          ) : (
            <GoogleLogin
              onSuccess={handleLoginSuccess}
              onError={handleLoginFailure}
            />
          )}
        </div>
      )}
    </div>
  );
}

export default UserIconPopup;