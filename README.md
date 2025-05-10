# LATAM DevSecOps/SRE Challenge Rodrigo Valdés

[![Deploy Status](https://github.com/rodvaldes/latam-devops-challenge/actions/workflows/deploy.yaml/badge.svg)](https://github.com/rodvaldes/latam-devops-challenge/actions/workflows/deploy.yaml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Aplicación FastAPI desplegada en Google Cloud Run como parte del challenge técnico para LATAM Airlines.  
Demuestra despliegue automatizado, ingesta de datos con Pub/Sub, almacenamiento en BigQuery y exposición vía API HTTP.

**API en producción:**  
[https://fastapi-app-980942243451.us-central1.run.app/datos](https://fastapi-app-980942243451.us-central1.run.app/datos)

## Prueba

```bash
curl https://fastapi-app-980942243451.us-central1.run.app/datos |jq |less
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   832  100   832    0     0    885      0 --:--:-- --:--:-- --:--:--   886
[
  {
    "flight_id": "flight10",
    "status": "delayed",
    "timestamp": "2024-01-10T00:00:00+00:00"
  },
  ...........
  {
    "flight_id": "flight1",
    "status": "ontime",
    "timestamp": "2024-01-01T00:00:00+00:00"
  }
]
---
```
## Estructura del Proyecto

```bash
.
├── .github/ # Workflows de Github Actions pasa CI/CD
├── app/ # API HTTP con FastAPI (exposición de datos desde BigQuery)
├── iac/terraform/ # Infraestructura como código (opcional)
├── publisher/ # Scripts para simular la publicación de eventos a Pub/Sub
├── utils/ # Scripts utilitarios
├── .gitignore
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

> El directorio `iac/terraform/` contiene los archivos `main.tf`, `variables.tf`, y `outputs.tf` que definen esta infraestructura en conjunto con los modulos iac/terraform/modules.
---

## Parte 2: Aplicaciones y CI/CD

- La API HTTP fue desarrollada con **FastAPI** y desplegada exitosamente en **Cloud Run**.
- Se conecta a **BigQuery** para exponer los datos ingresados previamente vía Pub/Sub.
- Se incluye una **prueba de integración** (`tests/test_api.py`) que valida que el endpoint `/datos` responde correctamente.
- El despliegue fue realizado inicialmente de forma manual; se deja implementado un pipeline GitHub Actions que ejecuta CI/CD de manera automática.

---

## Parte 3: Pruebas y calidad

- Se implementó una prueba de integración básica que:
  - Verifica el código de estado 200.
  - Confirma que la respuesta es una lista JSON no vacía con los campos `flight_id`, `status`, `timestamp`.

### Otras pruebas sugeridas (no implementadas)

- Test de carga al endpoint `/datos`.
- Validación de datos almacenados en BigQuery después de recibir mensajes Pub/Sub.
- Simulación de errores en la base de datos para probar resiliencia de la API.

---

## Parte 4: Métricas y monitoreo

### Métricas críticas propuestas

1. **Tasa de mensajes recibidos por Pub/Sub** (ingesta)
2. **Tiempo de respuesta del endpoint `/datos`**
3. **Errores 5xx o latencias elevadas en Cloud Run**

### Herramienta sugerida

- **Google Cloud Monitoring + Grafana**
  - Dashboards con:
    - Número de mensajes procesados
    - Errores por minuto
    - Tiempo promedio de respuesta

### Escalamiento

- Al escalar a múltiples servicios similares, se recomienda agrupar métricas por etiqueta (`project`, `dataset`, `service`) y usar vistas agregadas.

---

## Parte 5: Alertas y confiabilidad (opcional)

### Umbrales sugeridos

- Tiempo de respuesta > 1.5s en promedio → alerta
- Error rate > 1% sostenido → alerta al canal SRE
- Sin mensajes en Pub/Sub por más de 10 minutos → alerta

### SLIs/SLOs propuestos

| Servicio      | SLI                        | SLO                             |
|---------------|----------------------------|----------------------------------|
| API HTTP      | 99% de respuestas < 800ms  | 99.9% disponibilidad mensual     |
| Ingesta Pub/Sub | 99.5% de mensajes insertados correctamente | <0.5% fallos procesados al día |

## Arquitectura de Sistema

Este sistema sigue un patrón event-driven. Un publicador simula eventos de vuelos y los envía a un tópico Pub/Sub. Un suscriptor (Python) escucha y guarda los datos en BigQuery. Luego, una API FastAPI (en Cloud Run) expone los datos en formato JSON.

```bash
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
```

---

## ¿Cómo correr el proyecto?

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
```

##  Supuestos y mejoras posibles

- Se asume un formato de datos simple (flight_id, status, timestamp).

- Se deja como mejora implementar procesamiento batch con Apache Beam.

- Se puede integrar más monitoreo con Prometheus + Grafana.

- Pipeline CI/CD completo con más validaciones.

- Integración validación FinOps de costo de infra a partir del terraform plan. (Mover Finops al comienzo).

- Integración con IDP Portal o Backstage.

- Integración con Jira Cloud para obtención de métricas, gestión de proyecto, automatizaciones de flujo de "trabajo", habilitación ITSM con Jira Service Management.

Este commit se hizo desde el vuelo LA3 Airbus 321 SCL CCP.

Contacto
Rodrigo Valdés
rodrigovaldes@gmail.com
<https://github.com/rodvaldes>
