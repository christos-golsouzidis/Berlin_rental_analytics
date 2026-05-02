
SELECT 
    CASE 
        WHEN LOWER(furnishing) LIKE '%furnished%' AND LOWER(furnishing) NOT LIKE '%unfurnished%' THEN 'Furnished'
        WHEN LOWER(furnishing) LIKE '%unfurnished%' THEN 'Unfurnished'
        ELSE 'Partially Furnished'
    END as furnishing_status,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
FROM {{ source('rental_data', 'properties') }}
WHERE furnishing IS NOT NULL
GROUP BY furnishing_status
ORDER BY percentage DESC
