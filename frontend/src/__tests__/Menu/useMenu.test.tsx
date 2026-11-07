// React
import type { ReactNode } from "react";

// Third Party
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

// AA Example
import * as ApiCalls from "@/Api/calls/general";
import { useMenu } from "@/Menu/Hooks";

const wrapper = ({ children }: { children: ReactNode }) => {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retryDelay: 0 } } });
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};

describe("useMenu", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should load the left and right menu links", async () => {
    // Test Data
    const menu = {
      left_links: [{ name: "Dashboard", link: "/" }],
      right_links: [{ name: "Settings", link: "/settings/" }],
    };
    const spy = vi.spyOn(ApiCalls, "loadMenu").mockResolvedValue(menu as never);

    // Test Action
    const { result } = renderHook(() => useMenu(), { wrapper });

    // Expected Result
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual(menu);
    expect(spy).toHaveBeenCalledTimes(1);
  });

  it("should retry once and then report an error when the request fails", async () => {
    // Test Data
    const spy = vi.spyOn(ApiCalls, "loadMenu").mockRejectedValue(new Error("Failed to load menu"));

    // Test Action
    const { result } = renderHook(() => useMenu(), { wrapper });

    // Expected Result
    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.data).toBeUndefined();
    expect(spy).toHaveBeenCalledTimes(2);
  });
});
