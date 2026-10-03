// Third Party
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { apiClient } from '@/Api/Api';
import {
    loadMenu,
    loadUserData,
    loadUserSettings,
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
            expect(apiClient.GET).toHaveBeenCalledWith('/example/api/user/');
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
        it('calls /example/api/menu/ and returns data', async () => {
            const mockMenu = { left_links: [], right_links: [] };
            vi.spyOn(apiClient, 'GET').mockResolvedValueOnce({
                data: mockMenu,
                error: undefined,
                response: new Response(),
            } as never);

            const result = await loadMenu();
            expect(result).toEqual(mockMenu);
            expect(apiClient.GET).toHaveBeenCalledWith('/example/api/menu/');
        });
    });

    describe('loadUserSettings', () => {
        it('returns settings from the typed GET endpoint', async () => {
            const settings = { disable_notifications: true };
            vi.spyOn(apiClient, 'GET').mockResolvedValueOnce({
                data: settings,
                error: undefined,
                response: new Response(),
            } as never);

            const result = await loadUserSettings();
            expect(result).toEqual(settings);
            expect(apiClient.GET).toHaveBeenCalledWith('/example/api/settings/');
        });
    });

    describe('updateUserSettings', () => {
        it('submits JSON to the typed PUT endpoint', async () => {
            const settings = { disable_notifications: true };
            vi.spyOn(apiClient, 'PUT').mockResolvedValueOnce({
                data: settings,
                error: undefined,
                response: new Response(),
            } as never);

            const result = await updateUserSettings(settings);
            expect(result).toEqual(settings);
            expect(apiClient.PUT).toHaveBeenCalledWith('/example/api/settings/', {
                body: settings,
            });
        });

        it('throws error when update fails', async () => {
            vi.spyOn(apiClient, 'PUT').mockResolvedValueOnce({
                data: undefined,
                error: { status: 403 },
                response: new Response(),
            } as never);

            await expect(updateUserSettings({ disable_notifications: false })).rejects.toThrow('Failed to update user settings');
        });
    });
});
