// React
import React from 'react'
import ReactDOM from "react-dom/client";

// Configuration
import { AppName } from "@/configuration.js"

// Styles
import '@/index.css';

// App
import App from '@/App.tsx';

const container = document.getElementById(`${AppName}-root`)

if (!container) {
  throw new Error(`${AppName} React mount point was not found.`)
}

ReactDOM.createRoot(container).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
