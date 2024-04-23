// import { Axios } from 'axios';
import html2canvas from 'html2canvas';

const captureScreenshot = () => {
    html2canvas(document.body).then(canvas => {
        const image = canvas.toDataURL('image/png');
        saveScreenshot(image); // Function needs to be implemented to save the screenshot to MongoDB
    });
};

const saveScreenshot = async (image) => {
    // replace with url for save-image from backend
    const response = await fetch('REPLACE WITH URL', {      
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({data: image, contentType: 'image/png'})
    }) 
    const responseData = await response.json();
    console.log(responseData.message)
}


export default {captureScreenshot, saveScreenshot};

