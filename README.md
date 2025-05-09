# LATAM DevSecOps/SRE Challenge Rodrigo Valdés

[![Deploy Status](https://github.com/rodvaldes/latam-devops-challenge/actions/workflows/deploy.yml/badge.svg)](https://github.com/rodvaldes/latam-devops-challenge/actions/workflows/deploy.yml)


Este repositorio contiene la solución al desafío técnico de LATAM Airlines. El objetivo es construir un sistema en la nube que permita ingestar, almacenar y exponer datos mediante IaC, CI/CD y una arquitectura resiliente.

---

## 📦 Estructura del Proyecto

```bash
.
├── app/ # API HTTP con FastAPI (exposición de datos desde BigQuery)
├── publisher/ # Scripts para simular la publicación de eventos a Pub/Sub
├── tests/ # Prueba de integración de la API
├── iac/terraform/ # Infraestructura como código (opcional)
├── requirements.txt # Dependencias del proyecto
└── README.md
```
## Parte 1: Infraestructura e IaC

La infraestructura fue definida completamente con **Terraform**, permitiendo reproducibilidad y control de cambios. Se desplegaron los siguientes componentes en Google Cloud Platform:

- **Pub/Sub**: se creó un tópico para simular eventos en tiempo real.
- **BigQuery**: se configuró un dataset y una tabla para almacenar los eventos.
- **Service Accounts**: con permisos mínimos para ejecutar los componentes.
- **Cloud Run**: se dejó provisionado el entorno para alojar la API HTTP.
- **Remote Backend**: el estado de Terraform se almacenó en un bucket de GCS dedicado.

La estructura modular del código permite separar ambientes y reutilizar componentes.

> El directorio `iac/terraform/` contiene los archivos `main.tf`, `variables.tf`, y `outputs.tf` que definen esta infraestructura.
---

## Parte 2: Aplicaciones y CI/CD

- La API HTTP fue desarrollada con **FastAPI** y desplegada exitosamente en **Cloud Run**.
- Se conecta a **BigQuery** para exponer los datos ingresados previamente vía Pub/Sub.
- Se incluye una **prueba de integración** (`tests/test_api.py`) que valida que el endpoint `/datos` responde correctamente.
- El despliegue fue realizado inicialmente de forma manual; se deja planteado un pipeline GitHub Actions para futuras automatizaciones.

---

## 🧠 Parte 3: Pruebas y calidad

- Se implementó una prueba de integración básica que:
  - Verifica el código de estado 200.
  - Confirma que la respuesta es una lista JSON no vacía con los campos `flight_id`, `status`, `timestamp`.

### Otras pruebas sugeridas (no implementadas):

- Test de carga al endpoint `/datos`.
- Validación de datos almacenados en BigQuery después de recibir mensajes Pub/Sub.
- Simulación de errores en la base de datos para probar resiliencia de la API.

---

## Parte 4: Métricas y monitoreo

### Métricas críticas propuestas:

1. **Tasa de mensajes recibidos por Pub/Sub** (ingesta)
2. **Tiempo de respuesta del endpoint `/datos`**
3. **Errores 5xx o latencias elevadas en Cloud Run**

### Herramienta sugerida:

- **Google Cloud Monitoring + Grafana**
  - Dashboards con:
    - Número de mensajes procesados
    - Errores por minuto
    - Tiempo promedio de respuesta

### Escalamiento:

- Al escalar a múltiples servicios similares, se recomienda agrupar métricas por etiqueta (`project`, `dataset`, `service`) y usar vistas agregadas.

---

## Parte 5: Alertas y confiabilidad (opcional)

### Umbrales sugeridos:

- Tiempo de respuesta > 1.5s en promedio → alerta
- Error rate > 1% sostenido → alerta al canal SRE
- Sin mensajes en Pub/Sub por más de 10 minutos → alerta

### SLIs/SLOs propuestos:

| Servicio      | SLI                        | SLO                             |
|---------------|----------------------------|----------------------------------|
| API HTTP      | 99% de respuestas < 800ms  | 99.9% disponibilidad mensual     |
| Ingesta Pub/Sub | 99.5% de mensajes insertados correctamente | <0.5% fallos procesados al día |



# Arquitectura de Sistema

Este sistema sigue un patrón event-driven. Un publicador simula eventos de vuelos y los envía a un tópico Pub/Sub. Un suscriptor (Python) escucha y guarda los datos en BigQuery. Luego, una API FastAPI (en Cloud Run) expone los datos en formato JSON.


+-------------------+
|  Simulador/       |
|  Publicador de    |
|  eventos (Python) |
+---------+---------+
          |
          | JSON
          v
+---------+---------+
|     Pub/Sub       |
| (Topic: flight-events) |
+---------+---------+
          |
          | Trigger
          v
+------------------------+
| Suscriptor Python      |
| (script local)         |
| - Recibe mensaje       |
| - Inserta en BigQuery  |
+----------+-------------+
           |
           | INSERT
           v
+------------------------+
| BigQuery               |
| - Dataset: flights     |
| - Tabla: flight_status |
+----------+-------------+
           |
           | SELECT
           v
+--------------------------+
| API HTTP en FastAPI      |
| (Desplegada en Cloud Run)|
+----------+---------------+
           |
           | JSON Response
           v
+-------------------+
|    Usuario final  |
|  (Browser / curl) |
+-------------------+


---

## 🚀 Cómo correr el proyecto

```bash
# Clonar el repositorio
git clone https://github.com/tu_usuario/latam-devops-challenge.git
cd latam-devops-challenge

# Crear y activar entorno virtual (Python 3.11 recomendado)
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Correr la API localmente
uvicorn app.main:app --reload

# Ejecutar pruebas
pytest tests/test_api.py

# Publicar mensaje a Pub/Sub (opcional, ver publisher/publisher.py)
python publisher/publisher.py

# Supuestos y mejoras posibles

* Se asume un formato de datos simple (flight_id, status, timestamp).

* Se deja como mejora implementar procesamiento batch con Apache Beam.

* Se puede integrar más monitoreo con Prometheus + Grafana.

* Pipeline CI/CD completo con validaciones y despliegue automatizado es parte del roadmap futuro.

Contacto
Rodrigo Valdés
[rodrigovaldes@gmail.com]
https://github.com/rodvaldes
