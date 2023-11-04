WITH temp1 AS (
  SELECT DATE(FechaObservacion) AS Fecha, EXTRACT(HOUR FROM FechaObservacion) AS Hora, *
  FROM {{ source('project', 'wind_direction') }}
  ORDER BY FechaObservacion
), temp2 AS (
  SELECT DISTINCT
    AVG(ValorObservado) OVER (PARTITION BY Fecha, Hora, CodigoEstacion) AS direction,
    Fecha AS date,
    Hora AS hour, 
    CodigoEstacion AS code,
    INITCAP(TRANSLATE(Departamento, 'ÁÉÍÓÚÜÑ', 'AEIOUUN')) AS department,
    INITCAP(TRANSLATE(Municipio, 'ÁÉÍÓÚÜÑ', 'AEIOUUN')) AS state,
    Latitud AS latitude, 
    Longitud AS longitude
  FROM temp1
  ORDER BY date, hour, code
), temp3 AS (
  SELECT
    direction, date, hour, code,
    CASE
      WHEN department = 'Archipielago De San Andres, Providencia Y Santa Catalina' THEN 'Archipielago De San Andres Providencia Y Santa Catalina'
      WHEN department = 'San Andres Providencia' THEN 'Archipielago De San Andres Providencia Y Santa Catalina'
      WHEN department = 'Bogota D.C.' THEN 'Bogota D.C'
      WHEN department = 'Bogota' THEN 'Bogota D.C'
      ELSE department
    END AS department,
    CASE
      WHEN state = 'Bogota, D.C' THEN 'Bogota D.C'
      ELSE state
    END AS state,
    * EXCEPT(direction, date, hour, code, department, state)
  FROM temp2
)

SELECT 
  direction, date, hour, code,
  CASE
    WHEN UPPER(department) IN ('AMAZONAS', 'CAQUETA', 'GUAINIA', 'GUAVIARE', 'PUTUMAYO', 'VAUPES') THEN 'Amazonica'
    WHEN UPPER(department) IN ('ANTIOQUIA', 'BOGOTA D.C', 'SANTAFE DE BOGOTA D.C', 'BOYACA', 'CALDAS', 'CUNDINAMARCA', 'HUILA', 'NORTE DE SANTANDER', 'QUINDIO', 'RISARALDA', 'SANTANDER', 'TOLIMA') THEN 'Andina'
    WHEN UPPER(department) IN ('ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA', 'ATLANTICO', 'BOLIVAR', 'CESAR', 'CORDOBA', 'LA GUAJIRA', 'MAGDALENA', 'SUCRE') THEN 'Caribe'
    WHEN UPPER(department) IN ('CAUCA', 'CHOCO', 'NARINO', 'VALLE DEL CAUCA') THEN 'Pacifico'
    WHEN UPPER(department) IN ('ARAUCA', 'CASANARE', 'META', 'VICHADA') THEN 'Orinoquia'
    ELSE NULL -- Casos no mapeados
  END AS region,
  * EXCEPT(direction, date, hour, code)
FROM temp3