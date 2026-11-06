// React
import { MemoryRouter } from "react-router-dom";

// Third Party
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

// AA Example
import type { CharacterSchema } from "@/Api/schema";
import { CharacterTable } from "@/Components/Character/CharacterTable";

const characters: CharacterSchema[] = [
  {
    id: 1,
    character_id: 1001,
    character_name: "Alice",
    corporation_id: 2001,
    corporation_name: "Alpha Corp",
    portrait_url: "https://images.evetech.net/characters/1001/portrait?size=64",
    active: true,
    wallet_balance: 1500000,
    update_status: "ok",
    update_status_label: "OK",
    last_update: null,
  },
  {
    id: 2,
    character_id: 1002,
    character_name: "Bob",
    corporation_id: 2002,
    corporation_name: "Beta Corp",
    portrait_url: "https://images.evetech.net/characters/1002/portrait?size=64",
    active: true,
    wallet_balance: null,
    update_status: "token_error",
    update_status_label: "Token Error",
    last_update: null,
  },
];

const renderTable = (props?: Partial<React.ComponentProps<typeof CharacterTable>>) =>
  render(
    <MemoryRouter>
      <CharacterTable characters={characters} onUpdate={vi.fn()} {...props} />
    </MemoryRouter>,
  );

describe("CharacterTable", () => {
  it("should render the characters with wallet and status", () => {
    // Test Action
    renderTable();

    // Expected Result
    expect(screen.getByText("Alice")).toBeInTheDocument();
    expect(screen.getByText("Alpha Corp")).toBeInTheDocument();
    expect(screen.getByText("1,500,000 ISK")).toBeInTheDocument();
    const badges = screen.getAllByTestId("character-status-badge");
    expect(badges[0]).toHaveClass("bg-success");
    expect(badges[1]).toHaveClass("bg-warning");
    expect(badges[1]).toHaveTextContent("Token Error");
  });

  it("should call onUpdate with the character id", async () => {
    // Test Data
    const user = userEvent.setup();
    const onUpdate = vi.fn();
    renderTable({ onUpdate });

    // Test Action
    await user.click(screen.getByRole("button", { name: "Update Bob" }));

    // Expected Result
    expect(onUpdate).toHaveBeenCalledWith(1002);
  });

  it("should disable the button of the character being updated", () => {
    // Test Action
    renderTable({ updatingCharacterId: 1001 });

    // Expected Result
    expect(screen.getByRole("button", { name: "Update Alice" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Update Bob" })).toBeEnabled();
  });

  it("should show the empty text without characters", () => {
    // Test Action
    renderTable({ characters: [] });

    // Expected Result
    expect(screen.getByText("No characters registered yet.")).toBeInTheDocument();
  });
});
