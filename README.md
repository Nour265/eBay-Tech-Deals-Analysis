#eBay Tech Deals Analysis

Automated pipeline to scrape, clean, and analyze tech product deals from [eBay Global Deals](https://www.ebay.com/globaldeals/tech).



## Project Overview
- scraper.py – Selenium scraper collecting titles, prices, original prices, shipping info, and URLs.  
- clean_data.py – Cleans, standardizes, and computes discount metrics.  
- EDA.ipynb – Exploratory Data Analysis on cleaned data.  
- GitHub Actions – Runs every 3 hours (`cron: '0 */3 * * *'`) to update the dataset.

---

## Methodology
1. Scraping: Scrolls dynamically to load all deals and extracts product details using Selenium.  
2. Cleaning: Removes symbols from prices, fills missing values, converts data to numeric, and adds discount calculations.  
3. EDA: Analyzes hourly deal frequency, price distributions, discount trends, shipping options, and keyword frequencies.

---

## Key Insights
- Most prices are under $500; distribution is highly right-skewed.  
- Typical discounts range between 30%–60%, with a few extreme outliers (~80%).  
- Apple dominates product titles, followed by Samsung and iPhone.  
- Many items lack shipping info; “eBay International Shipping” is most common.  
- Largest markdowns appear on refurbished Apple devices.

---

## Challenges & Improvements
- Handling lazy-loaded elements and varying HTML structures.  
- Long scraping time reduced using multithreading.  
- Future work: add database storage, live dashboard, and automated cleaning workflow.

---


