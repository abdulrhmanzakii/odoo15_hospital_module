from datetime import date
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class OdooPlayGround(models.Model):
    _name = "odoo.playground"
    _description = "Odoo PlayGround"

    DEFAULT_ENV_VARIABLES = """""# Available variables:
    # - self : current object
    # - self.env : lol
    # - self.env :wacfasc
    # - self.env :adcac
    # - self.env :dvsav
    # - self.env :casc
    # - self.env :acav
    # - self.env :zvasv
    # - self.env :afwfw
    """""
    model_id = fields.Many2one('ir.model', String ="Model")
    code=fields.Text(string="Code")
    result = fields.Text(string="Result",readonly=True)
    help=fields.Text(string="Help",default=DEFAULT_ENV_VARIABLES,readonly=True)

    def action_execute(self):
        try:
            if self.model_id:
                model= self.env[self.model_id.model]
            else:
                model = self
            self.result = safe_eval(self.code.strip(), {'self': model})
        except Exception as e:
            self.result = str(e)






