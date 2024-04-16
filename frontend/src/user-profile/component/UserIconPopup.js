import React, { useState, useRef, useEffect } from 'react';
import './UserIconPopup.css';

function UserIconPopup() {
  const [showPopup, setShowPopup] = useState(false);
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

  return (
    <div className="user-icon-container">
      <div className="user-icon" onClick={() => 
        {
          setShowPopup(!showPopup);          
        }
      }>👤</div>
      {showPopup && (
        <div className="user-popup" ref={popupRef}>
          {/* Content of the popup */}
          <h3>My Account</h3>
          <p>User name: test_user1</p>
          <p>User Email: test_user1@gmail.com</p>
        </div>
      )}
    </div>
  );
}

export default UserIconPopup;