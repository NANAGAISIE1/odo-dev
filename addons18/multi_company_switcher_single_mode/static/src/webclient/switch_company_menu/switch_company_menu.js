/** @odoo-module **/

import { browser } from '@web/core/browser/browser';
import { patch } from '@web/core/utils/patch';
import { SwitchCompanyMenu } from '@web/webclient/switch_company_menu/switch_company_menu';
import { SET_COMPANY_SINGLE_MODE } from '../company_service';

patch(SwitchCompanyMenu.prototype, {
    /**
     * @override
     */
    toggleCompany(companyId) {},

    /**
     * @override
     */
    logIntoCompany(companyId) {
        browser.clearTimeout(this.toggleTimer);
        this.companyService.setCompanies(SET_COMPANY_SINGLE_MODE, companyId);
    },
});
