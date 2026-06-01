chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "sendAssignment") {
        const dataToSend = request.data;

        // Send to your Python Flask server
        fetch('http://127.0.0.1:5000', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({task: dataToSend })
        })
        .then(response => {
            // Debug: See what the server actually sent back before it breaks
            console.log("Response status:", response.status); 
            return response.json();
        })
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Logged Error:', error));

    }
});
