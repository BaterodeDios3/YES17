/** @odoo-module **/

import { ProductInfoPopup } from "@point_of_sale/app/screens/product_screen/product_info_popup/product_info_popup";
import { patch } from "@web/core/utils/patch";

patch(ProductInfoPopup.prototype, {
    async setup() {
        super.setup();

        try {
            // Asegurarnos de que el objeto de usuario esté disponible antes de proceder
            const usera = this.env.services.user.name;

            // Verificar que el usuario está correctamente cargado
            if (!usera) {
                throw new Error('No se pudo obtener el ID del usuario.');
            }
            console.log("Usuario:", usera);
            // Llamar al método del backend para verificar si el usuario pertenece al grupo
            const showCoste = await fetch('/stock_uppin_17/get_user_groups', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            // Esta el permiso en showCoste
            var showCost = false;
            if ('Gerencia Ventas' in showCoste) {
               showCost = true;
               console.log("Gerencia Ventas Si");
            }else{
                showCost = false;
                console.log("Gerencia Ventas No");
            }


            // Mostrar u ocultar las filas en función de la respuesta
            this.showCost = showCost;

            if (!this.showCost) {
                // Ocultar las filas de 'Total Cost' y 'Total Margin' si el usuario no tiene acceso
                $("tr:has(td:contains('Total Cost'))").closest("tr").hide();
                $("tr:has(td:contains('Total Margin'))").closest("tr").hide();
                $("tr:has(td:contains('Cost'))").closest("tr").hide();
                $("tr:has(td:contains('Margin'))").closest("tr").hide();
            } else {
                // Mostrar las filas si el usuario tiene acceso
                $("tr:has(td:contains('Total Cost'))").closest("tr").show();
                $("tr:has(td:contains('Total Margin'))").closest("tr").show();
                $("tr:has(td:contains('Cost'))").closest("tr").show();
                $("tr:has(td:contains('Margin'))").closest("tr").show();
            }

        } catch (error) {
            console.error("Error al verificar los permisos del usuario:", error);
        }
    },
});
