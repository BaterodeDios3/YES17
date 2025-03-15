/** @odoo-module */

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { patch } from "@web/core/utils/patch";
import { onWillUnmount } from "@odoo/owl";

patch(ReceiptScreen.prototype, {
    orderDone() {
        if (this.props.presale) {
            const { name, props } = this.nextScreen;
            this.pos.showScreen(name, props);
            this.pos.add_new_order();
        } else {
            super.orderDone(...arguments);
        }
    }
});
