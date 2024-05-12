-- List all bands with Glam rock as their main style, ranked by their longevity
SELECT 
	band_name,
	IF(split IS NULL, 2022 - formed, split - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style)
ORDER BY
	lifespan DESC
