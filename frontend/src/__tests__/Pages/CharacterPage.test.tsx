// React
import { MemoryRouter } from "react-router-dom";

// Third Party
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

// AA Example
import * as characterApi from "@/Api/calls/character";
import { ProjectName } from "@/constants";
import { CharacterPage } from "@/Pages/CharacterPage";

vi.mock("@/Api/calls/character", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/Api/calls/character")>();
  return {
    ...actual,
    loadCharacters: vi.fn(),
    updateCharacter: vi.fn(),
  };
});

const character = {
  id: 1,
  character_id: 1001,
  character_name: "Alice",
  corporation_id: 2001,
  corporation_name: "Alpha Corp",
  portrait_url: "https://images.evetech.net/characters/1001/portrait?size=64",
  active: true,
  wallet_balance: 100,
  update_status: "ok",
  update_status_label: "OK",
  last_update: null,
};

const renderPage = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[`/${ProjectName}/characters/`]}>
        <CharacterPage />
      </MemoryRouter>
    </QueryClientProvider>,
  );
};

describe("CharacterPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should list the characters", async () => {
    // Test Data
    vi.mocked(characterApi.loadCharacters).mockResolvedValue([character]);

    // Test Action
    renderPage();

    // Expected Result
    expect(await screen.findByText("Alice")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Characters" })).toBeInTheDocument();
  });

  it("should queue an update and show the message", async () => {
    // Test Data
    const user = userEvent.setup();
    vi.mocked(characterApi.loadCharacters).mockResolvedValue([character]);
    vi.mocked(characterApi.updateCharacter).mockResolvedValue({
      success: true,
      message: "Update task queued for Alice",
    });

    // Test Action
    renderPage();
    await user.click(await screen.findByRole("button", { name: "Update Alice" }));

    // Expected Result
    expect(characterApi.updateCharacter).toHaveBeenCalledWith(1001);
    expect(await screen.findByRole("status")).toHaveTextContent("Update task queued for Alice");
  });

  it("should show an error when the update fails", async () => {
    // Test Data
    const user = userEvent.setup();
    vi.mocked(characterApi.loadCharacters).mockResolvedValue([character]);
    vi.mocked(characterApi.updateCharacter).mockRejectedValue(new Error("boom"));

    // Test Action
    renderPage();
    await user.click(await screen.findByRole("button", { name: "Update Alice" }));

    // Expected Result
    expect(await screen.findByRole("alert")).toHaveTextContent("The update could not be queued.");
  });

  it("should show the error state when loading fails", async () => {
    // Test Data
    vi.mocked(characterApi.loadCharacters).mockRejectedValue(new Error("boom"));

    // Test Action
    renderPage();

    // Expected Result
    expect(await screen.findByText("Something went wrong.")).toBeInTheDocument();
  });
});
