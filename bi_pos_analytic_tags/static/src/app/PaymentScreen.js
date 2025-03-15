/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
    async validateOrder(){
        var self = this;
        var session = this.env.services.pos.pos_session
        var list = [];
        self.env.services.pos.get_order().set_order_custom_analytic(session.custom_analytic_id[0])
        self.env.services.pos.get_order().selected_paymentline.set_pay_custom_analytic_id(session.custom_analytic_id[0])
        await super.validateOrder(...arguments);
    }

});
