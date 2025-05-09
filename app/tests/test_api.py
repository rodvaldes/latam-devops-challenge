import requests

def test_datos_endpoint():
    url = "https://fastapi-app-980942243451.us-central1.run.app/datos"
    response = requests.get(url)

    # Verifica que responda 200 OK
    assert response.status_code == 200

    # Verifica que la respuesta sea una lista JSON no vacía
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Verifica que cada item tenga las claves esperadas
    for item in data:
        assert "flight_id" in item
        assert "status" in item
        assert "timestamp" in item
