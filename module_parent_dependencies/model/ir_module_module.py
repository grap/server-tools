# -*- encoding: utf-8 -*-
##############################################################################
#
#    Module - Parent Dependencies module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, fields
from openerp.models import Model


class IrModuleModule(Model):
    _inherit = 'ir.module.module'

    # Field function Section
#    def _get_all_installed_parent_ids(
#            self, cr, uid, ids, field_name, arg, context=None):
#        res = self._get_direct_installed_parent_ids(
#            cr, uid, ids, field_name, arg, context=context)
#        for id in ids:
#            parent_ids = list(res[id])
#            undirect_parent_ids = self._get_all_installed_parent_ids(
#                cr, uid, res[id], field_name, arg, context=context)
#            for parent_id in parent_ids:
#                res[id] += undirect_parent_ids[parent_id]
#            res[id] = list(set(res[id]))
#        return res

    @api.multi
    def _get_all_installed_parent_ids(self):
        print self
        for rec in self:
            parent_ids = rec.direct_installed_parent_ids
            import pdb;pdb.set_trace()

    @api.multi
    def _get_direct_installed_parent_ids(self):
        immd_obj = self.env['ir.module.module.dependency']
        for rec in self:
            immd_ids = immd_obj.search([('name', '=', rec.name)])
            imm_ids = [x.module_id.id for x in immd_ids]
            imm_lst = self.search([
                    ('id', 'in', imm_ids),
                    ('state', 'not in', ['uninstalled', 'uninstallable'])])
            rec.all_installed_parent_ids = [x.id for x in imm_lst]

    # Column Section
    direct_installed_parent_ids = fields.Many2many(
        compute=_get_direct_installed_parent_ids,
        comodel_name='ir.module.module',
        string='Direct Parent Installed Modules')

    all_installed_parent_ids = fields.Many2many(
        compute=_get_all_installed_parent_ids,
        comodel_name='ir.module.module',
        string='Direct and Indirect Parent Installed Modules')
