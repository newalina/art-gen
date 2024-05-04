import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import styles from "./ControlPanel.module.css";
import SliderWithInput from "../components/SliderWithInput";
import MultipleChoice from "../components/MultipleChoice";
import Axios from "axios";

const ControlPanel = () => {
  const history = useHistory();

  const databaseList = [
    "Melting Sea Ice",
    "Social Displacement",
    "Gas Levels",
    "Rising Temperatures",
    "Ocean Temperatures",
  ];
  const sliderConfigurations = {
    "Melting Sea Ice": [
      {
        name: "X-Spread",
        min: 0.0001,
        max: 0.001,
        defaultValue: 0.0001,
      },
      {
        name: "Y-Spread",
        min: 0.0001,
        max: 0.001,
        defaultValue: 0.0001,
      },
      { name: "Entropy", min: 0.999, max: 1, defaultValue: 0.999 },
      { name: "Texture", min: 0, max: 100, defaultValue: 0 },
    ],
    "Social Displacement": [
      { name: "Speed", min: 1, max: 8, defaultValue: 1 },
      { name: "Distance", min: 1, max: 5, defaultValue: 1 },
      { name: "Generation", min: 0.1, max: 1, defaultValue: 0.1 },
    ],
    "Gas Levels": [
      { name: "Density", min: 6, max: 10, defaultValue: 6 },
      { name: "Speed", min: 0.1, max: 0.5, defaultValue: 0.1 },
      { name: "Color inversion", min: 1, max: 2, defaultValue: 1 },
    ],
    "Rising Temperatures": [
      { name: "Height", min: 1, max: 3, defaultValue: 1 },
      { name: "Smoothness", min: 0.1, max: 10, defaultValue: 0.1 },
      { name: "Entropy", min: 0.1, max: 0.7, defaultValue: 0.1 },
    ],
    "Ocean Temperatures": [
      { name: "Size", min: 1, max: 5, defaultValue: 1 },
      { name: "Entropy", min: 0.1, max: 3, defaultValue: 0.1 },
      { name: "Distance", min: 0, max: 100, defaultValue: 0 },
    ],
  };
  const [selectedDatabase, setSelectedDatabase] = useState("Melting Sea Ice");
  const [mediaPopupOpen, setMediaPopupOpen] = useState(false);
  const [vidURL, setVidURL] = useState("");
  // potential user input params:
  const [parameter1, setParameter1] = useState();
  const [parameter2, setParameter2] = useState();
  const [parameter3, setParameter3] = useState();
  const [parameter4, setParameter4] = useState();

  useEffect(() => {
    const sliders = sliderConfigurations[selectedDatabase];
    if (sliders[0]) setParameter1(sliders[0].defaultValue);
    if (sliders[1]) setParameter2(sliders[1].defaultValue);
    if (sliders[2]) setParameter3(sliders[2].defaultValue);
    if (sliders[3]) setParameter4(sliders[3].defaultValue);
  }, [selectedDatabase]);

  const closeMediaPopup = () => {
    setMediaPopupOpen(false);
  };

  const handleGenerateArt = async () => {
    // Axios.get("http://10.38.171.41:80/api/artGeneration", {
    // Axios.get("http://172.20.10.4/api/artGeneration", {
    //   params: {
    //     modelSelection: 4,
    //     slider1Value: 20,
    //     slider2Value: 40,
    //     slider3Value: 80,
    //     slider4Value: 1,
    //     slider5Value: 1,
    //     slider6Value: 1,
    //   },
    // }).then((response) => {
    //   console.log(response.data.videoUrl);
    //   setVidURL(response.data.videoUrl);
    //   setMediaPopupOpen(true);
    // });

    // dummy version:
    history.push("/generator", { videoURL: vidURL });    
  };

  return (
    <div className={styles.container}>
      <h1 style={{ color: "white", fontSize: "48px" }}>Select Dataset</h1>

      {/* <h3 style={{ color: "white" }}>
        Current Database selection: {selectedDatabase}
        <br />
        just for debug: Current Parameter selection: Param1: {parameter1},
        Param2: {parameter2}, Param3: {parameter3}, Param4: {parameter4}
      </h3> */}

      <MultipleChoice
        value={selectedDatabase}
        onValueChange={setSelectedDatabase}
        optionList={databaseList}
      />

      {sliderConfigurations[selectedDatabase]?.map((sliderInfo, index) => (
        <SliderWithInput
          key={index}
          name={sliderInfo.name}
          value={
            index === 0
              ? parameter1
              : index === 1
              ? parameter2
              : index === 2
              ? parameter3
              : parameter4
          }
          min={sliderInfo.min}
          max={sliderInfo.max}
          onValueChange={
            index === 0
              ? setParameter1
              : index === 1
              ? setParameter2
              : index === 2
              ? setParameter3
              : setParameter4
          }
        />
      ))}

      <button className={styles.generateButton} onClick={handleGenerateArt}>
        generate
      </button>

      {mediaPopupOpen && (
        <div className="media-popup">
          <div className="media-popup-content">
            <div className={"media-controls"}>
              <svg
                width="36"
                height="36"
                viewBox="0 0 36 36"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M30 4.5H6C4.3455 4.5 3 5.8455 3 7.5V28.5C3 30.1545 4.3455 31.5 6 31.5H30C31.6545 31.5 33 30.1545 33 28.5V7.5C33 5.8455 31.6545 4.5 30 4.5ZM6 28.5V7.5H30L30.003 28.5H6Z"
                  fill="white"
                />
                <path
                  d="M9 10.5H27V13.5H9V10.5ZM9 16.5H27V19.5H9V16.5ZM9 22.5H18V25.5H9V22.5Z"
                  fill="white"
                />
              </svg>

              <svg
                onClick={closeMediaPopup}
                width="36"
                height="36"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g
                  id="SVGRepo_tracerCarrier"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                ></g>
                <g id="SVGRepo_iconCarrier">
                  {" "}
                  <path
                    d="M5 5L19 19M5 19L19 5"
                    stroke="#ffffff"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></path>{" "}
                </g>
              </svg>

              <svg
                width="36"
                height="36"
                viewBox="0 0 36 36"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M27 33C25.75 33 24.6875 32.5625 23.8125 31.6875C22.9375 30.8125 22.5 29.75 22.5 28.5C22.5 28.325 22.5125 28.1435 22.5375 27.9555C22.5625 27.7675 22.6 27.599 22.65 27.45L12.075 21.3C11.65 21.675 11.175 21.969 10.65 22.182C10.125 22.395 9.575 22.501 9 22.5C7.75 22.5 6.6875 22.0625 5.8125 21.1875C4.9375 20.3125 4.5 19.25 4.5 18C4.5 16.75 4.9375 15.6875 5.8125 14.8125C6.6875 13.9375 7.75 13.5 9 13.5C9.575 13.5 10.125 13.6065 10.65 13.8195C11.175 14.0325 11.65 14.326 12.075 14.7L22.65 8.55C22.6 8.4 22.5625 8.2315 22.5375 8.0445C22.5125 7.8575 22.5 7.676 22.5 7.5C22.5 6.25 22.9375 5.1875 23.8125 4.3125C24.6875 3.4375 25.75 3 27 3C28.25 3 29.3125 3.4375 30.1875 4.3125C31.0625 5.1875 31.5 6.25 31.5 7.5C31.5 8.75 31.0625 9.8125 30.1875 10.6875C29.3125 11.5625 28.25 12 27 12C26.425 12 25.875 11.894 25.35 11.682C24.825 11.47 24.35 11.176 23.925 10.8L13.35 16.95C13.4 17.1 13.4375 17.269 13.4625 17.457C13.4875 17.645 13.5 17.826 13.5 18C13.5 18.174 13.4875 18.3555 13.4625 18.5445C13.4375 18.7335 13.4 18.902 13.35 19.05L23.925 25.2C24.35 24.825 24.825 24.5315 25.35 24.3195C25.875 24.1075 26.425 24.001 27 24C28.25 24 29.3125 24.4375 30.1875 25.3125C31.0625 26.1875 31.5 27.25 31.5 28.5C31.5 29.75 31.0625 30.8125 30.1875 31.6875C29.3125 32.5625 28.25 33 27 33Z"
                  fill="white"
                />
              </svg>
            </div>
            <video
              id="media-player"
              className="video-js vjs-default-skin"
              controls
              autoPlay
            >
              <source className={"source"} src={vidURL} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      )}
    </div>
  );
};

export default ControlPanel;
