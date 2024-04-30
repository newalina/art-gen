import React from "react";
import './ArtDisplay.css';


function ArtDisplay(props) {


    return (
        props.isGrid ?
            (<div className="container">
                    <div id="image-grid" className={`grid-container grid`}>
                        {props.responseFromApi.map((image, index) => (
                            <div key={index} className="grid-item" onClick={() => props.openMediaPopup(image[0])}>
                                <img className="grid-item-img" src={image[0]} alt={`Image ${index}`} />
                            </div>
                        ))}
                    </div>
                </div>)
            :
                (<div className="slider">
                    <div id="px-8 slides" className="slide-track">
                        {props.responseFromApi.map((imageUrl, index) => (
                            <div key={index} className="px-8 slide text-center grid-item" onClick={() => props.openMediaPopup(imageUrl[0])}>
                                <img className="grid-item-img" src={imageUrl[0]} alt={`Image ${index}`} />
                            </div>
                        ))}
                    </div>
                </div>)
    );
}

export default ArtDisplay