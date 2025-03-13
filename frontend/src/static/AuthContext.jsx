import React, { createContext, useContext, useState } from 'react';
import AuthHandler from './auth';  // Import the AuthHandler class

// Create a context for AuthHandler
const AuthContext = createContext();

// A custom hook to use AuthContext
export const useAuth = () => {
  return useContext(AuthContext);
};

// AuthProvider component that will wrap your app
export const AuthProvider = ({ children }) => {
  const [authHandler] = useState(new AuthHandler());  // Instantiate the AuthHandler
  
  return (
    <AuthContext.Provider value={authHandler}>
      {children}
    </AuthContext.Provider>
  );
};
