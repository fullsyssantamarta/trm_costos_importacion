from odoo import api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    trm_rate = fields.Float(
        string="TAMPA TRM",
        digits=(12, 6),
        default=1.0,
        help="Tasa TRM aplicada para la valoración de esta recepción."
    )

    @api.onchange("purchase_id")
    def _onchange_purchase_trm(self):
        for picking in self:
            if picking.purchase_id:
                picking.trm_rate = picking.purchase_id.trm_rate or 1.0

    @api.model
    def create(self, vals):
        if not vals.get("trm_rate") and vals.get("purchase_id"):
            purchase = self.env["purchase.order"].browse(vals["purchase_id"])
            vals["trm_rate"] = purchase.trm_rate or 1.0
        return super().create(vals)

    def write(self, vals):
        trm_changed = "trm_rate" in vals
        if trm_changed:
            for picking in self:
                if picking.state in ("done", "cancel"):
                    raise UserError(
                        "No se puede modificar la TRM cuando la recepción está en estado Hecho."
                    )
        res = super().write(vals)
        if trm_changed:
            for picking in self:
                moves = picking.move_ids.filtered(lambda m: m.state not in ("done", "cancel"))
                if moves:
                    moves._recompute_trm_price_unit()
        return res
