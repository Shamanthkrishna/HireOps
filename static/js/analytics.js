// Advanced Analytics System
class AnalyticsSystem {
    constructor() {
        this.charts = {};
        this.analyticsData = {};
        this.filters = {
            dateRange: '30d',
            department: 'all',
            jobType: 'all'
        };
        this.init();
    }

    init() {
        this.loadAnalyticsData();
        this.setupFilters();
    }

    loadAnalyticsData() {
        // Generate comprehensive sample data for demonstration
        this.analyticsData = {
            overview: {
                totalApplications: 156,
                totalHires: 12,
                averageTimeToHire: 14.5,
                conversionRate: 7.7,
                activeJobs: 8,
                trends: {
                    applications: { current: 156, previous: 134, change: 16.4 },
                    hires: { current: 12, previous: 8, change: 50.0 },
                    timeToHire: { current: 14.5, previous: 18.2, change: -20.3 },
                    conversionRate: { current: 7.7, previous: 6.0, change: 28.3 }
                }
            },
            pipeline: {
                stages: {
                    'Applied': 45,
                    'Screening': 28,
                    'Interview': 18,
                    'Technical': 12,
                    'Final Round': 8,
                    'Offer': 5,
                    'Hired': 3
                },
                conversionRates: {
                    'Applied to Screening': 62.2,
                    'Screening to Interview': 64.3,
                    'Interview to Technical': 66.7,
                    'Technical to Final': 66.7,
                    'Final to Offer': 62.5,
                    'Offer to Hire': 60.0
                }
            },
            timeToHire: {
                byStage: {
                    'Applied to Screening': { avg: 2.1, median: 2.0, p90: 4.0 },
                    'Screening to Interview': { avg: 3.8, median: 3.0, p90: 7.0 },
                    'Interview to Technical': { avg: 2.5, median: 2.0, p90: 5.0 },
                    'Technical to Final': { avg: 4.2, median: 4.0, p90: 8.0 },
                    'Final to Offer': { avg: 1.8, median: 1.0, p90: 3.0 },
                    'Offer to Hire': { avg: 3.1, median: 3.0, p90: 6.0 }
                },
                byDepartment: {
                    'Engineering': { avg: 16.5, median: 15.0, count: 8 },
                    'Marketing': { avg: 12.3, median: 11.0, count: 3 },
                    'Sales': { avg: 9.8, median: 10.0, count: 1 },
                    'Product': { avg: 18.2, median: 17.0, count: 0 }
                },
                trends: [
                    { date: '2024-01', avgDays: 18.5 },
                    { date: '2024-02', avgDays: 16.8 },
                    { date: '2024-03', avgDays: 15.2 },
                    { date: '2024-04', avgDays: 14.1 },
                    { date: '2024-05', avgDays: 13.8 },
                    { date: '2024-06', avgDays: 14.5 }
                ]
            },
            sources: {
                effectiveness: {
                    'LinkedIn': { applications: 45, interviews: 18, hires: 6, cost: 2500 },
                    'Company Website': { applications: 32, interviews: 14, hires: 4, cost: 0 },
                    'Referrals': { applications: 28, interviews: 16, hires: 8, cost: 1200 },
                    'Job Boards': { applications: 31, interviews: 8, hires: 2, cost: 800 },
                    'Recruiters': { applications: 20, interviews: 12, hires: 3, cost: 3000 }
                },
                costPerHire: {
                    'LinkedIn': 416.67,
                    'Company Website': 0,
                    'Referrals': 150.00,
                    'Job Boards': 400.00,
                    'Recruiters': 1000.00
                }
            },
            diversity: {
                gender: { 'Male': 58, 'Female': 42, 'Other': 0 },
                ethnicity: {
                    'Asian': 28,
                    'White': 45,
                    'Hispanic': 15,
                    'Black': 8,
                    'Other': 4
                },
                experience: {
                    'Entry (0-2y)': 25,
                    'Mid (3-5y)': 35,
                    'Senior (6-10y)': 30,
                    'Lead (10+y)': 10
                }
            },
            performance: {
                recruiters: [
                    { name: 'Sarah Johnson', applications: 45, hires: 5, timeToHire: 12.3, satisfaction: 4.8 },
                    { name: 'Mike Chen', applications: 38, hires: 4, timeToHire: 15.2, satisfaction: 4.6 },
                    { name: 'Lisa Rodriguez', applications: 42, hires: 3, timeToHire: 18.1, satisfaction: 4.4 },
                    { name: 'David Kim', applications: 31, hires: 2, timeToHire: 16.8, satisfaction: 4.5 }
                ],
                interviewers: [
                    { name: 'Alex Thompson', interviews: 24, avgRating: 4.2, timeSpent: 18.5 },
                    { name: 'Maria Garcia', interviews: 19, avgRating: 4.6, timeSpent: 22.1 },
                    { name: 'John Smith', interviews: 16, avgRating: 3.9, timeSpent: 15.2 }
                ]
            },
            satisfaction: {
                candidates: {
                    overall: 4.2,
                    byStage: {
                        'Application': 4.1,
                        'Screening': 4.3,
                        'Interview': 4.0,
                        'Offer': 4.5
                    },
                    feedback: [
                        { comment: 'Great communication throughout the process', rating: 5 },
                        { comment: 'Interview process was thorough but fair', rating: 4 },
                        { comment: 'Could be faster response times', rating: 3 }
                    ]
                },
                hiring_managers: {
                    overall: 4.4,
                    quality: 4.3,
                    speed: 4.1,
                    process: 4.6
                }
            }
        };
    }

    renderAnalyticsDashboard() {
        const analyticsContent = document.querySelector('.analytics-content');
        
        analyticsContent.innerHTML = `
            <!-- Analytics Filters -->
            <div class="analytics-filters">
                <div class="filter-group">
                    <label>Date Range</label>
                    <select id="date-range-filter" onchange="analyticsSystem.updateFilter('dateRange', this.value)">
                        <option value="7d">Last 7 days</option>
                        <option value="30d" selected>Last 30 days</option>
                        <option value="90d">Last 90 days</option>
                        <option value="1y">Last year</option>
                        <option value="custom">Custom range</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Department</label>
                    <select id="department-filter" onchange="analyticsSystem.updateFilter('department', this.value)">
                        <option value="all">All Departments</option>
                        <option value="engineering">Engineering</option>
                        <option value="marketing">Marketing</option>
                        <option value="sales">Sales</option>
                        <option value="product">Product</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Job Type</label>
                    <select id="job-type-filter" onchange="analyticsSystem.updateFilter('jobType', this.value)">
                        <option value="all">All Types</option>
                        <option value="full_time">Full Time</option>
                        <option value="part_time">Part Time</option>
                        <option value="contract">Contract</option>
                    </select>
                </div>
                <button class="btn btn-outline btn-sm" onclick="analyticsSystem.exportReport()">
                    <i class="fas fa-download"></i>
                    Export Report
                </button>
            </div>

            <!-- Key Metrics Overview -->
            <div class="metrics-overview">
                <h3>Key Metrics</h3>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-icon applications">
                            <i class="fas fa-inbox"></i>
                        </div>
                        <div class="metric-content">
                            <div class="metric-value">${this.analyticsData.overview.totalApplications}</div>
                            <div class="metric-label">Total Applications</div>
                            <div class="metric-trend positive">
                                <i class="fas fa-arrow-up"></i>
                                +${this.analyticsData.overview.trends.applications.change}%
                            </div>
                        </div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-icon hires">
                            <i class="fas fa-user-check"></i>
                        </div>
                        <div class="metric-content">
                            <div class="metric-value">${this.analyticsData.overview.totalHires}</div>
                            <div class="metric-label">Total Hires</div>
                            <div class="metric-trend positive">
                                <i class="fas fa-arrow-up"></i>
                                +${this.analyticsData.overview.trends.hires.change}%
                            </div>
                        </div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-icon time">
                            <i class="fas fa-clock"></i>
                        </div>
                        <div class="metric-content">
                            <div class="metric-value">${this.analyticsData.overview.averageTimeToHire}d</div>
                            <div class="metric-label">Avg Time to Hire</div>
                            <div class="metric-trend positive">
                                <i class="fas fa-arrow-down"></i>
                                ${this.analyticsData.overview.trends.timeToHire.change}%
                            </div>
                        </div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-icon conversion">
                            <i class="fas fa-percentage"></i>
                        </div>
                        <div class="metric-content">
                            <div class="metric-value">${this.analyticsData.overview.conversionRate}%</div>
                            <div class="metric-label">Conversion Rate</div>
                            <div class="metric-trend positive">
                                <i class="fas fa-arrow-up"></i>
                                +${this.analyticsData.overview.trends.conversionRate.change}%
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Charts Grid -->
            <div class="analytics-charts-grid">
                <!-- Pipeline Funnel -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h4>Hiring Pipeline</h4>
                        <button class="btn-icon" onclick="analyticsSystem.viewPipelineDetails()">
                            <i class="fas fa-expand"></i>
                        </button>
                    </div>
                    <div class="chart-container">
                        <canvas id="pipeline-chart"></canvas>
                    </div>
                </div>

                <!-- Time to Hire Trend -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h4>Time to Hire Trend</h4>
                        <div class="chart-legend">
                            <span class="legend-item">
                                <span class="legend-color" style="background: #3b82f6;"></span>
                                Average Days
                            </span>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="time-to-hire-chart"></canvas>
                    </div>
                </div>

                <!-- Source Effectiveness -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h4>Source Effectiveness</h4>
                        <select class="chart-control" onchange="analyticsSystem.updateSourceChart(this.value)">
                            <option value="hires">Hires</option>
                            <option value="conversion">Conversion Rate</option>
                            <option value="cost">Cost per Hire</option>
                        </select>
                    </div>
                    <div class="chart-container">
                        <canvas id="source-effectiveness-chart"></canvas>
                    </div>
                </div>

                <!-- Diversity Metrics -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h4>Diversity & Inclusion</h4>
                        <div class="chart-tabs">
                            <button class="chart-tab active" onclick="analyticsSystem.showDiversityChart('gender')">Gender</button>
                            <button class="chart-tab" onclick="analyticsSystem.showDiversityChart('ethnicity')">Ethnicity</button>
                            <button class="chart-tab" onclick="analyticsSystem.showDiversityChart('experience')">Experience</button>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="diversity-chart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Performance Tables -->
            <div class="performance-section">
                <div class="analytics-card">
                    <div class="card-header">
                        <h4>Recruiter Performance</h4>
                        <button class="btn btn-outline btn-sm" onclick="analyticsSystem.exportRecruiterReport()">
                            <i class="fas fa-download"></i>
                            Export
                        </button>
                    </div>
                    <div class="table-container">
                        <table class="performance-table">
                            <thead>
                                <tr>
                                    <th>Recruiter</th>
                                    <th>Applications</th>
                                    <th>Hires</th>
                                    <th>Success Rate</th>
                                    <th>Avg Time to Hire</th>
                                    <th>Satisfaction</th>
                                    <th>Performance</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${this.analyticsData.performance.recruiters.map(recruiter => `
                                    <tr>
                                        <td>
                                            <div class="recruiter-info">
                                                <div class="recruiter-avatar">${recruiter.name.split(' ').map(n => n[0]).join('')}</div>
                                                <span>${recruiter.name}</span>
                                            </div>
                                        </td>
                                        <td>${recruiter.applications}</td>
                                        <td>${recruiter.hires}</td>
                                        <td>${((recruiter.hires / recruiter.applications) * 100).toFixed(1)}%</td>
                                        <td>${recruiter.timeToHire} days</td>
                                        <td>
                                            <div class="rating-stars">
                                                ${this.renderStars(recruiter.satisfaction)}
                                                <span>${recruiter.satisfaction}</span>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="performance-indicator ${this.getPerformanceLevel(recruiter)}">
                                                ${this.getPerformanceLevel(recruiter)}
                                            </div>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Insights & Recommendations -->
            <div class="insights-section">
                <div class="analytics-card">
                    <div class="card-header">
                        <h4>AI-Powered Insights</h4>
                        <span class="insights-badge">Beta</span>
                    </div>
                    <div class="insights-content">
                        ${this.generateInsights()}
                    </div>
                </div>
            </div>
        `;

        // Initialize charts after DOM is ready
        setTimeout(() => {
            this.initializeCharts();
        }, 100);
    }

    initializeCharts() {
        this.createPipelineChart();
        this.createTimeToHireChart();
        this.createSourceEffectivenessChart();
        this.createDiversityChart('gender');
    }

    createPipelineChart() {
        const ctx = document.getElementById('pipeline-chart').getContext('2d');
        const data = this.analyticsData.pipeline.stages;
        
        this.charts.pipeline = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Candidates',
                    data: Object.values(data),
                    backgroundColor: [
                        '#3b82f6', '#6366f1', '#8b5cf6', 
                        '#a855f7', '#c084fc', '#d8b4fe', '#e9d5ff'
                    ],
                    borderRadius: 6,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            afterLabel: (context) => {
                                const stage = context.label;
                                const nextStage = Object.keys(data)[context.dataIndex + 1];
                                if (nextStage) {
                                    const conversionKey = `${stage} to ${nextStage}`;
                                    const rate = this.analyticsData.pipeline.conversionRates[conversionKey];
                                    return rate ? `Conversion: ${rate}%` : '';
                                }
                                return '';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#f1f5f9'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    createTimeToHireChart() {
        const ctx = document.getElementById('time-to-hire-chart').getContext('2d');
        const data = this.analyticsData.timeToHire.trends;
        
        this.charts.timeToHire = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => {
                    const date = new Date(d.date);
                    return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
                }),
                datasets: [{
                    label: 'Average Time to Hire (days)',
                    data: data.map(d => d.avgDays),
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: '#f1f5f9'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + 'd';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    createSourceEffectivenessChart() {
        const ctx = document.getElementById('source-effectiveness-chart').getContext('2d');
        const data = this.analyticsData.sources.effectiveness;
        
        this.charts.sourceEffectiveness = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    data: Object.values(data).map(source => source.hires),
                    backgroundColor: [
                        '#3b82f6', '#10b981', '#f59e0b', 
                        '#ef4444', '#8b5cf6'
                    ],
                    borderWidth: 0,
                    cutout: '60%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            afterLabel: (context) => {
                                const source = context.label;
                                const sourceData = data[source];
                                const conversion = ((sourceData.hires / sourceData.applications) * 100).toFixed(1);
                                return [`Applications: ${sourceData.applications}`, `Conversion: ${conversion}%`];
                            }
                        }
                    }
                }
            }
        });
    }

    createDiversityChart(type = 'gender') {
        const ctx = document.getElementById('diversity-chart');
        if (!ctx) return;
        
        if (this.charts.diversity) {
            this.charts.diversity.destroy();
        }
        
        const data = this.analyticsData.diversity[type];
        
        this.charts.diversity = new Chart(ctx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    data: Object.values(data),
                    backgroundColor: [
                        '#3b82f6', '#10b981', '#f59e0b', 
                        '#ef4444', '#8b5cf6', '#06b6d4'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.raw / total) * 100).toFixed(1);
                                return `${context.label}: ${context.raw} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Chart interaction methods
    showDiversityChart(type) {
        // Update tab appearance
        document.querySelectorAll('.chart-tab').forEach(tab => tab.classList.remove('active'));
        event.target.classList.add('active');
        
        // Create new chart
        this.createDiversityChart(type);
    }

    updateSourceChart(metric) {
        if (!this.charts.sourceEffectiveness) return;
        
        const data = this.analyticsData.sources.effectiveness;
        let values;
        
        switch (metric) {
            case 'hires':
                values = Object.values(data).map(source => source.hires);
                break;
            case 'conversion':
                values = Object.values(data).map(source => 
                    ((source.hires / source.applications) * 100).toFixed(1)
                );
                break;
            case 'cost':
                values = Object.values(this.analyticsData.sources.costPerHire);
                break;
        }
        
        this.charts.sourceEffectiveness.data.datasets[0].data = values;
        this.charts.sourceEffectiveness.update();
    }

    // Helper methods
    renderStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let stars = '';
        
        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star"></i>';
        }
        
        if (hasHalfStar) {
            stars += '<i class="fas fa-star-half-alt"></i>';
        }
        
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        for (let i = 0; i < emptyStars; i++) {
            stars += '<i class="far fa-star"></i>';
        }
        
        return stars;
    }

    getPerformanceLevel(recruiter) {
        const successRate = (recruiter.hires / recruiter.applications) * 100;
        
        if (successRate >= 15) return 'excellent';
        if (successRate >= 10) return 'good';
        if (successRate >= 5) return 'average';
        return 'needs-improvement';
    }

    generateInsights() {
        return `
            <div class="insights-list">
                <div class="insight-item positive">
                    <div class="insight-icon">
                        <i class="fas fa-trending-up"></i>
                    </div>
                    <div class="insight-content">
                        <h5>Referral Program Success</h5>
                        <p>Your employee referral program shows the highest conversion rate at 28.6%. Consider expanding referral incentives to boost quality applications.</p>
                    </div>
                </div>
                
                <div class="insight-item warning">
                    <div class="insight-icon">
                        <i class="fas fa-clock"></i>
                    </div>
                    <div class="insight-content">
                        <h5>Interview Bottleneck</h5>
                        <p>Average time from interview to offer is 4.2 days, 40% longer than industry average. Consider streamlining decision-making process.</p>
                    </div>
                </div>
                
                <div class="insight-item info">
                    <div class="insight-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="insight-content">
                        <h5>Diversity Opportunity</h5>
                        <p>Female representation in technical roles is below target (28% vs 40% goal). Focus outreach on diverse technical communities.</p>
                    </div>
                </div>
                
                <div class="insight-item positive">
                    <div class="insight-icon">
                        <i class="fas fa-star"></i>
                    </div>
                    <div class="insight-content">
                        <h5>Candidate Experience</h5>
                        <p>Candidate satisfaction scores improved 15% this quarter. Your interview process improvements are paying off!</p>
                    </div>
                </div>
            </div>
        `;
    }

    // Filter and export methods
    updateFilter(filterType, value) {
        this.filters[filterType] = value;
        dashboard.showNotification(`Filter updated: ${filterType} = ${value}`, 'info');
        
        // In a real app, this would refetch data and update charts
        // For demo, we'll show the notification
    }

    exportReport() {
        dashboard.showNotification('Generating analytics report... This will be available shortly.', 'info');
        
        // Simulate report generation
        setTimeout(() => {
            dashboard.showNotification('Analytics report exported successfully!', 'success');
        }, 2000);
    }

    exportRecruiterReport() {
        dashboard.showNotification('Exporting recruiter performance report...', 'info');
        
        setTimeout(() => {
            dashboard.showNotification('Recruiter report exported successfully!', 'success');
        }, 1500);
    }

    viewPipelineDetails() {
        dashboard.showNotification('Detailed pipeline analysis - Feature in development', 'info');
    }

    setupFilters() {
        // Initialize filter event listeners and default states
        // This would typically connect to backend filtering
    }
}

// Initialize analytics system
window.analyticsSystem = new AnalyticsSystem();