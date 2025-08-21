class EchoMetricsDashboard {
    constructor() {
        // map backend chart types to DOM element IDs
        this.chartDomMap = {
            'price_vs_sales': { img: 'price-chart-img', spinner: 'price-spinner' },
            'category_distribution': { img: 'category-chart-img', spinner: 'category-spinner' },
            'age_behavior': { img: 'behavior-chart-img', spinner: 'behavior-spinner' }
        };
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
                const targetId = e.target.getAttribute('data-bs-target'); // e.g. #price-chart
                const id = (targetId || '').replace('#', '');
                
                // map tab pane id to backend chart type
                const map = {
                    'price-chart': 'price_vs_sales',
                    'category-chart': 'category_distribution',
                    'behavior-chart': 'age_behavior'
                };

                const chartType = map[id];
                if (chartType) this.loadChart(chartType);
            });
        });
    }

    async makePrediction() {
        const form = document.getElementById('prediction-form');
        const resultDiv = document.getElementById('prediction-result');
        const valueDiv = document.getElementById('prediction-value');

        // get form data
        const formData = {
            price: parseFloat(document.getElementById('price').value),
            age: parseInt(document.getElementById('age').value, 10),
            gender: parseInt(document.getElementById('gender').value, 10),
            frequency: parseInt(document.getElementById('frequency').value, 10),
            satisfaction: parseInt(document.getElementById('satisfaction').value, 10),
            intent: parseInt(document.getElementById('intent').value, 10)
        };

        // basic validation to avoid 400s
        if (Object.values(formData).some(v => Number.isNaN(v))) {
            this.showError('Please fill all fields with valid numeric values.');
            return;
        }

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

            const result = await response.json().catch(() => ({ status: 'error', error: 'Invalid JSON response' }));

            if (!response.ok) {
                throw new Error(result?.error || `Request failed with status ${response.status}`);
            }

            if (result.status === 'success') {
                valueDiv.textContent = `$${result.prediction.toLocaleString()}`;
                resultDiv.style.display = 'block';
                resultDiv.classList.add('prediction-success');
                
                setTimeout(() => { resultDiv.classList.remove('prediction-success'); }, 500);
            } else this.showError('Prediction failed: ' + (result.error || 'Unknown error'));
        } catch (error) {
            this.showError(error?.message || 'Network error while making prediction');
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
                    
                    // determine potential level
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

    loadCharts() { this.loadChart('price_vs_sales'); } // load initial chart

    async loadChart(chartType) {
        const dom = this.chartDomMap[chartType] || {};
        const imgElement = document.getElementById(dom.img);
        const spinner = document.getElementById(dom.spinner);

        if (!imgElement || !spinner) return;

        spinner.style.display = 'block';
        imgElement.style.display = 'none';

        try {
            const response = await fetch(`/api/chart/${chartType}`);
            const result = await response.json();

            if (result.status === 'success') {
                imgElement.src = result.chart;
                imgElement.style.display = 'block';
            } else console.error('Chart loading failed:', result.error);
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

        const container = document.querySelector('.container');
        if (container) {
            const firstChild = container.firstElementChild;
            if (firstChild) {
                container.insertBefore(alertDiv, firstChild);
            } else {
                container.appendChild(alertDiv);
            }
        } else {
            document.body.prepend(alertDiv);
        }
        
        setTimeout(() => { // auto-dismiss after 5 seconds
            if (alertDiv.parentNode) { alertDiv.remove(); }
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
