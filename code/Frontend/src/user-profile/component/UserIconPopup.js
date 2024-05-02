import React, { useState, useRef, useEffect } from "react";
import { useHistory } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import "./UserIconPopup.css";
import SignupIcon from "./SignupIcon";
import UserIcon from "./UserIcon";
import { useUser } from "../../context/UserContext";

function UserIconPopup() {
  const { userInfo, isSignedIn, login, logout } = useUser();
  const history = useHistory();
  const [showPopup, setShowPopup] = useState(false);
  const popupRef = useRef();

  useEffect(() => {
    function handleClickOutside(event) {
      if (popupRef.current && !popupRef.current.contains(event.target)) {
        setShowPopup(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [popupRef]);

  const handleLoginSuccess = (credentialResponse) => {
    const decodedCredential = jwtDecode(credentialResponse.credential);
    login({
      name: decodedCredential.name,
      email: decodedCredential.email,
    });
  };

  const handleLoginFailure = () => {
    console.log("Login Failed");
    // Handle login failure
  };

  const handleSignOut = () => {
    // Here you would also ideally clear the authentication session
    logout();
    history.push("/home");
  };

  const handleGoHome = () => {
    history.push("/user", { userInfo: userInfo });
  };

  return (
    <div className="user-icon-container">
      <div
        className="user-icon"
        onClick={() => {
          setShowPopup(!showPopup);
        }}
      >
        {isSignedIn ? <UserIcon /> : <SignupIcon />}
      </div>
      {showPopup && (
        <div
          className={`user-popup ${
            isSignedIn ? "largeVersion" : "smallVersion"
          }`}
          ref={popupRef}
        >
          {isSignedIn ? <h3>My Account:</h3> : <h3>Sign in with Google</h3>}
          {isSignedIn ? (
            <div>
              <div>Name: {userInfo.name}</div>
              <div>Email: {userInfo.email}</div>
              <button
                onClick={handleGoHome}
                style={{ marginTop: "10px", borderRadius: "10px" }}
              >
                View Gallery
              </button>
              <button
                onClick={handleSignOut}
                style={{ marginTop: "10px", borderRadius: "10px" }}
              >
                Sign Out
              </button>
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
