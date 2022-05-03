import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import Webcam from "react-webcam";

const WebcamCapture = () => {
    const [count, setCount] = useState(0);
    const [name, setName] = useState("");
    const countRef = useRef(0);
    const webcamRef = useRef(0);
    const videoConstraints = {
        width: 200,
        height: 200,
        facingMode: "user",
    };
    useEffect(() => {
        let cam = setInterval(() => {
            setCount(countRef.current++);
            console.log(countRef.current);

            const imageSrc = webcamRef.current.getScreenshot();
            axios
                .post("http://127.0.0.1:5000/api", { data: imageSrc })
                .then((resp) => {
                    setName(resp.data);
                    if (resp.data !== "Not Found") {
                        console.log(`Found, ${resp.data}`);
                        clearInterval(cam);
                        axios
                            .post("http://127.0.0.1:5000/test", {
                                data: resp.data,
                            })
                            .then((res) => {
                                console.log(res.data);
                                axios
                                    .post(
                                        "http://127.0.0.1:8080/react/t",
                                        res.data
                                    )
                                    .then((jav) => {
                                        console.log(jav);
                                    })
                                    .catch((error) => {
                                        console.log(error);
                                    });
                                window.location.replace(
                                    "http://127.0.0.1:8080/react/t"
                                );
                            })
                            .catch((error) => {
                                console.log(error);
                            });
                    }
                })
                .catch((error) => {
                    console.log(`error = ${error}`);
                });
            if (countRef.current === 20) {
                console.log("Timeout");
                clearInterval(cam);
            }
        }, 500);
    }, []);

    // const webcamRef = React.useRef(null);
    // const videoConstraints = {
    //     width: 200,
    //     height: 200,
    //     facingMode: "user",
    // };
    // const [name, setName] = useState("");
    const capture = React.useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        console.log(`imageSrc = ${imageSrc}`);
        axios
            .post("http://127.0.0.1:5000/api", { data: imageSrc }) // post -> flask data object
            .then((res) => {
                // success get /api from flask
                console.log(`response = ${res.data}`);
                setName(res.data);
            })
            .catch((error) => {
                console.log(`error = ${error}`);
            });
    }, [webcamRef]);

    return (
        <div>
            <Webcam
                audio={false}
                height={300}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={350}
                videoConstraints={videoConstraints}
            />
            <button onClick={capture}>Click Me!</button>
            <h2>{name}</h2>
        </div>
    );
};

export default WebcamCapture;
