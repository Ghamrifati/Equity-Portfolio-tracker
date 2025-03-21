/**
 * Utility functions for the Equity Portfolio Tracker
 */

const helpers = {
    /**
     * Format a number as currency
     * @param {number} value - The value to format
     * @param {string} currencySymbol - The currency symbol to use
     * @returns {string} - Formatted currency string
     */
    formatCurrency: function(value, currencySymbol = 'DH ') {
      return currencySymbol + value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    },
    
    /**
     * Calculate percentage change between two values
     * @param {number} oldValue - Initial value
     * @param {number} newValue - Current value
     * @returns {number} - Percentage change
     */
    calculatePercentageChange: function(oldValue, newValue) {
      if (oldValue === 0) return 0;
      return ((newValue - oldValue) / Math.abs(oldValue)) * 100;
    },
    
    /**
     * Format a date object or string to a human-readable format
     * @param {Date|string} date - Date to format
     * @param {string} format - Format type ('short', 'long', 'numeric')
     * @returns {string} - Formatted date string
     */
    formatDate: function(date, format = 'short') {
      const dateObj = date instanceof Date ? date : new Date(date);
      
      switch(format) {
        case 'long':
          return dateObj.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          });
        case 'numeric':
          return dateObj.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: '2-digit', 
            day: '2-digit' 
          });
        case 'short':
        default:
          return dateObj.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
          });
      }
    },
    
    /**
     * Generate a random color
     * @returns {string} - Random hex color
     */
    getRandomColor: function() {
      return '#' + Math.floor(Math.random()*16777215).toString(16);
    }
  };
  
  // Export for ES modules or CommonJS
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = helpers;
  } else {
    window.helpers = helpers;
  }
