/** @odoo-module */

console.log("🔥 OWL Dashboard JS loaded!");
import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class ChartRender extends Component {
  setup() {
    this.chartRef = useRef("chart");
    this.chart = null;
    onWillStart(async () => {
      await loadJS(
        "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.0/chart.umd.min.js"
      );
    });

    useEffect(
      () => {
        if (this.chartRef.el) {
          this.renderChart();
        } else {
          console.warn("⚠️ Canvas belum siap, menunggu render ulang...");
        }
      },
      () => [this.chartRef.el] // watch ref element
    );
  }

  onWillDestroy() {
    // Bersihkan chart saat komponen dihancurkan
    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }
  }

  renderChart() {
    const ctx = this.chartRef.el;
    if (!ctx) {
      console.error("❌ Tidak bisa render chart: canvas tidak ditemukan.");
      return;
    }

    const data = [
      { year: 2010, count: 10, color: "blue" },
      { year: 2011, count: 20, color: "green" },
      { year: 2012, count: 15, color: "red" },
      { year: 2013, count: 25, color: "yellow" },
      { year: 2014, count: 22, color: "orange" },
      { year: 2015, count: 30, color: "purple" },
      { year: 2016, count: 28, color: "pink" },
    ];

    const dataDays = [
      { days: "Mon", count: 5, color: "blue" },
      { days: "Tues", count: 25, color: "green" },
      { days: "Wed", count: 55, color: "red" },
    ];

    // Jika chart sudah pernah dibuat sebelumnya, destroy dulu biar nggak double
    // if (this.chart) {
    //   this.chart.destroy();
    // }
    this.chart = new Chart(this.chartRef.el, {
      type: this.props.type,
      data: {
        labels: data.map((row) => row.year),
        datasets: [
          {
            label: "Acquisitions by year",
            data: data.map((row) => row.count),
            backgroundColor: data.map((color) => color.color),
          },
          {
            label: "Acquisitions by Days",
            data: dataDays.map((row) => row.count),
            backgroundColor: dataDays.map((color) => color.color),
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
          },
          title: {
            display: true,
            text: this.props.title,
            position: "bottom",
          },
        },
      },
    });
  }
}

ChartRender.template = "owl_dashboard.ChartRender";
