WITH date_filtered AS (
    SELECT 
        warm_rent,
        CAST(created_at AS DATE) as listing_date
    FROM {{ source('rental_data', 'properties') }}
    WHERE CAST(created_at AS DATE) BETWEEN '2022-01-01' AND '2026-01-01'
        AND warm_rent IS NOT NULL
        AND warm_rent > 0
)
SELECT 
    DATE_TRUNC('quarter', listing_date) as quarter,
    COUNT(*) as num_properties,
    AVG(warm_rent) as avg_warm_rent,
    MEDIAN(warm_rent) as median_warm_rent,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY warm_rent) as p75_warm_rent,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY warm_rent) as p25_warm_rent
FROM date_filtered
GROUP BY DATE_TRUNC('quarter', listing_date)
ORDER BY quarter