// AA Example
import { apiClient } from "@/Api/Api";
import type { components } from "@/Api/OpenApi";
import { ProjectName } from "@/constants";

export async function loadUserSettings(): Promise<components["schemas"]["UserSettingsSchema"]> {
  const { data, error } = await apiClient.GET(`/${ProjectName}/api/settings/`);
  if (error || !data) {
    throw new Error("Failed to load user settings");
  }
  return data;
}

export async function updateUserSettings(
  settings: components["schemas"]["UserSettingsUpdateRequest"],
): Promise<components["schemas"]["UserSettingsSchema"]> {
  const { data, error } = await apiClient.PUT(`/${ProjectName}/api/settings/`, {
    body: settings,
  });

  if (error || !data) {
    throw new Error("Failed to update user settings");
  }
  return data;
}
