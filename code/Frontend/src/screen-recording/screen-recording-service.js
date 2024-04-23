let mediaRecorder;
let recordedChunks = [];

function startRecording(stream) {
    mediaRecorder = new mediaRecorder(stream);

    mediaRecorder.ondataavailable = function(e) {
        if (e.data.size > 0) {
            recordedChunks.push(e.data);
        }

        mediaRecorder.onstop = saveRecording; // Function needs to be implemented to save the recording to MongoDB
        mediaRecorder.start();
    };
}

function saveRecording() {
    const blob = new Blob(recordedChunks, {
        type: 'video/webm',
    });

    const formData = new FormData();
    formData.append('video', blob);

    // replace with url for save-image from backend
    fetch('REPLACE WITH URL', {
        method: 'POST',
        
    })

}

navigator.mediaDevices.getDisplayMedia({ video: true })
  .then(stream => startRecording(stream))
  .catch(console.error);
