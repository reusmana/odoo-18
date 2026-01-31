import { registry } from "@web/core/registry";

const shareStateService = {
  start(env) {
    this.state = {};

    return {
      getState: () => this.state,
      setState: (newState) => {
        this.state = { ...this.state, ...newState };
      },
    };
  },
};
// registry.category("services").add("myService", shareStateService);
