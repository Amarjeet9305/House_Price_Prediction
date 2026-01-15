document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const resultArea = document.getElementById('resultArea');
    const priceDisplay = document.getElementById('priceDisplay');
    const loadingSpinner = document.getElementById('loadingSpinner');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI Feedback
        const button = form.querySelector('.cta-button');
        const originalText = button.innerText;
        button.innerText = 'Calculating...';
        button.disabled = true;

        resultArea.classList.remove('hidden');
        priceDisplay.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');

        // Gather data
        const formData = new FormData(form);
        const data = {
            bedrooms: formData.get('bedrooms'),
            bathrooms: formData.get('bathrooms'),
            sqft: formData.get('sqft'),
            floors: formData.get('floors'),
            age: formData.get('age'),
            location: formData.get('location'),
            currency: formData.get('currency'),
            waterfront: form.querySelector('#waterfront').checked,
            garage: form.querySelector('#garage').checked,
            garden: form.querySelector('#garden').checked
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            // Simulate a small delay for the "processing" feel
            setTimeout(() => {
                loadingSpinner.classList.add('hidden');
                priceDisplay.classList.remove('hidden');

                if (result.error) {
                    priceDisplay.innerText = "Error: " + result.error;
                    priceDisplay.style.fontSize = "1.2rem";
                    priceDisplay.style.color = "red";
                } else {
                    priceDisplay.innerText = result.prediction;
                    priceDisplay.style.fontSize = "2.5rem"; // Reset size

                    // Simple animation for the number
                    priceDisplay.animate([
                        { transform: 'scale(0.8)', opacity: 0 },
                        { transform: 'scale(1)', opacity: 1 }
                    ], {
                        duration: 500,
                        easing: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)'
                    });
                }

                button.innerText = originalText;
                button.disabled = false;

                // Scroll to result if needed
                resultArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 800);

        } catch (error) {
            console.error('Error:', error);
            loadingSpinner.classList.add('hidden');
            priceDisplay.classList.remove('hidden');
            priceDisplay.innerText = "An error occurred.";
            button.innerText = originalText;
            button.disabled = false;
        }
    });
});
