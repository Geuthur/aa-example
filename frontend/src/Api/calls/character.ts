// AA Example
import { apiClient } from "@/Api/Api";
import type { ActionResponse, CharacterDetailSchema, CharacterSchema } from "@/Api/schema";
import { ProjectName } from "@/constants";

/** Query keys of the character module. */
export const characterQueryKeys = {
  all: ["Characters"] as const,
  detail: (characterId: number) => ["Characters", characterId] as const,
};

export async function loadCharacters(): Promise<CharacterSchema[]> {
  const { data, error } = await apiClient.GET(`/${ProjectName}/api/characters/`);
  if (error || !data) {
    throw new Error("Failed to load characters");
  }
  return data;
}

export async function loadCharacter(characterId: number): Promise<CharacterDetailSchema> {
  const { data, error } = await apiClient.GET(`/${ProjectName}/api/characters/{character_id}/`, {
    params: { path: { character_id: characterId } },
  });
  if (error || !data) {
    throw new Error("Failed to load character");
  }
  return data;
}

export async function updateCharacter(characterId: number, forceRefresh = false): Promise<ActionResponse> {
  const { data, error } = await apiClient.POST(`/${ProjectName}/api/characters/{character_id}/update/`, {
    params: { path: { character_id: characterId } },
    body: { force_refresh: forceRefresh },
  });
  if (error || !data) {
    throw new Error("Failed to queue the character update");
  }
  return data;
}
