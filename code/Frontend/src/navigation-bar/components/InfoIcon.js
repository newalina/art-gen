import React from "react";

const InfoIcon = ({ onClick }) => (
  <button
    onClick={onClick}
    style={{
      marginTop: "30px",
      fontFamily: "Space",
      fontSize: "18px",
      backgroundColor: "#737e56",
    }}
  >
    about us
  </button>
);

export default InfoIcon;
