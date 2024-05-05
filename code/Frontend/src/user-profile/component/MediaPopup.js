import React, {useEffect, useRef, useState} from 'react';
import './MediaPopup.css'

function MediaPopup(props) {
    const [docPopupOpen, setDocPopupOpen] = useState(false);
    const mediaRef = useRef(null);
    const controlIslandRef = useRef(null);

    const handleDocPopup = () => {
        setDocPopupOpen(!docPopupOpen);
    };

    const handleCloseButton = () => {
        props.closeMediaPopup();
        setDocPopupOpen(false);
    }

    const handleClickOutside = (event) => {
        if (mediaRef.current && !mediaRef.current.contains(event.target) && // click is outside media view...
            controlIslandRef.current && !controlIslandRef.current.contains(event.target)) { // and controls island
            handleCloseButton(); // close the media
        }
    };

    useEffect(() => {
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    return (
        <div className="media-popup">
            <div className="media-popup-content">
                <div className={"media-controls"} ref={controlIslandRef}>
                    <svg className={'doc-btn-icon'} onClick={handleDocPopup} width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path className={'doc-icon-path ' + (docPopupOpen ? 'doc-open' : '')} d="M30 4.5H6C4.3455 4.5 3 5.8455 3 7.5V28.5C3 30.1545 4.3455 31.5 6 31.5H30C31.6545 31.5 33 30.1545 33 28.5V7.5C33 5.8455 31.6545 4.5 30 4.5ZM6 28.5V7.5H30L30.003 28.5H6Z" fill="white"/>
                        <path className={'doc-icon-path ' + (docPopupOpen ? 'doc-open' : '')} d="M9 10.5H27V13.5H9V10.5ZM9 16.5H27V19.5H9V16.5ZM9 22.5H18V25.5H9V22.5Z" fill="white"/>
                    </svg>
                    <svg className={'close-btn-icon'} onClick={handleCloseButton} width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M5 5L19 19M5 19L19 5" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g>
                    </svg>
                </div>
                <div className={"media-player-container"} ref={mediaRef}>
                    <div className={`doc-popup ${!docPopupOpen ? "doc-popup-transparent" : ""}`}>
                        <div className={'doc-info-container'}>
                            <h5 className={'doc-info'}>Dataset: Watercolor</h5>
                            <h5 className={'doc-info'}>Setting: .0001</h5>
                            <h5 className={'doc-info'}>Setting: 6</h5>
                        </div>
                    </div>
                    {props.mediaIsVideo ?
                        (<video id="media-player" className="video-js vjs-default-skin" controls autoPlay>
                            <source className={'source'} src={props.source} type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>) :
                        (<div className="media-image">
                            <img src={props.source} />
                        </div>)
                    }
                </div>
            </div>
        </div>
    );
}

export default MediaPopup;
