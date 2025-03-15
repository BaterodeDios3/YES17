/** @odoo-module */

import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.order_custom_analytic_id = this.order_custom_analytic_id || "";
    },
    set_order_custom_analytic(order_custom_analytic_id){
        this.order_custom_analytic_id = order_custom_analytic_id;
    },
    get_order_custom_analytic(){
        return this.order_custom_analytic_id;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.order_custom_analytic_id = this.order_custom_analytic_id;
        return json;
    },
    init_from_JSON(json){
        super.init_from_JSON(...arguments);
        this.order_custom_analytic_id = json.order_custom_analytic_id;
    }

});
patch(Payment.prototype, {
   setup(_defaultObj, options) {
        super.setup(...arguments);
        this.pay_custom_analytic_id = this.pay_custom_analytic_id || "";
   },
   set_pay_custom_analytic_id(pay_custom_analytic_id){
        this.pay_custom_analytic_id = pay_custom_analytic_id;
   },
   get_pay_custom_analytic_id(){
        return this.pay_custom_analytic_id;
   },
   export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.pay_custom_analytic_id = this.pay_custom_analytic_id;
        return json;
   },
   init_from_JSON(json){
        super.init_from_JSON(...arguments);
        this.pay_custom_analytic_id = json.pay_custom_analytic_id;
   }
});

