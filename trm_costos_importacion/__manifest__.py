{
    "name": "TRM Costos de Importación",
    "version": "18.0.1.0.1",
    "category": "Purchase/Inventory",
    "summary": "TRM por compra y recepción con costo promedio ponderado",
    "author": "Tampa Soluciones",
    "license": "LGPL-3",
    "depends": ["purchase", "stock", "account"],
    "data": [
        "views/purchase_order_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_valuation_layer_view.xml"
    ],
    "installable": True,
    "application": False
}
