// Third Party
import { beforeEach, describe, expect, it, vi } from "vitest";

// AA Example
import { apiClient } from "@/Api/Api";
import { characterQueryKeys, loadCharacter, loadCharacters, updateCharacter } from "@/Api/calls/character";
import { ProjectName } from "@/constants";

const character = {
  id: 1,
  character_id: 1001,
  character_name: "Test Pilot",
  corporation_id: 2001,
  corporation_name: "Test Corp",
  portrait_url: "https://images.evetech.net/characters/1001/portrait?size=64",
  active: true,
  wallet_balance: 1234.56,
  update_status: "ok",
  update_status_label: "OK",
  last_update: null,
};

describe("Character API calls", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("should build query keys per character", () => {
    // Test Action & Expected Result
    expect(characterQueryKeys.all).toEqual(["Characters"]);
    expect(characterQueryKeys.detail(1001)).toEqual(["Characters", 1001]);
  });

  describe("loadCharacters", () => {
    it("should return the characters from the list endpoint", async () => {
      // Test Data
      vi.spyOn(apiClient, "GET").mockResolvedValueOnce({
        data: [character],
        error: undefined,
        response: new Response(),
      } as never);

      // Test Action
      const result = await loadCharacters();

      // Expected Result
      expect(result).toEqual([character]);
      expect(apiClient.GET).toHaveBeenCalledWith(`/${ProjectName}/api/characters/`);
    });

    it("should throw when the request fails", async () => {
      // Test Data
      vi.spyOn(apiClient, "GET").mockResolvedValueOnce({
        data: undefined,
        error: { error: "Permission Denied" },
        response: new Response(),
      } as never);

      // Test Action & Expected Result
      await expect(loadCharacters()).rejects.toThrow("Failed to load characters");
    });
  });

  describe("loadCharacter", () => {
    it("should pass the character id as path parameter", async () => {
      // Test Data
      const detail = { ...character, sections: [] };
      vi.spyOn(apiClient, "GET").mockResolvedValueOnce({
        data: detail,
        error: undefined,
        response: new Response(),
      } as never);

      // Test Action
      const result = await loadCharacter(1001);

      // Expected Result
      expect(result).toEqual(detail);
      expect(apiClient.GET).toHaveBeenCalledWith(`/${ProjectName}/api/characters/{character_id}/`, {
        params: { path: { character_id: 1001 } },
      });
    });
  });

  describe("updateCharacter", () => {
    it("should post the force refresh flag", async () => {
      // Test Data
      const response = { success: true, message: "Update task queued for Test Pilot" };
      vi.spyOn(apiClient, "POST").mockResolvedValueOnce({
        data: response,
        error: undefined,
        response: new Response(),
      } as never);

      // Test Action
      const result = await updateCharacter(1001, true);

      // Expected Result
      expect(result).toEqual(response);
      expect(apiClient.POST).toHaveBeenCalledWith(`/${ProjectName}/api/characters/{character_id}/update/`, {
        params: { path: { character_id: 1001 } },
        body: { force_refresh: true },
      });
    });

    it("should throw when the update cannot be queued", async () => {
      // Test Data
      vi.spyOn(apiClient, "POST").mockResolvedValueOnce({
        data: undefined,
        error: { error: "Character not found" },
        response: new Response(),
      } as never);

      // Test Action & Expected Result
      await expect(updateCharacter(1001)).rejects.toThrow("Failed to queue the character update");
    });
  });
});
