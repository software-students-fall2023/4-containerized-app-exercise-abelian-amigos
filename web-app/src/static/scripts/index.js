document.addEventListener("DOMContentLoaded", function () {
    // Enable the webcam on button click
    document.getElementById('enableWebcamButton').addEventListener("click", function () {
        document.getElementsByClassName('webcam')[0].style.display = 'block';
        document.getElementById('enableWebcamButton').style.display = 'none';
    });

    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const snapButton = document.getElementById('snap');
    const retryButton = document.getElementById('retry');
    const uploadButton = document.getElementById('uploadSnap');

    // Request access to the webcam
    navigator.mediaDevices.getUserMedia({video: true})
        .then(function (stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function (error) {
            console.error("Webcam not accessible", error);
        });

    // Capture the photo on button click
    snapButton.addEventListener("click", function () {
        canvas.style.display = 'block';
        video.style.display = 'none';
        context.drawImage(video, 0, 0, 640, 480);
        retryButton.style.display = 'block';
        uploadButton.style.display = 'block';
        snapButton.style.display = 'none';
    });

    // Retry button to retake the photo
    retryButton.addEventListener("click", function () {
        video.style.display = 'block';
        canvas.style.display = 'none';
        retryButton.style.display = 'none';
        uploadButton.style.display = 'none';
        snapButton.style.display = 'block';
    });

    document.getElementById('uploadSnap').addEventListener("click", function () {
        canvas.toBlob(function (blob) {
            let newImage = new File([blob], 'webcam_image.png', {
                type: 'image/png'
            });

            let dt = new DataTransfer();
            dt.items.add(newImage);
            let fileList = dt.files;

            let form = document.createElement('form');
            form.enctype = 'multipart/form-data';
            form.method = 'post';
            form.action = '/sketchify';
            form.style.display = 'none';

            let input = document.createElement('input');
            input.type = 'file';
            input.name = 'photo';
            input.files = fileList;

            form.appendChild(input);
            document.body.appendChild(form);
            form.submit();
        }, 'image/png');
    });

});