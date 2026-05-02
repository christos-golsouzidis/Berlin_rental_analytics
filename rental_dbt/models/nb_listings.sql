SELECT 
    neighborhood,
    COUNT(*) as total_properties,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage_of_all,
    MIN(warm_rent) as min_warm_rent,
    MAX(warm_rent) as max_warm_rent,
    AVG(area_m2) as avg_area_m2
FROM {{ source('rental_data', 'properties') }}
WHERE neighborhood IS NOT NULL
    AND neighborhood != ''
GROUP BY neighborhood
ORDER BY total_properties DESC