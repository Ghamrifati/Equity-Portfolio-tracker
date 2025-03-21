/**
 * Chart components for visualizing portfolio data
 */

const chartComponents = (function() {
    // Store chart instances for later reference
    const chartInstances = {};
    
    /**
     * Create a pie chart for sector allocation
     * @param {string} canvasId - Canvas element ID
     * @param {Array} sectorData - Sector allocation data
     */
    function createSectorPieChart(canvasId, sectorData) {
      const canvas = document.getElementById(canvasId);
      if (!canvas || !sectorData) return;
      
      // Destroy existing chart if it exists
      if (chartInstances[canvasId]) {
        chartInstances[canvasId].destroy();
      }
      
      const ctx = canvas.getContext('2d');
      
      const labels = sectorData.map(item => item.sector);
      const data = sectorData.map(item => item.value);
      const backgroundColors = sectorData.map(() => helpers.getRandomColor());
      
      chartInstances[canvasId] = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: backgroundColors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                font: {
                  size: 12
                }
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const value = context.raw;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(1);
                  return `${context.label}: ${helpers.formatCurrency(value)} (${percentage}%)`;
                }
              }
            }
          }
        }
      });
      
      return chartInstances[canvasId];
    }
    
    /**
     * Create a line chart for portfolio performance
     * @param {string} canvasId - Canvas element ID
     * @param {Array} historicalData - Historical performance data
     */
    function createPerformanceLineChart(canvasId, historicalData) {
      const canvas = document.getElementById(canvasId);
      if (!canvas || !historicalData) return;
      
      // Destroy existing chart if it exists
      if (chartInstances[canvasId]) {
        chartInstances[canvasId].destroy();
      }
      
      const ctx = canvas.getContext('2d');
      
      const dates = historicalData.map(item => item.date);
      const values = historicalData.map(item => item.value);
      
      chartInstances[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [{
            label: 'Portfolio Value',
            data: values,
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              grid: {
                display: false
              }
            },
            y: {
              beginAtZero: false,
              ticks: {
                callback: function(value) {
                  return helpers.formatCurrency(value);
                }
              }
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  return helpers.formatCurrency(context.raw);
                }
              }
            }
          }
        }
      });
      
      return chartInstances[canvasId];
    }
    
    /**
     * Create a bar chart for comparing stocks
     * @param {string} canvasId - Canvas element ID
     * @param {Array} stocksData - Stocks data
     */
    function createStocksBarChart(canvasId, stocksData) {
      const canvas = document.getElementById(canvasId);
      if (!canvas || !stocksData) return;
      
      // Destroy existing chart if it exists
      if (chartInstances[canvasId]) {
        chartInstances[canvasId].destroy();
      }
      
      const ctx = canvas.getContext('2d');
      
      const labels = stocksData.map(stock => stock.symbol);
      const currentValues = stocksData.map(stock => stock.shares * stock.currentPrice);
      const costValues = stocksData.map(stock => stock.shares * stock.costBasis);
      
      chartInstances[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Current Value',
              data: currentValues,
              backgroundColor: 'rgba(76, 175, 80, 0.7)',
              borderColor: '#4CAF50',
              borderWidth: 1
            },
            {
              label: 'Cost Basis',
              data: costValues,
              backgroundColor: 'rgba(33, 150, 243, 0.7)',
              borderColor: '#2196F3',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              grid: {
                display: false
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return helpers.formatCurrency(value);
                }
              }
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  return context.dataset.label + ': ' + helpers.formatCurrency(context.raw);
                }
              }
            }
          }
        }
      });
      
      return chartInstances[canvasId];
    }
    
    // Public API
    return {
      createSectorPieChart,
      createPerformanceLineChart,
      createStocksBarChart,
      
      // Access to chart instances
      getChartInstance: function(canvasId) {
        return chartInstances[canvasId];
      },
      
      // Destroy all charts
      destroyAllCharts: function() {
        Object.values(chartInstances).forEach(chart => chart.destroy());
        Object.keys(chartInstances).forEach(key => delete chartInstances[key]);
      }
    };
  })();
  
  // Export for ES modules or CommonJS
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = chartComponents;
  } else {
    window.chartComponents = chartComponents;
  }