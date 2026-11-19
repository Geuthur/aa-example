// Third Party
import { apiErrorMessage } from "aa-geuthur-react";

// AA Example
import { apiClient } from "@/Api/Api";
import type { ActionResponse, CharacterDetailSchema, CharacterSchema } from "@/Api/schema";
import { ProjectName } from "@/constants";

/*
 * A failed request throws the message of the API (`{"error": …}`) so the user reads the reason,
 * and the fixed text only when the API sent none.
 */

/** Query keys of the character module. */
export const characterQueryKeys = {
  all: ["Characters"] as const,
  detail: (characterId: number) => ["Characters", characterId] as const,
};

export async function loadCharacters(): Promise<CharacterSchema[]> {
  const { data, error } = await apiClient.GET(`/${ProjectName}/api/characters/`);
  if (error || !data) {
    throw new Error(apiErrorMessage(error, "Failed to load characters"));
  }
  return data;
}

export async function loadCharacter(characterId: number): Promise<CharacterDetailSchema> {
  const { data, error } = await apiClient.GET(`/${ProjectName}/api/characters/{character_id}/`, {
    params: { path: { character_id: characterId } },
  });
  if (error || !data) {
    throw new Error(apiErrorMessage(error, "Failed to load character"));
  }
  return data;
}

export async function updateCharacter(characterId: number, forceRefresh = false): Promise<ActionResponse> {
  const { data, error } = await apiClient.POST(`/${ProjectName}/api/characters/{character_id}/update/`, {
    params: { path: { character_id: characterId } },
    body: { force_refresh: forceRefresh },
  });
  if (error || !data) {
    throw new Error(apiErrorMessage(error, "Failed to queue the character update"));
  }
  return data;
}
