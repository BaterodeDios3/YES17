odoo.define('pw_pos_pre_receipt.models', function(require){
    'use strict';
    const { PosGlobalState, Order} = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    var core = require('web.core');
    var _t = core._t;

    const PwPresalePosGlobalState = (PosGlobalState) => class PwPresalePosGlobalState extends PosGlobalState {
        add_new_order(){
            var orders = _.filter(this.get_order_list(), function(o){
                return o.orderlines.length == 0;
            });
            if (orders.length > 0) {
                this.set_order(orders[orders.length-1])
            } else {
                const order = this.createReactiveOrder();
                this.orders.add(order);
                this.selectedOrder = order;
                return order;
            }
        }
    }
    Registries.Model.extend(PosGlobalState, PwPresalePosGlobalState);
});
