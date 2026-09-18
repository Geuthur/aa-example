import { apiClient } from "@/Api/Api";
import type { components } from "@/Api/OpenApi";

export async function loadUserData(): Promise<{ user: components["schemas"]["UserData"] }> {
  const { data, error } = await apiClient.GET("/example/api/view/user/");
  if (error || !data) {
    throw new Error("Failed to load user data");
  }
  return { user: data };
}

export async function loadMenu(): Promise<components["schemas"]["MenuSchema"]> {
  const { data, error } = await apiClient.GET("/example/api/view/menu/");
  if (error || !data) {
    throw new Error("Failed to load menu");
  }
  return data;
}

export async function updateUserSettings(settings: { disable_notifications: boolean }): Promise<{ success: boolean; message?: string }> {
  const body = new FormData();
  if (settings.disable_notifications) {
    body.append("disable_notifications", "on");
  }

  const { data, error } = await apiClient.POST("/example/api/modify/user/settings/", {
    body: body as never,
  });

  if (error || !data || (data as { success?: boolean }).success !== true) {
    throw new Error((data as { message?: string } | undefined)?.message ?? "Failed to update user settings");
  }
  return data as { success: boolean; message?: string };
}
