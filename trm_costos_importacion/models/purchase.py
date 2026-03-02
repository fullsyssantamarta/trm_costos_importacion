from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    trm_rate = fields.Float(
        string="TAMPA TRM",
        digits=(12, 6),
        default=1.0,
        help="Tasa TRM usada para convertir la moneda de la compra a la moneda de la compañía."
    )

    @api.onchange("currency_id", "company_id")
    def _onchange_currency_trm_default(self):
        for order in self:
            if not order.currency_id or not order.company_id:
                continue
            if order.currency_id == order.company_id.currency_id:
                order.trm_rate = 1.0

    def write(self, vals):
        res = super().write(vals)
        if "trm_rate" in vals:
            for order in self:
                pickings = order.picking_ids.filtered(lambda p: p.state not in ("done", "cancel"))
                if pickings:
                    pickings.write({"trm_rate": order.trm_rate})
        return res
