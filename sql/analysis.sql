
-- 1. Total water consumption by building
SELECT
    building_name,
    ROUND(SUM(total_consumption_litres), 2) AS total_litres
FROM daily_consumption
GROUP BY building_name
ORDER BY total_litres DESC;


-- 2. Daily water consumption across all buildings
SELECT
    reading_date,
    ROUND(SUM(total_consumption_litres), 2) AS daily_total
FROM daily_consumption
GROUP BY reading_date
ORDER BY reading_date;


-- 3. Buildings with the highest average daily consumption
SELECT
    building_name,
    ROUND(AVG(total_consumption_litres), 2) AS average_daily_litres
FROM daily_consumption
GROUP BY building_name
ORDER BY average_daily_litres DESC;


-- 4. Potential unusual consumption records
SELECT
    reading_date,
    building_name,
    total_consumption_litres
FROM daily_consumption
WHERE potential_anomaly = 1
ORDER BY total_consumption_litres DESC;


-- 5. Number of readings per building
SELECT
    b.building_name,
    COUNT(r.reading_id) AS reading_count
FROM buildings b
JOIN meters m ON b.building_id = m.building_id
JOIN readings r ON m.meter_id = r.meter_id
GROUP BY b.building_name
ORDER BY reading_count DESC;
