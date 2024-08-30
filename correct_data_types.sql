-- Milestone 3 
-- Task 1 - orders_table
SELECT 
    MAX(CHAR_LENGTH(card_number::TEXT)) AS max_card_number_len,
    MAX(CHAR_LENGTH(store_code::TEXT)) AS max_store_code_len,
    MAX(CHAR_LENGTH(product_code::TEXT)) AS max_product_code_len
FROM orders_table;

ALTER TABLE orders_table
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    ALTER COLUMN card_number TYPE VARCHAR(19),
    ALTER COLUMN store_code TYPE VARCHAR(12),
    ALTER COLUMN product_code TYPE VARCHAR(11),
    ALTER COLUMN product_quantity TYPE SMALLINT USING product_quantity::SMALLINT;

-- task 2 - dim_users
SELECT 
    MAX(CHAR_LENGTH(country_code)) AS max_country_code_len
FROM dim_users;

ALTER TABLE dim_users
	ALTER COLUMN first_name TYPE VARCHAR(255),
	ALTER COLUMN last_name TYPE VARCHAR(255),
	ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE,
	ALTER COLUMN country_code TYPE VARCHAR(3),
	ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
	ALTER COLUMN join_date TYPE DATE USING join_date::DATE;


-- Task 3 - dim_store_details
UPDATE dim_store_details
SET longitude = NULL,
	locality = NULL,
	latitude = NULL,
	lat = NULL,
	address = NULL
WHERE Index = 0;

UPDATE dim_store_details
SET latitude = COALESCE(CAST(lat AS FLOAT), CAST(latitude AS FLOAT));

ALTER TABLE dim_store_details
	DROP COLUMN IF EXISTS lat;
	
ALTER TABLE dim_store_details
	ALTER COLUMN longitude TYPE FLOAT USING longitude::FLOAT,
	ALTER COLUMN locality TYPE VARCHAR(255),
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
	ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
	ALTER COLUMN store_type TYPE VARCHAR(255),
	ALTER COLUMN latitude TYPE FLOAT USING latitude::FLOAT,
	ALTER COLUMN country_code TYPE VARCHAR(3),
	ALTER COLUMN continent TYPE VARCHAR(255);


-- Task 4 - prep products table
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '');


ALTER TABLE dim_products
	ADD COLUMN weight_class VARCHAR(20);

UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
    WHEN weight >= 140 THEN 'Truck_Required'
END;


-- Task 5 - dim_products
ALTER TABLE dim_products RENAME COLUMN removed TO still_available;

SELECT MAX(CHAR_LENGTH("EAN")) AS max_ean_length,
       MAX(CHAR_LENGTH(product_code)) AS max_product_code_length,
       MAX(CHAR_LENGTH(weight_class)) AS max_weight_class_length
FROM dim_products;

ALTER TABLE dim_products
	ALTER COLUMN product_price TYPE FLOAT USING product_price::FLOAT,
	ALTER COLUMN weight TYPE FLOAT USING weight::FLOAT,
	ALTER COLUMN "EAN" TYPE VARCHAR(17),
	ALTER COLUMN product_code TYPE VARCHAR(11),
	ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
	ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
	ALTER COLUMN weight_class TYPE VARCHAR(14),
	ALTER COLUMN still_available TYPE BOOLEAN
	USING CASE
	    WHEN still_available = 'Still_avaliable' THEN true
	    WHEN still_available = 'Removed' THEN false
END;


-- Task 6 - dim_date_times
SELECT 
    MAX(CHAR_LENGTH(CAST(month AS TEXT))) AS max_month_length,
    MAX(CHAR_LENGTH(CAST(year AS TEXT))) AS max_year_length,
    MAX(CHAR_LENGTH(CAST(day AS TEXT))) AS max_day_length,
    MAX(CHAR_LENGTH(CAST(time_period AS TEXT))) AS max_time_period_length
FROM dim_date_times;

ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(2),
    ALTER COLUMN year TYPE VARCHAR(4),
    ALTER COLUMN day TYPE VARCHAR(2),
    ALTER COLUMN time_period TYPE VARCHAR(10),
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;


-- Task 7 - dim_card_details
SELECT 
    MAX(CHAR_LENGTH(card_number)) AS max_card_number_length,
    MAX(CHAR_LENGTH(expiry_date)) AS max_expiry_date_length
FROM dim_card_details;

ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(22),
    ALTER COLUMN expiry_date TYPE VARCHAR(5),
    ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE;

-- TASK 8 - Primary key
ALTER TABLE dim_users
	ADD CONSTRAINT PK_dim_users PRIMARY KEY(user_uuid);
	
ALTER TABLE dim_store_details
	ADD CONSTRAINT PK_dim_store_details PRIMARY KEY(store_code);

ALTER TABLE dim_products
	ADD CONSTRAINT PK_dim_products PRIMARY KEY (product_code);

ALTER TABLE dim_date_times
	ADD CONSTRAINT PK_dim_date_times PRIMARY KEY(date_uuid);

ALTER TABLE dim_card_details
	ADD CONSTRAINT PK_dim_card_details PRIMARY KEY(card_number);

-- Task 9 - Foreign key
ALTER TABLE orders_table
	ADD CONSTRAINT FK_dim_users FOREIGN KEY(user_uuid) REFERENCES dim_users(user_uuid);
ALTER TABLE orders_table	
	ADD CONSTRAINT FK_store_details FOREIGN KEY(store_code) REFERENCES dim_store_details(store_code);
ALTER TABLE orders_table
	ADD CONSTRAINT FK_products FOREIGN KEY(product_code) REFERENCES dim_products(product_code);	
ALTER TABLE orders_table
	ADD CONSTRAINT FK_date_times FOREIGN KEY(date_uuid) REFERENCES dim_date_times(date_uuid);
ALTER TABLE orders_table
	ADD CONSTRAINT FK_card_details FOREIGN KEY(card_number) REFERENCES dim_card_details(card_number);
