// Third Party
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { apiClient } from '@/Api/Api';
import {
    loadMenu,
    loadUserData,
    updateUserSettings,
} from '@/Api/ApiCalls';

describe('General API client functions', () => {
    beforeEach(() => {
        vi.restoreAllMocks();
    });

    describe('loadUserData', () => {
        it('returns user data on successful GET', async () => {
            const mockUser = { user_id: 1, character_id: 42, character_name: 'Test Pilot' };
            vi.spyOn(apiClient, 'GET').mockResolvedValueOnce({
                data: mockUser,
                error: undefined,
                response: new Response(),
            } as never);

            const result = await loadUserData();
            expect(result).toEqual({ user: mockUser });
            expect(apiClient.GET).toHaveBeenCalledWith('/example/api/view/user/');
        });

        it('throws error when GET fails or returns no data', async () => {
            vi.spyOn(apiClient, 'GET').mockResolvedValueOnce({
                data: undefined,
                error: { status: 500 },
                response: new Response(),
            } as never);

            await expect(loadUserData()).rejects.toThrow('Failed to load user data');
        });
    });

    describe('loadMenu', () => {
        it('calls /view/menu/ and returns data', async () => {
            const mockMenu = { links: [] };
            vi.spyOn(apiClient, 'GET').mockResolvedValueOnce({
                data: mockMenu,
                error: undefined,
                response: new Response(),
            } as never);

            const result = await loadMenu();
            expect(result).toEqual(mockMenu);
            expect(apiClient.GET).toHaveBeenCalledWith('/example/api/view/menu/');
        });
    });

    describe('updateUserSettings', () => {
        it('submits FormData with disable_notifications and returns success', async () => {
            vi.spyOn(apiClient, 'POST').mockResolvedValueOnce({
                data: { success: true },
                error: undefined,
                response: new Response(),
            } as never);

            const result = await updateUserSettings({ disable_notifications: true });
            expect(result).toEqual({ success: true });
            expect(apiClient.POST).toHaveBeenCalledWith('/example/api/modify/user/settings/', expect.any(Object));
        });

        it('throws error when update fails', async () => {
            vi.spyOn(apiClient, 'POST').mockResolvedValueOnce({
                data: { success: false, message: 'Permission denied' },
                error: undefined,
                response: new Response(),
            } as never);

            await expect(updateUserSettings({ disable_notifications: false })).rejects.toThrow('Permission denied');
        });
    });
});
