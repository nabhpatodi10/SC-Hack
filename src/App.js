import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Signup from "./components/Signup";
import Login from "./components/Login";
import Camera from "./components/Camera";
import OCRUpload from "./components/OCRUpload";
import Loan from "./loan";
import SuccessPage from "./components/success";
import Failure from "./components/failure";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/camera" element={<Camera />} />
        <Route path="/ocr" element={<OCRUpload />} />
        <Route path="/loan" element={<Loan/>} />
        <Route path="/success" element={<SuccessPage />} />
        <Route path="/failure" element={<Failure />} />

      </Routes>
    </Router>
  );
}

export default App;
