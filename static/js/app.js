document.getElementById("prediction-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    // Collect the input values
    const symptoms = document.getElementById("symptoms").value.split(",").map(symptom => symptom.trim());
    const weight = document.getElementById("weight").value;
    const height = document.getElementById("height").value;

    // Prepare the data to send
    const data = {
        symptoms: symptoms,
        weight: parseFloat(weight),
        height: parseFloat(height)
    };
    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const newdata = await response.json();
        if (response.ok) {
            document.getElementById("result").innerHTML = `
                <h3>Predicted Disease: ${newdata.generated_text}</h3>
                
            `;
        } else {
            document.getElementById("result").innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById("result").innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
});
