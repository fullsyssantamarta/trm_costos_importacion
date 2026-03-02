from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    trm_rate = fields.Float(
        string="TRM",
        digits=(12, 6),
        related="picking_id.trm_rate",
        store=False
    )
    trm_price_unit = fields.Monetary(
        string="Precio TRM",
        currency_field="company_currency_id",
        compute="_compute_trm_values"
    )
    trm_value = fields.Monetary(
        string="Valor TRM",
        currency_field="company_currency_id",
        compute="_compute_trm_values"
    )

    @api.depends("product_uom_qty", "purchase_line_id.price_unit", "picking_id.trm_rate")
    def _compute_trm_values(self):
        for move in self:
            price_unit = move._get_trm_price_unit()
            move.trm_price_unit = price_unit
            move.trm_value = price_unit * move.product_uom_qty

    def _get_trm_price_unit(self):
        self.ensure_one()
        if not self.purchase_line_id:
            return 0.0
        purchase_line = self.purchase_line_id
        price_unit = purchase_line.price_unit
        if purchase_line.product_uom != self.product_uom:
            price_unit = purchase_line.product_uom._compute_price(price_unit, self.product_uom)
        return price_unit * (self.picking_id.trm_rate or 1.0)

    def _get_price_unit(self):
        price_unit = super()._get_price_unit()
        if self.purchase_line_id and self.picking_id and self.picking_id.trm_rate:
            purchase_line = self.purchase_line_id
            unit_price = purchase_line.price_unit
            if purchase_line.product_uom != self.product_uom:
                unit_price = purchase_line.product_uom._compute_price(unit_price, self.product_uom)
            price_unit = unit_price * self.picking_id.trm_rate
        return price_unit

    def _recompute_trm_price_unit(self):
        # Método auxiliar para refrescar valores TRM en la vista
        for move in self:
            move._compute_trm_values()
