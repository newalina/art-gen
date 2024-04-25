import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import './Generator.css'

const Generator = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [isRecording, setIsRecording] = useState(false)
    const [isScreenshotting, setIsScreenshotting] = useState(false)

    const cameraButtonHandler = () => {
        let currentTime = document.getElementById('media-player-g').currentTime
        console.log(currentTime)
        setIsScreenshotting(true)

        setTimeout(() => {
            setIsScreenshotting(false)
        }, "1000");

    }

    const recordButtonHandler = () => {
        let currentTime = document.getElementById('media-player-g').currentTime
        console.log(currentTime)
        if (!isRecording) {
            setIsRecording(true)
        }
        else {
            setIsRecording(false)
        }
    }


    return(
        <div className={'container'}>
            <div className="media-popup-g">
                <div className="media-popup-content-g">
                    <div className={"media-controls-g"}>
                        <svg className={'camera-icon'} onClick={cameraButtonHandler} width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M29.25 7.875H25.3519L23.4352 5.00063C23.3325 4.84671 23.1934 4.7205 23.0303 4.63318C22.8672 4.54586 22.685 4.50011 22.5 4.5H13.5C13.315 4.50011 13.1328 4.54586 12.9697 4.63318C12.8066 4.7205 12.6675 4.84671 12.5648 5.00063L10.6467 7.875H6.75C5.85489 7.875 4.99645 8.23058 4.36351 8.86351C3.73058 9.49645 3.375 10.3549 3.375 11.25V27C3.375 27.8951 3.73058 28.7536 4.36351 29.3865C4.99645 30.0194 5.85489 30.375 6.75 30.375H29.25C30.1451 30.375 31.0036 30.0194 31.6365 29.3865C32.2694 28.7536 32.625 27.8951 32.625 27V11.25C32.625 10.3549 32.2694 9.49645 31.6365 8.86351C31.0036 8.23058 30.1451 7.875 29.25 7.875ZM30.375 27C30.375 27.2984 30.2565 27.5845 30.0455 27.7955C29.8345 28.0065 29.5484 28.125 29.25 28.125H6.75C6.45163 28.125 6.16548 28.0065 5.9545 27.7955C5.74353 27.5845 5.625 27.2984 5.625 27V11.25C5.625 10.9516 5.74353 10.6655 5.9545 10.4545C6.16548 10.2435 6.45163 10.125 6.75 10.125H11.25C11.4353 10.1251 11.6177 10.0795 11.7811 9.99215C11.9445 9.90482 12.0837 9.77849 12.1866 9.62438L14.1019 6.75H21.8967L23.8134 9.62438C23.9163 9.77849 24.0555 9.90482 24.2189 9.99215C24.3823 10.0795 24.5647 10.1251 24.75 10.125H29.25C29.5484 10.125 29.8345 10.2435 30.0455 10.4545C30.2565 10.6655 30.375 10.9516 30.375 11.25V27ZM18 12.375C16.7762 12.375 15.5799 12.7379 14.5624 13.4178C13.5449 14.0977 12.7518 15.064 12.2835 16.1946C11.8152 17.3253 11.6926 18.5694 11.9314 19.7696C12.1701 20.9699 12.7594 22.0724 13.6248 22.9377C14.4901 23.8031 15.5926 24.3924 16.7929 24.6311C17.9931 24.8699 19.2372 24.7473 20.3679 24.279C21.4985 23.8107 22.4648 23.0176 23.1447 22.0001C23.8246 20.9826 24.1875 19.7863 24.1875 18.5625C24.1856 16.922 23.5331 15.3493 22.3732 14.1893C21.2132 13.0294 19.6405 12.3769 18 12.375ZM18 22.5C17.2212 22.5 16.46 22.2691 15.8124 21.8364C15.1649 21.4038 14.6602 20.7888 14.3622 20.0693C14.0642 19.3498 13.9862 18.5581 14.1382 17.7943C14.2901 17.0305 14.6651 16.3289 15.2158 15.7783C15.7664 15.2276 16.468 14.8526 17.2318 14.7007C17.9956 14.5487 18.7873 14.6267 19.5068 14.9247C20.2263 15.2227 20.8413 15.7274 21.2739 16.3749C21.7066 17.0225 21.9375 17.7837 21.9375 18.5625C21.9375 19.6068 21.5227 20.6083 20.7842 21.3467C20.0458 22.0852 19.0443 22.5 18 22.5Z" fill="white"/>
                        </svg>

                        <svg className={'record-icon'} onClick={recordButtonHandler} width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path className={'record-icon-path ' + (isRecording ? 'recording' : '')} d="M18 22.2C19.114 22.2 20.1822 21.7575 20.9699 20.9698C21.7576 20.1822 22.2 19.1139 22.2 18C22.2 16.8861 21.7576 15.8178 20.9699 15.0301C20.1822 14.2425 19.114 13.8 18 13.8C16.8861 13.8 15.8179 14.2425 15.0302 15.0301C14.2425 15.8178 13.8 16.8861 13.8 18C13.8 19.1139 14.2425 20.1822 15.0302 20.9698C15.8179 21.7575 16.8861 22.2 18 22.2Z" fill="white"/>
                            <path className={'record-icon-path ' + (isRecording ? 'recording' : '')} fill-rule="evenodd" clip-rule="evenodd" d="M32 18C32 25.7322 25.7322 32 18 32C10.2678 32 4 25.7322 4 18C4 10.2678 10.2678 4 18 4C25.7322 4 32 10.2678 32 18ZM29.2 18C29.2 20.9704 28.02 23.8192 25.9196 25.9196C23.8192 28.02 20.9704 29.2 18 29.2C15.0296 29.2 12.1808 28.02 10.0804 25.9196C7.98 23.8192 6.8 20.9704 6.8 18C6.8 15.0296 7.98 12.1808 10.0804 10.0804C12.1808 7.98 15.0296 6.8 18 6.8C20.9704 6.8 23.8192 7.98 25.9196 10.0804C28.02 12.1808 29.2 15.0296 29.2 18Z" fill="white"/>
                        </svg>

                    </div>
                    <div className={'video-js-container'}>
                        <div className={'flash-overlay ' + (isScreenshotting ? 'screenshotting' : '')}></div>
                    <video id="media-player-g" className="video-js video-js-g vjs-default-skin" controls autoPlay muted>
                        <source className={'source'} src={'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                    </div>
                </div>
            </div>

        </div>
    );
};

export default Generator;