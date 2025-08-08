/* Copyright 2023 Tecnativa - Stefan Ungureanu
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

// Odoo 17 uses CalendarRenderer (v18 refactored to CalendarCommonRenderer)
import { CalendarRenderer } from "@web/views/calendar/calendar_renderer";
import { patch } from "@web/core/utils/patch";

patch(CalendarRenderer.prototype, {
    get options() {
        const options = super.options;
        if (this.env.searchModel.context.calendar_slot_duration) {
            options.slotDuration = this.env.searchModel.context.calendar_slot_duration;
        }
        return options;
    },
});
