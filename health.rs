def test_health_check_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}

def test_health_check_response_time():
    start_time = time.time()
    response = client.get('/health')
    end_time = time.time()
    assert response.status_code == 200
    assert (end_time - start_time) < 30  # response time should be less than 30 seconds