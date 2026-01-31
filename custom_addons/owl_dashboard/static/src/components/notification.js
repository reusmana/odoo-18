import { registry } from "@web/core/registry";

const myServiceNotif = {
  dependencies: ["notification"],
  start(env, { notification }) {
    let counter = 1;
    setInterval(() => {
      notification.add(`Tick Tock ${counter++}`, { type: "success" });
    }, 5000);
  },
};

registry.category("services").add("myServiceNotif", myServiceNotif);
