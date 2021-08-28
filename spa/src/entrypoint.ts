import React from "react";
import ReactDOM from "react-dom";
import { App } from "./App";

function renderApp(selector: string): void {
  ReactDOM.render(React.createElement(App), document.querySelector(selector));
}

renderApp("#app");
