# 📊 API de Evaluaciones de Personal

Esta API, desarrollada con Flask, permite realizar evaluaciones de personal en función de los datos almacenados en hojas de Google Sheets. Filtra los datos según el mes y año especificados, realiza cálculos sobre varios indicadores de desempeño, y devuelve un resumen detallado en formato JSON. La API está diseñada para integrarse en un CRM desarrollado en otro lenguaje, permitiendo el análisis y seguimiento del rendimiento del personal de manera centralizada.

## 🚀 Descripción

La API conecta con una hoja de Google para obtener datos de evaluación de personal y, a partir de esta información, calcula varios indicadores de rendimiento:
- Cumplimiento de horario
- Discreción en políticas internas
- Clima organizacional
- Cumplimiento de actividades

Luego, el promedio de estos indicadores se calcula para cada miembro del personal, proporcionando un puntaje general de evaluación. La API permite obtener datos específicos por mes y año, y devolverlos en un formato JSON fácil de consumir por otras aplicaciones, como un CRM.

---

## 📌 Funcionalidades Principales

- **Conexión a Google Sheets**: Utiliza Google Sheets para almacenar datos de evaluaciones y detalles del personal.
- **Filtros por Fecha**: Obtiene datos específicos de evaluaciones según el mes y año solicitados.
- **Cálculos Automáticos**: Calcula el promedio de varios indicadores para proporcionar un puntaje general de desempeño.
- **Formato de Respuesta JSON**: Retorna los datos en un formato JSON estructurado, fácil de integrar con otras aplicaciones.
- **Manejo de Errores**: Valida los parámetros de entrada y proporciona mensajes de error útiles en caso de datos incorrectos o faltantes.
- **Integración con CRM**: Diseñada para integrarse con un CRM desarrollado en otro lenguaje, ampliando la capacidad de análisis y seguimiento del personal.

## 🛠️ Tecnologías Utilizadas

- **Framework**:
  - **Flask**: Servidor web y manejador de rutas.
  
- **Bases de Datos**:
  - **Google Sheets**: Almacena datos de evaluaciones y personal.

- **Librerías**:
  - **pandas**: Para la manipulación y el análisis de datos.
  - **gspread**: Permite el acceso y manipulación de hojas de Google Sheets.
  - **oauth2client**: Maneja la autenticación de Google.
  
## 📥 Endpoints

## GET /evaluacion
1. **Descripción**: Obtiene los datos de evaluación filtrados por mes y año.
2. **Parámetros**:
  2.1 **mes**: Número del mes (1 a 12).
  2.2 **ano**: Año en formato de cuatro dígitos (por ejemplo, 2024).

## Ejemplo de Uso
http://localhost:5000/evaluacion?mes=5&ano=2024

## Respuesta de exito
```json
[
  {
    "PERSONAL": "Juan Pérez",
    "CEDULA": "12345678",
    "CARGO": "Gerente",
    "CORREO": "juan@example.com",
    "RESULTADO EVALUACION": 85.5
  },
  {
    "PERSONAL": "Ana García",
    "CEDULA": "87654321",
    "CARGO": "Analista",
    "CORREO": "ana@example.com",
    "RESULTADO EVALUACION": 92.0
  }
]



