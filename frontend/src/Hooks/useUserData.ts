// Third Party
import { useQuery } from "@tanstack/react-query";

// AA Example
import { loadUserData } from "@/Api/calls/general";
import { queryKeys } from "@/Api/query";

/** Loads the current user (main character, corporation, superuser flag). */
export function useUserData() {
  return useQuery({
    queryKey: queryKeys.User,
    queryFn: loadUserData,
    staleTime: 5 * 60 * 1000,
  });
}
