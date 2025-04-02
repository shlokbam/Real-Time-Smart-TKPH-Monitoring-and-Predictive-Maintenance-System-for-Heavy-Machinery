document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    const realTimeChart = initRealTimeChart();
    // const tkphGauge = initTkphGauge();
    
    // Auto-refresh toggle
    const autoRefreshToggle = document.getElementById('autoRefreshToggle');
    let refreshInterval;
    
    // Start auto-refresh by default
    startAutoRefresh();
    
    // Refresh toggle event handler
    autoRefreshToggle.addEventListener('change', function() {
        if (this.checked) {
            startAutoRefresh();
        } else {
            stopAutoRefresh();
        }
    });
    
    // Export button handler
    document.getElementById('exportData').addEventListener('click', function() {
        exportToCSV();
    });
    
    // Functions
    function startAutoRefresh() {
        // Initial data load
        fetchTruckData();
        
        // Set up interval for refreshing data
        refreshInterval = setInterval(fetchTruckData, 3000);
    }
    
    function stopAutoRefresh() {
        clearInterval(refreshInterval);
    }
    
    function fetchTruckData() {
        const selectedTruck = document.getElementById('truckSelector').value;
        const endpoint = `/api/truck-data${selectedTruck !== 'all' ? '?truck=' + selectedTruck : ''}`;
        
        fetch(endpoint)
            .then(response => response.json())
            .then(result => {
                if (result.status === 'success') {
                    updateDashboard(result.data);
                } else {
                    console.warn('No data available or error:', result.message);
                }
            })
            .catch(error => {
                console.error('Error fetching truck data:', error);
            });
    }
    
    function updateDashboard(data) {
        if (!data || data.length === 0) return;
        
        // Get latest entry
        const latest = data[0];
        
        // Update status cards
        document.querySelector('#speedCard .status-value h3').textContent = `${latest.speed} km/h`;
        document.querySelector('#payloadCard .status-value h3').textContent = `${latest.payload.toLocaleString()} kg`;
        document.querySelector('#tkphCard .status-value h3').textContent = latest.tkph;
        
        // Update TKPH gauge
        // updateTkphGauge(latest.tkph);
        
        // Update real-time chart
        updateRealTimeChart(data);
        
        // Update data log table
        updateDataLogTable(data);
    }
    
    function calculateTireHealth(tkph) {
        // Simple formula: 100 - (tkph / 600 * 100), capped at 0-100
        const health = Math.max(0, Math.min(100, 100 - (tkph / 6)));
        return Math.round(health);
    }
    
    function updateTkphGauge(tkphValue) {
        // Update gauge value
        tkphGauge.data.datasets[0].data = [tkphValue, 600 - tkphValue];
        tkphGauge.update();
        
        // Update status badge
        const tkphStatus = document.getElementById('tkphStatus');
        let statusClass = 'bg-success';
        let statusText = 'Safe Operating Range';
        
        if (tkphValue > 300) {
            statusClass = 'bg-danger';
            statusText = 'High Heat Failure Risk';
        } else if (tkphValue > 150) {
            statusClass = 'bg-warning';
            statusText = 'High Cut Failure Risk';
        }
        
        tkphStatus.innerHTML = `<span class="badge ${statusClass}">${statusText}</span>`;
    }
    
    function updateRealTimeChart(data) {
        // Reverse data to show chronological order
        const chartData = data.slice().reverse();
        
        realTimeChart.data.labels = chartData.map(entry => `Entry ${entry.entry_no}`);
        realTimeChart.data.datasets[0].data = chartData.map(entry => entry.speed);
        realTimeChart.data.datasets[1].data = chartData.map(entry => entry.payload/1000); // Convert to tons for better scale
        realTimeChart.data.datasets[2].data = chartData.map(entry => entry.tkph);
        
        realTimeChart.update();
    }
    
    function updateDataLogTable(data) {
        const tbody = document.querySelector('#dataLogTable tbody');
        tbody.innerHTML = '';
        
        data.forEach(entry => {
            const row = document.createElement('tr');
            
            // Determine status based on TKPH
            let statusBadge = '<span class="badge bg-success">Normal</span>';
            if (entry.tkph > 300) {
                statusBadge = '<span class="badge bg-danger">Critical</span>';
            } else if (entry.tkph > 150) {
                statusBadge = '<span class="badge bg-warning">Warning</span>';
            }
            
            // Generate timestamp (mock for demo)
            const currentTime = new Date();
            const entryTime = new Date(currentTime.getTime() - (entry.entry_no * 3000));
            const timeString = entryTime.toLocaleTimeString();
            
            row.innerHTML = `
                <td>${entry.entry_no}</td>
                <td>${timeString}</td>
                <td>${entry.speed}</td>
                <td>${entry.payload.toLocaleString()}</td>
                <td>${entry.tkph}</td>
                <td>${statusBadge}</td>
            `;
            
            tbody.appendChild(row);
        });
    }
    
    function exportToCSV() {
        const table = document.getElementById('dataLogTable');
        const rows = table.querySelectorAll('tr');
        
        let csv = [];
        for (let i = 0; i < rows.length; i++) {
            const row = [], cols = rows[i].querySelectorAll('td, th');
            
            for (let j = 0; j < cols.length; j++) {
                // Get the text content and remove HTML tags
                let data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ');
                // Escape double-quotes with double-quotes
                data = data.replace(/"/g, '""');
                // Push escaped string
                row.push('"' + data + '"');
            }
            csv.push(row.join(','));
        }
        
        const csvString = csv.join('\n');
        const filename = 'truck_data_' + new Date().toISOString().slice(0, 10) + '.csv';
        const link = document.createElement('a');
        link.style.display = 'none';
        link.setAttribute('target', '_blank');
        link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvString));
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    function initRealTimeChart() {
        const ctx = document.getElementById('realTimeChart').getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Speed (km/h)',
                        data: [],
                        borderColor: '#4e73df',
                        backgroundColor: 'rgba(78, 115, 223, 0.05)',
                        tension: 0.3,
                        fill: false,
                        pointRadius: 3
                    },
                    {
                        label: 'Payload (tons)',
                        data: [],
                        borderColor: '#1cc88a',
                        backgroundColor: 'rgba(28, 200, 138, 0.05)',
                        tension: 0.3,
                        fill: false,
                        pointRadius: 3
                    },
                    {
                        label: 'TKPH',
                        data: [],
                        borderColor: '#f6c23e',
                        backgroundColor: 'rgba(246, 194, 62, 0.05)',
                        tension: 0.3,
                        fill: false,
                        pointRadius: 3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            borderDash: [2],
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                animation: {
                    duration: 300
                }
            }
        });
    }
    
    // function initTkphGauge() {
    //     const ctx = document.getElementById('tkphGauge').getContext('2d');
    //     return new Chart(ctx, {
    //         type: 'doughnut',
    //         data: {
    //             labels: ['TKPH', 'Remaining'],
    //             datasets: [{
    //                 data: [0, 600],
    //                 backgroundColor: [
    //                     '#4e73df',
    //                     '#eaecf4'
    //                 ],
    //                 borderWidth: 0,
    //                 cutout: '80%'
    //             }]
    //         },
    //         options: {
    //             responsive: true,
    //             maintainAspectRatio: false,
    //             plugins: {
    //                 legend: {
    //                     display: false
    //                 },
    //                 tooltip: {
    //                     enabled: false
    //                 },
    //                 title: {
    //                     display: true,
    //                     text: 'TKPH Gauge',
    //                     font: {
    //                         size: 16
    //                     }
    //                 }
    //             },
    //             layout: {
    //                 padding: 20
    //             }
    //         },
    //         plugins: [{
    //             id: 'gaugeText',
    //             afterDraw: (chart) => {
    //                 const {ctx, width, height, _metasets} = chart;
    //                 ctx.save();
                    
    //                 // Get TKPH value
    //                 const tkphValue = chart.data.datasets[0].data[0];
                    
    //                 // Draw value
    //                 ctx.textAlign = 'center';
    //                 ctx.textBaseline = 'middle';
    //                 ctx.font = 'bold 24px Arial';
                    
    //                 // Color based on value
    //                 if (tkphValue > 300) {
    //                     ctx.fillStyle = '#e74a3b';
    //                 } else if (tkphValue > 150) {
    //                     ctx.fillStyle = '#f6c23e';
    //                 } else {
    //                     ctx.fillStyle = '#1cc88a';
    //                 }
                    
    //                 ctx.fillText(tkphValue, width / 2, height / 2);
                    
    //                 // Draw label
    //                 ctx.font = '14px Arial';
    //                 ctx.fillStyle = '#858796';
    //                 ctx.fillText('TKPH', width / 2, height / 2 + 25);
                    
    //                 ctx.restore();
    //             }
    //         }]
    //     });
    // }
});