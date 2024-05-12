-- SQL scrips that ranks country origin of bands, ordered by number of funs
SELECT origin, SUM(fans) as nb_fans FROM metal_bands GROUP BY origin ORDER BY nb_fans DESC;
