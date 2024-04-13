import React, { useState, useRef, useEffect } from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode";
import './UserIconPopup.css';

function UserIconPopup() {
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

  return (
    <div className="user-icon-container">
      <div className="user-icon" onClick={() => { setShowPopup(!showPopup); }}>👤</div>
      {showPopup && (
        <div className={`user-popup ${isSignedIn ? 'largeVersion' : 'smallVersion'}`} ref={popupRef}>
          <h2>My Account</h2>
          {isSignedIn ? (
            <>
              <div>Name: {userInfo.name}</div>
              <div>Email: {userInfo.email}</div>
              <button onClick={handleSignOut}>Sign Out</button>
              <button>Home</button>
            </>
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