/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";


export class ReceiptReviewButton extends Component {
    static template = "pw_pos_pre_receipt.ReceiptReviewButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }
    async click() {
        const order = this.pos.get_order();
        const orderLines = order.get_orderlines();
        var order_lines = order.get_orderlines();
        if (order_lines.length === 0) {
            return;
        }
        this.pos.showScreen("ReceiptScreen", { order: order , 'presale': true});
    }
}

ProductScreen.addControlButton({
    component: ReceiptReviewButton,
    condition: function () {
        return this.pos.config.enable_presale;
    },
});
