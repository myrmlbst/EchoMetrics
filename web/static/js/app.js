class EchoMetricsDashboard {
    constructor() {
        this.initializeEventListeners();
        this.loadAnalytics();
        this.loadScenarios();
        this.loadCharts();
    }

    initializeEventListeners() {
        // prediction form submission
        document.getElementById('prediction-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.makePrediction();
        });

        // chart tab switching
        document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
            tab.addEventListener('shown.bs.tab', (e) => {
                const chartType = e.target.getAttribute('data-bs-target').replace('#', '').replace('-chart', '');
                this.loadChart(chartType);
            });
        });
    }

    async makePrediction() {
        const form = document.getElementById('prediction-form');
        const resultDiv = document.getElementById('prediction-result');
        const valueDiv = document.getElementById('prediction-value');

        // get form data
        const formData = {
            price: document.getElementById('price').value,
            age: document.getElementById('age').value,
            gender: document.getElementById('gender').value,
            frequency: document.getElementById('frequency').value,
            satisfaction: document.getElementById('satisfaction').value,
            intent: document.getElementById('intent').value
        };

        form.classList.add('loading');
        resultDiv.style.display = 'none';

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.status === 'success') {
                valueDiv.textContent = `$${result.prediction.toLocaleString()}`;
                resultDiv.style.display = 'block';
                resultDiv.classList.add('prediction-success');
                
                setTimeout(() => {
                    resultDiv.classList.remove('prediction-success');
                }, 500);
            } else {
                this.showError('Prediction failed: ' + result.error);
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            form.classList.remove('loading');
        }
    }

    async loadAnalytics() {
        try {
            const response = await fetch('/api/analytics');
            const result = await response.json();

            if (result.status === 'success') {
                const analytics = result.analytics;
                
                document.getElementById('total-records').textContent = analytics.total_records.toLocaleString();
                document.getElementById('avg-sales').textContent = `$${analytics.avg_sales_potential.toLocaleString()}`;
                document.getElementById('max-sales').textContent = `$${analytics.max_sales_potential.toLocaleString()}`;
            }
        } catch (error) {
            console.error('Failed to load analytics:', error);
        }
    }

    async loadScenarios() {
        try {
            const response = await fetch('/api/scenarios');
            const result = await response.json();

            if (result.status === 'success') {
                const tbody = document.getElementById('scenarios-tbody');
                tbody.innerHTML = '';

                result.scenarios.forEach((scenario, index) => {
                    const row = document.createElement('tr');
                    
                    // Determine potential level
                    let potentialClass = 'text-success';
                    let potentialIcon = 'fas fa-arrow-up';
                    if (scenario.predicted_sales < 800) {
                        potentialClass = 'text-warning';
                        potentialIcon = 'fas fa-minus';
                    }
                    if (scenario.predicted_sales < 400) {
                        potentialClass = 'text-danger';
                        potentialIcon = 'fas fa-arrow-down';
                    }

                    row.innerHTML = `
                        <td><span class="badge bg-primary">${index + 1}</span></td>
                        <td>${scenario.ProductCategory}</td>
                        <td>${scenario.ProductBrand}</td>
                        <td>$${scenario.ProductPrice.toLocaleString()}</td>
                        <td><strong>$${scenario.predicted_sales.toLocaleString()}</strong></td>
                        <td><i class="${potentialIcon} ${potentialClass}"></i></td>
                    `;
                    
                    tbody.appendChild(row);
                });
            }
        } catch (error) {
            console.error('Failed to load scenarios:', error);
        }
    }

    loadCharts() {
        // load initial chart
        this.loadChart('price_vs_sales');
    }

    async loadChart(chartType) {
        const imgElement = document.getElementById(`${chartType.replace('_vs_', '-')}-chart-img`);
        const spinner = document.getElementById(`${chartType.replace('_vs_', '-')}-spinner`);

        if (!imgElement || !spinner) return;

        spinner.style.display = 'block';
        imgElement.style.display = 'none';

        try {
            const response = await fetch(`/api/chart/${chartType}`);
            const result = await response.json();

            if (result.status === 'success') {
                imgElement.src = result.chart;
                imgElement.style.display = 'block';
            } else {
                console.error('Chart loading failed:', result.error);
            }
        } catch (error) {
            console.error('Failed to load chart:', error);
        } finally {
            spinner.style.display = 'none';
        }
    }

    showError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-3';
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.row'));
        
        // auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // utility method to format numbers
    formatCurrency(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(value);
    }
}

// initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EchoMetricsDashboard();
});
