import functions_framework
import json

# Mock database / cache for inventory level
INVENTORY_CACHE = {
    "SKU-2001": {"item": "Smart POS Terminal", "stock": 25},
    "SKU-2002": {"item": "Inventory Barcode Reader", "stock": 60}
}

@functions_framework.http
def inventory_sync(request):
    """
    Serverless function for Meridian Pivot sync service.
    Handles inventory level requests via HTTP.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    sku = None
    if request_json and 'sku' in request_json:
        sku = request_json['sku']
    elif request_args and 'sku' in request_args:
        sku = request_args['sku']

    if not sku:
        return json.dumps({"error": "Missing 'sku' parameter."}), 400, {'Content-Type': 'application/json'}

    item_data = INVENTORY_CACHE.get(sku)
    if not item_data:
        return json.dumps({"sku": sku, "status": "Not Found", "stock": 0}), 404, {'Content-Type': 'application/json'}

    return json.dumps({
        "sku": sku,
        "item": item_data["item"],
        "stock": item_data["stock"],
        "source": "serverless-sync-cache"
    }), 200, {'Content-Type': 'application/json'}