// React
import React from "react"
import {  BrowserRouter, Navigate, Route, Routes } from "react-router-dom"

// Third Party
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import i18n from "i18next";
import Backend from "i18next-http-backend";
import { NuqsAdapter } from "nuqs/adapters/react-router/v8";
import { initReactI18next } from "react-i18next";

import { ErrorPage } from "@/Pages/404";
import AuthBase from "@/Pages/Base";
import MainPage from "@/Pages/MainPage";
import Settings from "@/Pages/Settings";
import StyleGuide from "@/Pages/StyleGuide";

const queryClient = new QueryClient();
export const AppName = "aa-example";
export const ProjectName = "example";

// Read language directly from Django's LANGUAGE_CODE (set as lang="..." on root div)
const djangoLanguage = typeof document !== "undefined" ? document.getElementById(`${AppName}-root`)?.getAttribute("lang") ?? "en" : "en";

i18n
  .use(Backend)
  .use(initReactI18next)
  .init({
    lng: djangoLanguage,
    fallbackLng: "en",
    keySeparator: false,
    nsSeparator: false,
    interpolation: {
      escapeValue: false, // react already safes from xss => https://www.i18next.com/translation-function/interpolation#unescape
    },
    react: {
      useSuspense: false, //   <---- this will do the magic
    },
    backend: {
      loadPath: `/static/${ProjectName}/i18n/{{lng}}/{{ns}}.json`,
    },
  });

function App() {
  return (
    <React.StrictMode>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <NuqsAdapter>
            <Routes>
              <Route path={`/${ProjectName}/`} element={<AuthBase />}>
                <Route index element={<MainPage />} />
                <Route path="styleguide/" element={<StyleGuide />} />
                <Route path="settings/" element={<Settings />} />
                <Route path="*" element={<ErrorPage />} />
              </Route>
              <Route path="*" element={<Navigate to={`/${ProjectName}/`} replace />} />
            </Routes>
          </NuqsAdapter>
        </BrowserRouter>
      </QueryClientProvider>
    </React.StrictMode>
  )
}

export default App