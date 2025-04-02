document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            mainContent.classList.toggle('sidebar-active');
        });
    }
    
    // History modal handler
    const historyLinks = document.querySelectorAll('.history-link');
    const historyModal = new bootstrap.Modal(document.getElementById('historyModal'));
    
    historyLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            loadHistoryData();
            historyModal.show();
        });
    });
    
    // Load history data function
    function loadHistoryData() {
        fetch('/api/history')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const tableBody = document.querySelector('#historyTable tbody');
                    tableBody.innerHTML = '';
                    
                    data.data.forEach(item => {
                        const row = document.createElement('tr');
                        
                        row.innerHTML = `
                            <td>${item['Vehicle Number']}</td>
                            <td>${item['TKPH Value']}</td>
                            <td>${item['Tire Wear (%)'].toFixed(2)}%</td>
                            <td>${item['Remaining Life (Hours)'].toFixed(2)}</td>
                            <td>${item['Fuel Consumption (L/h)'].toFixed(2)}</td>
                            <td>${item['Failure Risk']}</td>
                            <td>${item['Maintenance Alert'] ? 
                                '<span class="badge bg-danger">Required</span>' : 
                                '<span class="badge bg-success">Not Required</span>'
                            }</td>
                        `;
                        
                        tableBody.appendChild(row);
                    });
                } else {
                    const tableBody = document.querySelector('#historyTable tbody');
                    tableBody.innerHTML = `
                        <tr>
                            <td colspan="7" class="text-center">No history data available</td>
                        </tr>
                    `;
                }
            })
            .catch(error => {
                console.error('Error loading history:', error);
            });
    }
});