// React
import { MemoryRouter } from "react-router";

// Third Party
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import StyleGuide from "@/Pages/StyleGuide";

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}));

describe("StyleGuide", () => {
  it("renders utility previews and both table variants", () => {
    // Test Data
    render(
      <MemoryRouter>
        <StyleGuide />
      </MemoryRouter>,
    );

    // Test Action
    const tables = screen.getAllByRole("table");

    // Expected Result
    expect(screen.getByRole("heading", { name: "AllianceAuth Style Test" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "EVE helper previews" })).toBeTruthy();
    expect(tables).toHaveLength(2);
    expect(screen.getAllByText("Aster Voss")).toHaveLength(2);
  });
});