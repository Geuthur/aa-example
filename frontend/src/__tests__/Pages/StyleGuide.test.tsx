// React
import { MemoryRouter } from "react-router";

// Third Party
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import StyleGuide from "@/Pages/StyleGuide";

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}));

describe("StyleGuide", () => {
  it("renders utility previews and all table variants including light modal variant", () => {
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
    expect(tables).toHaveLength(3);
    expect(screen.getAllByText("Aster Voss")).toHaveLength(3);
  });

  it("opens modal with light table preview when modal button is clicked", async () => {
    // Test Data
    const user = userEvent.setup();
    render(
      <MemoryRouter>
        <StyleGuide />
      </MemoryRouter>,
    );

    // Test Action
    const modalBtn = screen.getByRole("button", { name: /Preview in Modal/i });
    await user.click(modalBtn);

    // Expected Result
    expect(screen.getByText("Modal Table Showcase")).toBeTruthy();
    expect(screen.getByText("Roster in Modal (aa-panel + aa-table-light)")).toBeTruthy();
  });
});