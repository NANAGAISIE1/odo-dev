/** @odoo-module **/

import { companyService } from '@web/webclient/company_service';
import { browser } from '@web/core/browser/browser';

export const SET_COMPANY_SINGLE_MODE = 'single';
const originalStart = companyService.start;

companyService.start = (env, { user, router, cookie }) => {
    const result = originalStart(env, { user, router, cookie });
    const originalSetCompanies = result.setCompanies;
    result.setCompanies = (mode, ...companyIds) => {
        if (mode === SET_COMPANY_SINGLE_MODE) {
            router.pushState({ cids: companyIds }, { lock: true });
            cookie.setCookie("cids", companyIds);
            browser.setTimeout(() => browser.location.reload());
        } else {
            originalSetCompanies(mode, ...companyIds);
        }
    }
    return result;
}
