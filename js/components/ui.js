/**
 * UI components for the Equity Portfolio Tracker
 */

const uiComponents = (function() {
    /**
     * Initialize the portfolio summary section
     * @param {Object} metrics - Portfolio metrics
     */
    function initPortfolioSummary(metrics) {
      const summaryElement = document.getElementById('portfolio-summary');
      if (!summaryElement) return;
      
      summaryElement.innerHTML = `
        <div class="summary-card">
          <h3>Total Value</h3>
          <p class="value">${helpers.formatCurrency(metrics.totalValue)}</p>
        </div>
        <div class="summary-card">
          <h3>Total Cost</h3>
          <p class="value">${helpers.formatCurrency(metrics.totalCost)}</p>
        </div>
        <div class="summary-card ${metrics.totalGain >= 0 ? 'positive' : 'negative'}">
          <h3>Total Gain/Loss</h3>
          <p class="value">${helpers.formatCurrency(metrics.totalGain)}</p>
          <p class="percentage">${metrics.gainPercentage.toFixed(2)}%</p>
        </div>
      `;
    }
    
    /**
     * Create the holdings table
     * @param {Array} portfolioData - Portfolio data
     */
    function createHoldingsTable(portfolioData) {
      const tableElement = document.getElementById('holdings-table');
      if (!tableElement || !portfolioData) return;
      
      // Clear existing table
      tableElement.innerHTML = '';
      
      // Create table header
      const tableHeader = document.createElement('thead');
      tableHeader.innerHTML = `
        <tr>
          <th>Symbol</th>
          <th>Name</th>
          <th>Sector</th>
          <th>Shares</th>
          <th>Cost Basis</th>
          <th>Current Price</th>
          <th>Current Value</th>
          <th>Gain/Loss</th>
          <th>Gain/Loss %</th>
          <th>Actions</th>
        </tr>
      `;
      tableElement.appendChild(tableHeader);
      
      // Create table body
      const tableBody = document.createElement('tbody');
      
      portfolioData.forEach(stock => {
        const currentValue = stock.shares * stock.currentPrice;
        const costBasisTotal = stock.shares * stock.costBasis;
        const gainLoss = currentValue - costBasisTotal;
        const gainLossPercentage = helpers.calculatePercentageChange(costBasisTotal, currentValue);
        
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${stock.symbol}</td>
          <td>${stock.name}</td>
          <td>${stock.sector}</td>
          <td>${stock.shares}</td>
          <td>${helpers.formatCurrency(stock.costBasis)}</td>
          <td>${helpers.formatCurrency(stock.currentPrice)}</td>
          <td>${helpers.formatCurrency(currentValue)}</td>
          <td class="${gainLoss >= 0 ? 'positive' : 'negative'}">${helpers.formatCurrency(gainLoss)}</td>
          <td class="${gainLoss >= 0 ? 'positive' : 'negative'}">${gainLossPercentage.toFixed(2)}%</td>
          <td>
            <button class="btn-edit" data-symbol="${stock.symbol}">Edit</button>
            <button class="btn-delete" data-symbol="${stock.symbol}">Delete</button>
          </td>
        `;
        
        tableBody.appendChild(row);
      });
      
      tableElement.appendChild(tableBody);
      
      // Add event listeners for edit and delete buttons
      addTableActionListeners();
    }
    
    /**
     * Add event listeners to table action buttons
     */
    function addTableActionListeners() {
      // Edit buttons
      document.querySelectorAll('.btn-edit').forEach(button => {
        button.addEventListener('click', function() {
          const symbol = this.getAttribute('data-symbol');
          openEditStockModal(symbol);
        });
      });
      
      // Delete buttons
      document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
          const symbol = this.getAttribute('data-symbol');
          if (confirm(`Are you sure you want to delete ${symbol} from your portfolio?`)) {
            deleteStock(symbol);
          }
        });
      });
    }
    
    /**
     * Open the modal to edit a stock
     * @param {string} symbol - Stock symbol
     */
    function openEditStockModal(symbol) {
      const portfolioData = dataService.getPortfolioData();
      const stock = portfolioData.find(s => s.symbol === symbol);
      
      if (!stock) return;
      
      const modal = document.getElementById('edit-stock-modal');
      const form = document.getElementById('edit-stock-form');
      
      if (!modal || !form) return;
      
      // Fill the form with stock data
      form.elements['symbol'].value = stock.symbol;
      form.elements['name'].value = stock.name;
      form.elements['sector'].value = stock.sector;
      form.elements['shares'].value = stock.shares;
      form.elements['costBasis'].value = stock.costBasis;
      form.elements['currentPrice'].value = stock.currentPrice;
      
      // Show the modal
      modal.style.display = 'block';
      
      // Update the form submission handler
      form.onsubmit = function(e) {
        e.preventDefault();
        updateStock(form);
        modal.style.display = 'none';
      };
      
      // Add a close button event listener
      document.querySelector('.close-modal').onclick = function() {
        modal.style.display = 'none';
      };
    }
    
    /**
     * Update a stock in the portfolio
     * @param {HTMLFormElement} form - The edit stock form
     */
    function updateStock(form) {
      const portfolioData = dataService.getPortfolioData();
      const symbol = form.elements['symbol'].value;
      
      const stockIndex = portfolioData.findIndex(s => s.symbol === symbol);
      if (stockIndex === -1) return;
      
      // Update the stock data
      portfolioData[stockIndex] = {
        symbol: symbol,
        name: form.elements['name'].value,
        sector: form.elements['sector'].value,
        shares: parseFloat(form.elements['shares'].value),
        costBasis: parseFloat(form.elements['costBasis'].value),
        currentPrice: parseFloat(form.elements['currentPrice'].value)
      };
      
      // Save the updated portfolio
      savePortfolio(portfolioData);
      
      // Refresh the UI
      refreshUI();
    }
    
    /**
     * Delete a stock from the portfolio
     * @param {string} symbol - Stock symbol
     */
    function deleteStock(symbol) {
      const portfolioData = dataService.getPortfolioData();
      const updatedPortfolio = portfolioData.filter(stock => stock.symbol !== symbol);
      
      // Save the updated portfolio
      savePortfolio(updatedPortfolio);
      
      // Refresh the UI
      refreshUI();
    }
    
    /**
     * Save the portfolio data
     * @param {Array} portfolioData - Updated portfolio data
     */
    function savePortfolio(portfolioData) {
      // In a real application, this would send data to a server
      // For now, we'll just update the in-memory data
      localStorage.setItem('portfolioData', JSON.stringify(portfolioData));
      
      // Update the data service
      dataService.loadPortfolioData()
        .catch(error => {
          console.error('Failed to reload portfolio data:', error);
        });
    }
    
    /**
     * Refresh the entire UI
     */
    function refreshUI() {
      const portfolioData = dataService.getPortfolioData();
      if (!portfolioData) return;
      
      const metrics = dataService.calculatePortfolioMetrics(portfolioData);
      const sectorAllocation = dataService.calculateSectorAllocation(portfolioData);
      
      // Update portfolio summary
      initPortfolioSummary(metrics);
      
      // Update holdings table
      createHoldingsTable(portfolioData);
      
      // Update charts
      chartComponents.createSectorPieChart('sector-chart', sectorAllocation);
      chartComponents.createStocksBarChart('stocks-chart', portfolioData);
      
      const historicalData = dataService.getHistoricalData();
      if (historicalData) {
        chartComponents.createPerformanceLineChart('performance-chart', historicalData);
      }
    }
    
    /**
     * Initialize the add stock form
     */
    function initAddStockForm() {
      const form = document.getElementById('add-stock-form');
      if (!form) return;
      
      form.onsubmit = function(e) {
        e.preventDefault();
        
        const newStock = {
          symbol: form.elements['symbol'].value.toUpperCase(),
          name: form.elements['name'].value,
          sector: form.elements['sector'].value,
          shares: parseFloat(form.elements['shares'].value),
          costBasis: parseFloat(form.elements['costBasis'].value),
          currentPrice: parseFloat(form.elements['currentPrice'].value)
        };
        
        addNewStock(newStock);
        form.reset();
      };
    }
    
    /**
     * Add a new stock to the portfolio
     * @param {Object} newStock - New stock data
     */
    function addNewStock(newStock) {
      const portfolioData = dataService.getPortfolioData();
      
      // Check if the stock already exists
      const existingStockIndex = portfolioData.findIndex(s => s.symbol === newStock.symbol);
      
      if (existingStockIndex !== -1) {
        if (confirm(`${newStock.symbol} already exists in your portfolio. Do you want to update it?`)) {
          portfolioData[existingStockIndex] = newStock;
        } else {
          return;
        }
      } else {
        portfolioData.push(newStock);
      }
      
      // Save the updated portfolio
      savePortfolio(portfolioData);
      
      // Refresh the UI
      refreshUI();
    }
    
    // Public API
    return {
      initPortfolioSummary,
      createHoldingsTable,
      refreshUI,
      initAddStockForm,
      openEditStockModal
    };
  })();
  
  // Export for ES modules or CommonJS
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = uiComponents;
  } else {
    window.uiComponents = uiComponents;
  }