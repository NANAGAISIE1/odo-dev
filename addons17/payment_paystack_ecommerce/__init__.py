# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


def uninstall_hook(cr, registry):
    from odoo.api import SUPERUSER_ID, Environment

    env = Environment(cr, SUPERUSER_ID, {})
    paystack_acquirer = env.ref(
        "payment_paystack.payment_acquirer_paystack", raise_if_not_found=False
    )

    if paystack_acquirer:
        paystack_acquirer.write(
            {
                "module_id": False,
                "state": "disabled",
            }
        )
