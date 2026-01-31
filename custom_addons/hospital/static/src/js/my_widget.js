/** @odoo-module */
import { registry } from "@web/core/registry";

function myWidgetAction(env, action) {
  console.log(env);
  console.log(action);
  alert("Hello from my custom client action!");
}

registry.category("actions").add("my_widget_action", myWidgetAction);
