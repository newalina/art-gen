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

navigator.mediaDevices.getDisplayMedia({ video: true })
  .then(stream => startRecording(stream))
  .catch(console.error);
