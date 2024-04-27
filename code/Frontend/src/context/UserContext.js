import React, { createContext, useState, useContext } from 'react';

const UserContext = createContext();

export const useUser = () => useContext(UserContext);

export const UserProvider = ({ children }) => {
  const [userInfo, setUserInfo] = useState({});
  const [isSignedIn, setIsSignedIn] = useState(false);

  const login = (user) => {
    setUserInfo(user);
    setIsSignedIn(true);
  };

  const logout = () => {
    setUserInfo({});
    setIsSignedIn(false);
  };

  return (
    <UserContext.Provider value={{ userInfo, isSignedIn, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};
