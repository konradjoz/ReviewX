from fastapi import *
from starlette.responses import HTMLResponse

from models import Shop

router = APIRouter(prefix="/api/v1")


@router.get("/merchant/{merchant_url}")
async def get_merchants():
    l = Shop.objects().all().to_json()
    html = f"""
    <html>
    <head>
    <title>Merchants</title>
    </head>
    <body>
    <pre class="prettyprint">
    <code class="">
    {l}
    </code>
    </pre>
    </body>
    <script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js"></script>
    """

    return HTMLResponse(html)
    """
    merchants_list = []
    for merchant in Shop.objects().fields(name=1):
        merchants_list.append(merchant.name)
    if len(merchants_list) != 0:
        return JSONResponse(merchants_list)
    else:
        return JSONResponse({
            "message": "No merchants found"
        })
"""
