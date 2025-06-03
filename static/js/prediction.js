document.addEventListener('DOMContentLoaded', function() {
    // Form submission handler
    const predictionForm = document.getElementById('predictionForm');
    const resultCard = document.getElementById('resultCard');
    
    predictionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const vehicleNumber = document.getElementById('vehicleNumber').value;
        const tkphValue = parseFloat(document.getElementById('tkphValue').value);
        
        if (!vehicleNumber || isNaN(tkphValue)) {
            alert('Please enter valid values for all fields.');
            return;
        }
        
        // Show loading state
        showLoading();
        
        // Make prediction request
        fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                vehicleNumber: vehicleNumber,
                tkphValue: tkphValue
            })
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            if (data.status === 'success') {
                displayResults(data.data, vehicleNumber);
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            hideLoading();
            console.error('Error making prediction:', error);
            alert('An error occurred while making the prediction. Please try again.');
        });
    });
    
    // New Analysis button handler
    document.getElementById('newAnalysisBtn').addEventListener('click', function() {
        resultCard.classList.add('d-none');
        predictionForm.reset();
    });
    
    // Save PDF button handler (simplified - would need additional libraries for full implementation)
    document.getElementById('savePdfBtn').addEventListener('click', function() {
        alert('PDF generation would be implemented here with a library like jsPDF.');
    });
    
    // Helper functions
    function showLoading() {
        predictionForm.querySelector('button').innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Calculating...';
        predictionForm.querySelector('button').disabled = true;
    }
    
    function hideLoading() {
        predictionForm.querySelector('button').innerHTML = '<i class="fas fa-calculator"></i> Calculate Predictions';
        predictionForm.querySelector('button').disabled = false;
    }
    
    function displayResults(data, vehicleNumber) {
        // Display the vehicle number
        document.getElementById('vehicleLabel').textContent = `(${vehicleNumber})`;
        
        // Tire wear
        const tireWearProgress = document.getElementById('tireWearProgress');
        const tireWearValue = document.getElementById('tireWearValue');
        
        tireWearProgress.style.width = `${data.tire_wear}%`;
        tireWearValue.textContent = `${data.tire_wear}%`;
        
        // Set progress bar color based on wear
        if (data.tire_wear > 75) {
            tireWearProgress.className = 'progress-bar bg-danger';
        } else if (data.tire_wear > 50) {
            tireWearProgress.className = 'progress-bar bg-warning';
        } else {
            tireWearProgress.className = 'progress-bar bg-success';
        }
        
        // Remaining life
        document.getElementById('remainingLifeValue').textContent = data.remaining_life;
        
        // Fuel consumption
        document.getElementById('fuelConsumptionValue').textContent = data.fuel_consumption;
        
        // Failure risk
        const failureRiskContainer = document.getElementById('failureRiskContainer');
        let riskBadgeClass = 'bg-success';
        
        if (data.failure_risk.includes('High Heat')) {
            riskBadgeClass = 'bg-danger';
        } else if (data.failure_risk.includes('High Cut')) {
            riskBadgeClass = 'bg-warning';
        }
        
        failureRiskContainer.innerHTML = `<span class="badge ${riskBadgeClass}">${data.failure_risk}</span>`;
        
        // Maintenance alert
        const maintenanceAlertContainer = document.getElementById('maintenanceAlertContainer');
        
        if (data.maintenance_alert) {
            maintenanceAlertContainer.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i> Immediate maintenance required!
                </div>
            `;
        } else {
            maintenanceAlertContainer.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i> No maintenance required at this time
                </div>
            `;
        }
        
        // Insights
        const insightsContainer = document.getElementById('insightsContainer');
        insightsContainer.innerHTML = '';
        
        if (data.insights && data.insights.length > 0) {
            data.insights.forEach(insight => {
                let iconClass = 'info';
                
                switch (insight.type) {
                    case 'success':
                        iconClass = 'check-circle';
                        break;
                    case 'warning':
                        iconClass = 'exclamation-triangle';
                        break;
                    case 'danger':
                        iconClass = 'exclamation-circle';
                        break;
                }
                
                const insightElement = document.createElement('div');
                insightElement.className = 'insight-item';
                insightElement.innerHTML = `
                    <i class="fas fa-${iconClass} text-${insight.type}"></i>
                    <span>${insight.message}</span>
                `;
                
                insightsContainer.appendChild(insightElement);
            });
        } else {
            insightsContainer.innerHTML = '<p class="text-muted">No insights available.</p>';
        }
        
        // Show the results card
        resultCard.classList.remove('d-none');
    }
});