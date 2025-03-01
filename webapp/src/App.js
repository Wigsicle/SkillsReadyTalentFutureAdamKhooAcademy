import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import CreateAccount from './components/CreateAccount';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/create-account" element={<CreateAccount />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
