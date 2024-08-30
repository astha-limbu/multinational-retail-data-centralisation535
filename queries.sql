-- milestone 4
-- TASK 1 - total no of stores in each country
SELECT 
	country_code AS country, 
	COUNT(*) AS total_no_stores
FROM dim_store_details
WHERE address IS NOT NULL
GROUP BY country_code;

-- TASK 2 - Most no of stores in each location
SELECT 
	locality, 
	COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7;

-- TASK 3 - highest total sales by month
SELECT 
	CAST(SUM(p.product_price*o.product_quantity) AS DECIMAL(10,2)) AS total_sales, 
	dt.month
FROM orders_table o
JOIN dim_products p ON o.product_code = p.product_code
JOIN dim_date_times dt ON o.date_uuid = dt.date_uuid
GROUP BY dt.month
ORDER BY total_sales DESC
LIMIT 6

-- Task 4 - how many sales are happening online vs offline
SELECT 
	COUNT(o.index) AS numbers_of_sales,
	SUM(o.product_quantity) AS product_quantity_count,
	CASE
		WHEN sd.store_type = 'Web Portal' THEN 'Web'
		ELSE 'Offline'
	END AS Location
FROM orders_table o
JOIN dim_store_details sd ON sd.store_code = o.store_code
GROUP BY Location

-- Task 5 -  total and percentage of sales coming from each of the different store types
WITH 
	CTE_sales_data AS (
	SELECT 
		SUM(o.product_quantity*p.product_price) AS total_sales,
		sd.store_type
	FROM orders_table o
	JOIN dim_store_details sd ON sd.store_code = o.store_code
	JOIN dim_products p ON p.product_code = o.product_code
	GROUP BY sd.store_type
	),
	CTE_grand_total AS (
	SELECT 
		SUM(total_sales) AS grand_total_sales
	FROM CTE_sales_data
	)
SELECT 
    sd.store_type,
    sd.total_sales,
    CAST((sd.total_sales * 100.0) / gt.grand_total_sales AS DECIMAL(10,2)) AS percentage_total
FROM CTE_sales_data sd
CROSS JOIN CTE_grand_total gt
ORDER BY percentage_total DESC;


-- TASK 6 - which months in which years have had the most sales historically
SELECT 
    CAST(SUM(o.product_quantity * p.product_price) AS DECIMAL(10,2)) AS total_sales,
    ddt.year AS year,
    ddt.month AS month
FROM orders_table o
JOIN dim_products p ON p.product_code = o.product_code
JOIN dim_date_times ddt ON o.date_uuid = ddt.date_uuid
GROUP BY 
    ddt.year, 
    ddt.month
ORDER BY total_sales DESC
LIMIT 10;


-- Task 7 - overall staff numbers in each location around the world
SELECT 
    SUM(staff_numbers) AS total_staff_numbers,
    country_code
FROM dim_store_details
GROUP BY country_code
ORDER BY total_staff_numbers DESC;

-- Task 8 - Determine which type of store is generating the most sales in Germany
SELECT
	CAST(SUM(p.product_price*o.product_quantity) AS DECIMAL(10,2)) AS total_sales,
	sd.store_type,
	sd.country_code
FROM orders_table o
JOIN dim_products p ON o.product_code = p.product_code
JOIN dim_store_details sd ON o.store_code = sd.store_code
WHERE country_code = 'DE'
GROUP BY
	sd.store_type,
	sd.country_code
ORDER BY total_sales ASC

-- TASK 9 - average time taken between each sale grouped by year
WITH 
	CTE_sales_time AS (
    SELECT
        year::INT,
        month::INT,
        day::INT,
        timestamp::TIME AS sale_time,
        TO_TIMESTAMP(year || '-' || month || '-' || day || ' ' || timestamp, 'YYYY-MM-DD HH24:MI:SS') AS sale_date_time
    FROM dim_date_times
	),
	CTE_next_time AS (
    SELECT
        *,
        LEAD(sale_date_time) OVER (PARTITION BY year ORDER BY sale_date_time) AS next_sale_time
    FROM CTE_sales_time
	)
SELECT
    year,
    CONCAT(
        '"hours": ', FLOOR(AVG(EXTRACT(EPOCH FROM (next_sale_time - sale_date_time))) / 3600),
        ', "minutes": ', FLOOR((AVG(EXTRACT(EPOCH FROM (next_sale_time - sale_date_time))) % 3600) / 60),
        ', "seconds": ', FLOOR(AVG(EXTRACT(EPOCH FROM (next_sale_time - sale_date_time))) % 60),
		', "milliseconds": ', FLOOR(AVG(EXTRACT(EPOCH FROM (next_sale_time - sale_date_time))) * 1000)
    ) AS actual_time_taken
FROM CTE_next_time
WHERE next_sale_time IS NOT NULL
GROUP BY year
ORDER BY actual_time_taken DESC

