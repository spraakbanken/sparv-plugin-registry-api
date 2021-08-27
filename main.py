from fastapi import FastAPI

import get_manifests

app = FastAPI()


@app.get("/")
def manifest_info():
    """Get all manifests."""
    manifests = get_manifests.main()
    return manifests
