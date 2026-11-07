// React
import type { ReactNode } from "react";

// Third Party
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

// AA Example
import * as ApiCalls from "@/Api/ApiCalls";
import { useUserData } from "@/Hooks/useUserData";

const wrapper = ({ children }: { children: ReactNode }) => {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};

describe("useUserData", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should load the user data", async () => {
    // Test Data
    const userData = { user: { is_superuser: true } };
    const spy = vi.spyOn(ApiCalls, "loadUserData").mockResolvedValue(userData as never);

    // Test Action
    const { result } = renderHook(() => useUserData(), { wrapper });

    // Expected Result
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual(userData);
    expect(spy).toHaveBeenCalledTimes(1);
  });

  it("should report an error when the request fails", async () => {
    // Test Data
    vi.spyOn(ApiCalls, "loadUserData").mockRejectedValue(new Error("Failed to load user data"));

    // Test Action
    const { result } = renderHook(() => useUserData(), { wrapper });

    // Expected Result
    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.data).toBeUndefined();
  });
});
