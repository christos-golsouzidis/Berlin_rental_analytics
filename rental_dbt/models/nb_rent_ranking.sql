WITH neighborhood_stats AS (
    SELECT 
        neighborhood,
        COUNT(*) as num_properties,
        AVG(warm_rent) as avg_warm_rent,
        MEDIAN(warm_rent) as median_warm_rent,
        MIN(warm_rent) as min_warm_rent,
        MAX(warm_rent) as max_warm_rent
    FROM {{ source('rental_data', 'properties') }}
    WHERE warm_rent IS NOT NULL 
        AND warm_rent > 0
        AND neighborhood IS NOT NULL
        AND neighborhood != ''
    GROUP BY neighborhood
    HAVING COUNT(*) >= 5  -- Only neighborhoods with at least 5 properties
)
SELECT 
    neighborhood,
    num_properties,
    ROUND(avg_warm_rent, 2) as avg_warm_rent,
    median_warm_rent,
    RANK() OVER (ORDER BY avg_warm_rent DESC) as rank_highest,
    RANK() OVER (ORDER BY avg_warm_rent ASC) as rank_lowest
FROM neighborhood_stats
ORDER BY avg_warm_rent DESC