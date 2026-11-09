-- Q1 / P1 Fase 1: bases con más expediciones
SELECT b.codigo_base,b.nombre,COUNT(e.codigo_expedicion) AS total_expediciones FROM base_cientifica b INNER JOIN expedicion e ON e.codigo_base=b.codigo_base GROUP BY b.codigo_base,b.nombre ORDER BY total_expediciones DESC,b.nombre;
-- Q2 / P2 Fase 1: distribución de muestras clasificadas por tipo y base
SELECT b.nombre AS base, m.tipo_especializacion AS tipo,COUNT(*) AS cantidad FROM muestra m INNER JOIN recoleccion r ON r.codigo_muestra=m.codigo_muestra INNER JOIN expedicion e ON e.codigo_expedicion=r.codigo_expedicion INNER JOIN base_cientifica b ON b.codigo_base=e.codigo_base WHERE m.tipo_especializacion IS NOT NULL GROUP BY b.nombre,m.tipo_especializacion ORDER BY b.nombre,cantidad DESC;
-- Q3 / P3 Fase 1: relación entre duración y promedio de evaluación
SELECT e.codigo_expedicion,e.duracion_dias,COUNT(v.nro_correlativo) AS evaluaciones,ROUND(AVG(v.calificacion),2) AS promedio_calificacion FROM expedicion e INNER JOIN evaluacion v ON v.codigo_expedicion=e.codigo_expedicion GROUP BY e.codigo_expedicion,e.duracion_dias ORDER BY e.duracion_dias DESC;
-- Q4: personal con mayor número de expediciones
SELECT p.id_personal,p.nombre||' '||p.apellido AS participante, COUNT(pa.codigo_expedicion) AS expediciones FROM personal p INNER JOIN participacion pa ON p.id_personal=pa.id_personal GROUP BY p.id_personal,p.nombre,p.apellido ORDER BY expediciones DESC,participante;
-- Q5: carga de recolecciones por expedición y base
SELECT b.nombre AS base,e.codigo_expedicion,COUNT(r.codigo_muestra) AS muestras_recolectadas FROM expedicion e INNER JOIN base_cientifica b ON e.codigo_base=b.codigo_base INNER JOIN recoleccion r ON e.codigo_expedicion=r.codigo_expedicion GROUP BY b.nombre,e.codigo_expedicion ORDER BY muestras_recolectadas DESC,e.codigo_expedicion;
