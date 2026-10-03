import { apiClient } from "@/Api/Api";
import type { components } from "@/Api/OpenApi";
import { ProjectName } from '@/App';

export async function loadUserData(): Promise<{ user: components["schemas"]["UserData"] }> {
  const { data, error } = await apiClient.GET(`/${ProjectName}/api/user/`);
  if (error || !data) {
    throw new Error("Failed to load user data");
  }
  return { user: data };
}

export async function loadUserSettings(): Promise<components["schemas"]["UserSettingsSchema"]> {
  const { data, error } = await apiClient.GET(`/${ProjectName}/api/settings/`);
  if (error || !data) {
    throw new Error("Failed to load user settings");
  }
  return data;
}

export async function loadMenu(): Promise<components["schemas"]["MenuSchema"]> {
  const { data, error } = await apiClient.GET(`/${ProjectName}/api/menu/`);
  if (error || !data) {
    throw new Error("Failed to load menu");
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
