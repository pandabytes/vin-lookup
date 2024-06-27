// import React, { StrictMode } from "react";
// import { createRoot } from "react-dom/client";
// import "./styles.css";

// import App from "./App";
// // import Board from "./Board";
// // import Header from './Header';
// // import SubmitForm from './SubmitForm';
// // import VinsTable from './VinsTable';

// const root = createRoot(document.getElementById("root"));
// root.render(
//   <StrictMode>
//     <App />
//   </StrictMode>
// );

import { StrictMode } from "react";
import { Container, createRoot } from "react-dom/client";
import "./styles.css";
import App from "./App";

const root = createRoot(document.getElementById("root") as Container);

root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
