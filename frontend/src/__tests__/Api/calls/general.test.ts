// Third Party
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { apiClient } from '@/Api/Api';
import {
    loadUserSettings,
    updateUserSettings,
} from '@/Api/calls/general';
import { ProjectName } from '@/constants';

describe('General API client functions', () => {
    beforeEach(() => {
        vi.restoreAllMocks();
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
            expect(apiClient.GET).toHaveBeenCalledWith(`/${ProjectName}/api/settings/`);
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
            expect(apiClient.PUT).toHaveBeenCalledWith(`/${ProjectName}/api/settings/`, {
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
