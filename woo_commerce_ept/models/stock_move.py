# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import models


class StockMove(models.Model):
    """
    Inherited model for adding custom fields in picking while creating it.
    @author: Maulik Barad on Date 14-Nov-2019.
    """
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        """
        This method sets Woocommerce instance in picking.
        @author: Maulik Barad on Date 14-Nov-2019.
        """
        res = super(StockMove, self)._get_new_picking_values()
        order_id = self.sale_line_id.order_id
        if order_id.woo_order_id:
            res.update({'woo_instance_id': order_id.woo_instance_id.id, 'is_woo_delivery_order': True})
        return res

    def _action_assign(self):
        # We inherited the base method here to set the instance values in picking while the picking type is dropship.
        res = super(StockMove, self)._action_assign()
        picking_ids = self.mapped('picking_id')
        for picking in picking_ids:
            if not picking.woo_instance_id and picking.sale_id and picking.sale_id.woo_instance_id:
                picking.write({'woo_instance_id':picking.sale_id.woo_instance_id.id, 'is_woo_delivery_order': True})
        return res