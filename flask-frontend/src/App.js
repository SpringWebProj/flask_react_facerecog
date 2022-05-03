import React, { Component } from "react";
import Webcam from "react-webcam";
import WebcamCapture from "./components/webcam.js";

class App extends Component {
    render() {
        return (
            <div>
                <div className="head text-center">
                    <h1>Live Face Recognition</h1>
                </div>
                <WebcamCapture />
            </div>
        );
    }
}

export default App;
