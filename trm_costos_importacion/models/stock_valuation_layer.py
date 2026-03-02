from odoo import fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    picking_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Recepción",
        related="stock_move_id.picking_id",
        store=False
    )
    purchase_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Compra",
        related="stock_move_id.purchase_line_id.order_id",
        store=False
    )
    trm_rate = fields.Float(
        string="TAMPA TRM",
        digits=(12, 6),
        related="stock_move_id.picking_id.trm_rate",
        store=False
    )
