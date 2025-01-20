document.getElementById("prediction-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    // Collect the input values
    const userId = document.getElementById("user_id").value;
    const symptoms = document.getElementById("symptoms").value.split(",").map(symptom => symptom.trim());
    const weight = document.getElementById("weight").value;
    const height = document.getElementById("height").value;

    // Prepare the data to send
    const data = {
        user_id: userId,
        symptoms: symptoms,
        weight: parseFloat(weight),
        height: parseFloat(height)
    };

    // Send the data to the Flask backend using fetch API
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById("result");
        if (data.error) {
            resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <h2>Prediction Result</h2>
                <p>Predicted Disease: ${data.predicted_disease}</p>
                <p>Prediction Probability: ${data.probability}</p>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = `<p class="error">An error occurred while processing your request.</p>`;
    });
});
