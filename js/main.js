/**
 * Main application file for Equity Portfolio Tracker
 */

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', async function() {
    try {
      // Show loading state
      document.getElementById('loading').style.display = 'block';
      
      // Load portfolio data
      await dataService.loadPortfolioData();
      
      // Load historical data
      await dataService.loadHistoricalData();
      
      // Calculate portfolio metrics
      const portfolioData = dataService.getPortfolioData();
      const metrics = dataService.calculatePortfolioMetrics(portfolioData);
      const sectorAllocation = dataService.calculateSectorAllocation(portfolioData);
      
      // Initialize UI components
      uiComponents.initPortfolioSummary(metrics);
      uiComponents.createHoldingsTable(portfolioData);
      uiComponents.initAddStockForm();
      
      // Initialize charts
      chartComponents.createSectorPieChart('sector-chart', sectorAllocation);
      chartComponents.createPerformanceLineChart('performance-chart', dataService.getHistoricalData());
      chartComponents.createStocksBarChart('stocks-chart', portfolioData);
      
      // Hide loading state
      document.getElementById('loading').style.display = 'none';
      
      // Initialize event listeners for UI interaction
      initializeEventListeners();
      
    } catch (error) {
      console.error('Failed to initialize application:', error);
      document.getElementById('loading').style.display = 'none';
      document.getElementById('error-message').textContent = 'Failed to load portfolio data. Please try again later.';
      document.getElementById('error-message').style.display = 'block';
    }
  });
  
  /**
   * Initialize various event listeners
   */
  function initializeEventListeners() {
    // Toggle sidebar
    const sidebarToggle = document.getElementById('sidebar-toggle');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', function() {
        document.getElementById('sidebar').classList.toggle('collapsed');
        document.getElementById('main-content').classList.toggle('expanded');
      });
    }
    
    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        const isDarkTheme = document.body.classList.contains('dark-theme');
        localStorage.setItem('darkTheme', isDarkTheme);
        
        // Update chart themes
        updateChartThemes(isDarkTheme);
      });
      
      // Apply saved theme preference
      const savedTheme = localStorage.getItem('darkTheme');
      if (savedTheme === 'true') {
        document.body.classList.add('dark-theme');
        updateChartThemes(true);
      }
    }
    
    // Modal close buttons
    document.querySelectorAll('.close-modal').forEach(button => {
      button.addEventListener('click', function() {
        this.closest('.modal').style.display = 'none';
      });
    });
    
    // Add stock button
    const addStockBtn = document.getElementById('add-stock-btn');
    if (addStockBtn) {
      addStockBtn.addEventListener('click', function() {
        document.getElementById('add-stock-modal').style.display = 'block';
      });
    }
    
    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
      const modals = document.querySelectorAll('.modal');
      for (const modal of modals) {
        if (event.target === modal) {
          modal.style.display = 'none';
        }
      }
    });
  }
  
  /**
   * Update chart themes based on dark/light mode
   * @param {boolean} isDarkTheme - Whether dark theme is active
   */
  function updateChartThemes(isDarkTheme) {
    const chartOptions = {
      scales: {
        x: {
          grid: {
            color: isDarkTheme ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: isDarkTheme ? '#ccc' : '#666'
          }
        },
        y: {
          grid: {
            color: isDarkTheme ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: isDarkTheme ? '#ccc' : '#666'
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: isDarkTheme ? '#ccc' : '#666'
          }
        }
      }
    };
    
    // Get all chart instances
    const chartIds = ['sector-chart', 'performance-chart', 'stocks-chart'];
    
    chartIds.forEach(id => {
      const chart = chartComponents.getChartInstance(id);
      if (chart) {
        // Update options for this chart
        chart.options.scales.x.grid.color = chartOptions.scales.x.grid.color;
        chart.options.scales.x.ticks.color = chartOptions.scales.x.ticks.color;
        chart.options.scales.y.grid.color = chartOptions.scales.y.grid.color;
        chart.options.scales.y.ticks.color = chartOptions.scales.y.ticks.color;
        chart.options.plugins.legend.labels.color = chartOptions.plugins.legend.labels.color;
        
        // Update the chart
        chart.update();
      }
    });
  }