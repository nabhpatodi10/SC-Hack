import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Signup from "./components/Signup";
import Login from "./components/Login";
import Camera from "./components/Camera";
import OCRUpload from "./components/OCRUpload";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/camera" element={<Camera />} />
        <Route path="/ocr" element={<OCRUpload />} />
      </Routes>
    </Router>
  );
}

export default App;
