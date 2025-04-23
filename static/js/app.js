document.getElementById("prediction-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission

    const symptoms = document.getElementById("symptoms").value;

    const data = {
        symptoms: symptoms,
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
            const markdownText = newdata.generated_text || newdata; // In case you return string directly
            const htmlContent = marked.parse(markdownText); // Convert markdown to HTML
            document.getElementById("prediction-text").innerHTML = htmlContent;
        } else {
            document.getElementById("prediction-text").innerHTML = `<p style="color:red;">Error: ${newdata.error}</p>`;
        }
    } catch (error) {
        document.getElementById("prediction-text").innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
});
