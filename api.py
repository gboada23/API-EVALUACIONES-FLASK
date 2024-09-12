import os
from flask import Flask, request, jsonify
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Usar el archivo de secretos en Render
credentials_path = "/etc/secrets/credentials.json"

# Configuración para la autenticación de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(creds)


# Definición de la función de procesamiento de datos
def personalgrupo(mes):
    # Abrimos la hoja de Google y cargamos los datos
    grupo = gc.open('GRUPO DE EMPRESAS NUEVA').worksheet('EVALUACIONES')
    datos = grupo.get_all_records()
    datos = pd.DataFrame(datos)

    # Formateamos la fecha y extraemos el mes
    datos['FECHA'] = pd.to_datetime(datos['FECHA'], format='%d/%m/%Y')
    datos['MES'] = datos['FECHA'].dt.month

    # Filtramos los datos para el mes solicitado
    mes = datos[datos['MES'] == mes].copy()

    # Calculamos los porcentajes de cada columna de evaluación
    mes['cumplimiento_horario_pct'] = mes["CUMPLIENTO DE HORARIO"] / 4
    mes['discrecion_politicas_pct'] = mes["DISCRECION POLITICAS INTERNAS"] / 4
    mes['clima_organizacional_pct'] = mes["CLIMA ORGANIZACIONAL"] / 4
    mes['cumplimiento_actividades_pct'] = mes["CUMPLIMIENTO DE ACTIVIDADES "] / 4

    # Calculamos el resultado promedio global usando los valores normalizados
    mes['Resultado final'] = (mes['cumplimiento_horario_pct'] +
                         mes['discrecion_politicas_pct'] +
                         mes['clima_organizacional_pct'] +
                         mes['cumplimiento_actividades_pct']) / 4

    # Agrupamos los resultados por el personal y calculamos el promedio
    mes = mes.groupby('PERSONAL')[["PERSONAL",
                                 "cumplimiento_horario_pct",
                                 "discrecion_politicas_pct",
                                 "clima_organizacional_pct",
                                 "cumplimiento_actividades_pct",
                                 "Resultado final"]].mean(numeric_only=True).reset_index()

    # Cargamos la lista del personal
    personal = gc.open('GRUPO DE EMPRESAS NUEVA').worksheet('LISTADO DEL PERSONAL')
    personal = personal.get_all_records()
    personal = pd.DataFrame(personal)
    personal = personal[['NOMBRES Y APELLIDOS','CEDULA','CARGO','CORREO']]
    personal = personal.rename(columns={'NOMBRES Y APELLIDOS':'PERSONAL'})

    # Realizamos el merge con los resultados del personal
    merge = pd.merge(personal, mes, on="PERSONAL", how="inner")
    merge = merge.sort_values(by='PERSONAL', ascending=True)
    merge = merge.round(2)
    columnas = ['cumplimiento_horario_pct', 'discrecion_politicas_pct', 'clima_organizacional_pct', 'cumplimiento_actividades_pct', 'Resultado final']
    for columna in columnas:
        merge[columna] = merge[columna].apply(lambda x: f'{x * 100}'.replace('.', ',') + '%')
    return merge

@app.route('/')
def home():
    return "API de Evaluaciones: usa la ruta /evaluacion?mes=<numero_mes> para obtener los datos."

# Crear un endpoint para la API
@app.route('/evaluacion', methods=['GET'])
def get_evaluacion():
    # Obtener el parámetro de mes de la URL
    mes = request.args.get('mes')
    
    # Validar el parámetro de mes
    if not mes:
        return jsonify({"error": "El parámetro 'mes' es requerido."}), 400
    try:
        mes = int(mes)
        if mes < 1 or mes > 12:
            return jsonify({"error": "El mes debe estar entre 1 y 12."}), 400
    except ValueError:
        return jsonify({"error": "El parámetro 'mes' debe ser un número entero."}), 400

    # Obtener los datos filtrados
    try:
        resultado = personalgrupo(mes)
        return jsonify(resultado.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
