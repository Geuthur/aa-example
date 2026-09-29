// React
import React from 'react'
import ReactDOM from "react-dom/client";

// Styles
import '@/index.css';

import App from '@/App.tsx';

const container = document.getElementById('aa-example-root')

if (!container) {
  throw new Error('Example React mount point was not found.')
}

ReactDOM.createRoot(container).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
