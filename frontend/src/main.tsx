// React
import React from 'react'
import ReactDOM from "react-dom/client";

import App from '@/App.tsx';
import '@/index.css';

const container = document.getElementById('aa-example-root')

if (!container) {
  throw new Error('Example React mount point was not found.')
}

ReactDOM.createRoot(container).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
