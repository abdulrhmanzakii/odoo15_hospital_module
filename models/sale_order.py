from odoo import api, fields, models
from odoo.addons.sale.models.sale_order import SaleOrder as OdooSaleOrder


class SaleOrder(models.Model):
    _inherit = "sale.order"


    # @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        print("........................................")
        for order in self:

            return super(OdooSaleOrder,self)._unlink_except_draft_or_cancel()
