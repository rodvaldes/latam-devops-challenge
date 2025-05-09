# Etapa base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requerimientos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer puerto (opcional para testing local)
EXPOSE 8080

# Comando por defecto para ejecutar la app localmente dentro de Docker
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
