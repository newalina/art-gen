import html2canvas from 'html2canvas';

const captureScreenshot = () => {
    html2canvas(document.body).then(canvas => {
        const image = canvas.toDataURL('image/png');
        saveScreenshot(image); // Function needs to be implemented to save the screenshot to MongoDB
    });
};

export default captureScreenshot;
