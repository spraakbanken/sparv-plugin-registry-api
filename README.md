# sparv-plugin-registry-api

REST-API for listing Sparv plugins and validating plugin manifests.


## Running a test server

```
uvicorn main:app --reload
```

## Running a production server

```
gunicorn -k uvicorn.workers.UvicornWorker main:app
```
