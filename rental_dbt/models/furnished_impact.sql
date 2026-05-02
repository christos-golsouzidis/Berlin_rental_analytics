WITH furnished_comparison AS (
    SELECT 
        CASE 
            WHEN LOWER(furnishing) IN ('furnished', 'fully furnished') THEN 'Furnished'
            WHEN LOWER(furnishing) IN ('unfurnished', 'not furnished') THEN 'Unfurnished'
            ELSE 'Other'
        END as furnishing_category,
        warm_rent,
        area_m2,
        rooms
    FROM {{ source('rental_data', 'properties') }}
    WHERE warm_rent IS NOT NULL 
        AND warm_rent > 0
        AND furnishing IS NOT NULL
)
SELECT 
    furnishing_category,
    COUNT(*) as num_properties,
    ROUND(AVG(warm_rent), 2) as avg_warm_rent,
    ROUND(MEDIAN(warm_rent), 2) as median_warm_rent,
    ROUND(STDDEV(warm_rent), 2) as std_warm_rent,
    -- Price per square meter for better comparison
    ROUND(AVG(warm_rent / NULLIF(area_m2, 0)), 2) as avg_price_per_m2
FROM furnished_comparison
WHERE furnishing_category IN ('Furnished', 'Unfurnished')
GROUP BY furnishing_category