// React
import React from "react"
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"

// Third Party
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AaReactProvider, AuthBase, ErrorPage } from "aa-geuthur-react";
import { NuqsAdapter } from "nuqs/adapters/react-router/v8";

import { AppName, ProjectName } from "@/constants";
import CharacterPage from "@/Pages/CharacterPage";
import MainPage from "@/Pages/MainPage";
import SettingsPage from "@/Pages/SettingsPage";
import StyleGuide from "@/Pages/StyleGuide";

const queryClient = new QueryClient();

function Routing() {
  return (
    <React.StrictMode>
      <AaReactProvider projectName={ProjectName} appName={AppName}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <NuqsAdapter>
            <Routes>
              <Route path={`/${ProjectName}/`} element={<AuthBase />}>
                <Route index element={<MainPage />} />
                <Route path="characters/" element={<CharacterPage />} />
                <Route path="styleguide/" element={<StyleGuide />} />
                <Route path="settings/" element={<SettingsPage />} />
                <Route path="*" element={<ErrorPage />} />
              </Route>
              <Route path="*" element={<Navigate to={`/${ProjectName}/`} replace />} />
            </Routes>
          </NuqsAdapter>
        </BrowserRouter>
      </QueryClientProvider>
      </AaReactProvider>
    </React.StrictMode>
  )
}

export default Routing
