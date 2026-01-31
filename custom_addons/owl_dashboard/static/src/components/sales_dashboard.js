/** @odoo-module */

console.log("🔥 OWL Dashboard JS loaded!");
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Component, onWillStart, useRef, onMounted, useState } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
const { DateTime } = luxon;

import { KPICard } from "./kpi_card/kpi_card";
import { ChartRender } from "./chart_render/chart_render";
import { useService } from "@web/core/utils/hooks";

export class OwlSalesDashboard extends Component {
  setup() {
    this.state = useState({
      quotation: {
        value: 0,
        percentage: 0,
      },

      period: 7,
    });

    // Add some buttons for quick navigation
    this.action = useService("action");

    // ORM service to interact with Odoo models
    this.orm = useService("orm");

    // Notification service
    // this.myServiceNotif = useService("myServiceNotif");

    onWillStart(async () => {
      this.getDate();
      await this.getQuotation();
    });
  }

  async onChangePeriod() {
    // using luxom
    this.getDate();
    await this.getQuotation();
  }

  // open action from view, or navigate to form view
  async openActivity(activity) {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: _t("Hospital Patients"),
      target: "popup",
      res_id: activity.res_id,
      res_model: "hospital.patients",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  getDate() {
    this.state.date = DateTime.now()
      .minus({ days: this.state.period })
      .toLocaleString(DateTime.DATE_SHORT);
  }

  async getQuotation() {
    // let domain = [["state", "in", ["draft", "sent"]]];
    let domain = [];
    if (this.state.period > 0) {
      domain.push(["date_order", ">=", this.state.date]);
    }
    console.log("masukkkk");
    const data = await this.orm.searchCount("sale.order", domain);
    console.log(data);
    this.state.quotation.value = data;
  }
}

OwlSalesDashboard.template = "owl_dashboard.OwlSalesDashboard";
OwlSalesDashboard.components = { KPICard, ChartRender };

registry
  .category("actions")
  .add("owl_dashboard.sales_dashboard", OwlSalesDashboard);
