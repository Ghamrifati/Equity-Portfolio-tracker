/**
 * Data service for fetching and processing portfolio data
 */

const dataService = (function() {
    // Private variables
    let portfolioData = null;
    let historicalData = null;
    
    /**
     * Load portfolio data from JSON file
     * @returns {Promise} - Resolves with portfolio data
     */
    async function loadPortfolioData() {
      try {
        const response = await fetch('../data/portfolio.json');
        if (!response.ok) {
          throw new Error('Failed to load portfolio data');
        }
        portfolioData = await response.json();
        return portfolioData;
      } catch (error) {
        console.error('Error loading portfolio data:', error);
        throw error;
      }
    }
    
    /**
     * Load historical data from JSON file
     * @returns {Promise} - Resolves with historical data
     */
    async function loadHistoricalData() {
      try {
        const response = await fetch('../data/historical.json');
        if (!response.ok) {
          throw new Error('Failed to load historical data');
        }
        historicalData = await response.json();
        return historicalData;
      } catch (error) {
        console.error('Error loading historical data:', error);
        throw error;
      }
    }
    
    /**
     * Calculate portfolio metrics
     * @param {Array} portfolioData - Portfolio data
     * @returns {Object} - Portfolio metrics
     */
    function calculatePortfolioMetrics(portfolioData) {
      if (!portfolioData || !Array.isArray(portfolioData)) {
        return {
          totalValue: 0,
          totalCost: 0,
          totalGain: 0,
          gainPercentage: 0
        };
      }
      
      const metrics = portfolioData.reduce((acc, stock) => {
        const value = stock.shares * stock.currentPrice;
        const cost = stock.shares * stock.costBasis;
        const gain = value - cost;
        
        acc.totalValue += value;
        acc.totalCost += cost;
        acc.totalGain += gain;
        
        return acc;
      }, {
        totalValue: 0,
        totalCost: 0,
        totalGain: 0
      });
      
      metrics.gainPercentage = helpers.calculatePercentageChange(metrics.totalCost, metrics.totalValue);
      
      return metrics;
    }
    
    /**
     * Calculate sector allocation
     * @param {Array} portfolioData - Portfolio data
     * @returns {Object} - Sector allocation data
     */
    function calculateSectorAllocation(portfolioData) {
      if (!portfolioData || !Array.isArray(portfolioData)) {
        return [];
      }
      
      const sectors = {};
      const totalValue = portfolioData.reduce((sum, stock) => sum + (stock.shares * stock.currentPrice), 0);
      
      portfolioData.forEach(stock => {
        const value = stock.shares * stock.currentPrice;
        if (!sectors[stock.sector]) {
          sectors[stock.sector] = 0;
        }
        sectors[stock.sector] += value;
      });
      
      return Object.keys(sectors).map(sector => ({
        sector: sector,
        value: sectors[sector],
        percentage: (sectors[sector] / totalValue) * 100
      }));
    }
    
    // Public API
    return {
      loadPortfolioData,
      loadHistoricalData,
      calculatePortfolioMetrics,
      calculateSectorAllocation,
      
      // Getter methods
      getPortfolioData: function() {
        return portfolioData;
      },
      
      getHistoricalData: function() {
        return historicalData;
      }
    };
  })();
  
  // Export for ES modules or CommonJS
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = dataService;
  } else {
    window.dataService = dataService;
  }