# sm
Aplicación de pruebas de salud mental

## Acceso al API

**Get Authentication Token**
```
~$ curl -X POST -H 'Accept: application/json; indent=4' -d 'username=sotolito_admin&password=prueba123' http://127.0.0.1:8081/api/
```

**Use the Token**
```
curl -H "Authorization: e89e8f4a1563908620b0d0eb54c17eb06d42b341" http://127.0.0.1:8081/api/mental_test/
```


