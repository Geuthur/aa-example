// React
import { MemoryRouter } from 'react-router';

// Third Party
import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { ProjectName } from '@/constants';
import AuthLeftMenu from '@/Menu/AuthLeftMenu';

vi.mock('react-i18next', async (importOriginal) => {
    const actual = await importOriginal<typeof import('react-i18next')>();
    return {
        ...actual,
        useTranslation: () => ({
            t: (key: string) => key,
        }),
    };
});

describe('AuthLeftMenu', () => {
    it('should render internal navigation links', () => {
        // Test Data
        const testData = [
            { name: 'Dashboard', link: 'dashboard' },
            { name: 'Settings', link: '/settings/' },
        ];

        // Test Action
        render(
            <MemoryRouter initialEntries={[`/${ProjectName}/`]}>
                <AuthLeftMenu data={testData} isLoading={false} error={false} />
            </MemoryRouter>
        );

        // Expected Result
        const dashboardLink = screen.getByText('Dashboard');
        expect(dashboardLink).toBeDefined();
        expect(dashboardLink.getAttribute('href')).toBe(`/${ProjectName}/dashboard/`);

        const settingsLink = screen.getByText('Settings');
        expect(settingsLink).toBeDefined();
        expect(settingsLink.getAttribute('href')).toBe(`/${ProjectName}/settings/`);
    });

    it('should render external links with standard href', () => {
        // Test Data
        const testData = [
            { name: 'External Docs', link: 'https://docs.example.com', is_external: true },
        ];

        // Test Action
        render(
            <MemoryRouter>
                <AuthLeftMenu data={testData} isLoading={false} error={false} />
            </MemoryRouter>
        );

        // Expected Result
        const externalLink = screen.getByText('External Docs');
        expect(externalLink).toBeDefined();
        expect(externalLink.getAttribute('href')).toBe('https://docs.example.com');
    });

    it('should filter out items without links or handle empty list', () => {
        // Test Data
        const testData = [
            { name: 'No Link Category' },
        ];

        // Test Action
        const { container } = render(
            <MemoryRouter>
                <AuthLeftMenu data={testData} isLoading={false} error={false} />
            </MemoryRouter>
        );

        // Expected Result
        expect(container.querySelectorAll('li')).toHaveLength(0);
    });

    it('should render pulsating danger badge when has_errors is true', () => {
        // Test Data
        const testData = [
            { name: 'Settings', link: '/settings/', badge: 2, has_errors: true },
        ];

        // Test Action
        render(
            <MemoryRouter initialEntries={[`/${ProjectName}/`]}>
                <AuthLeftMenu data={testData} isLoading={false} error={false} />
            </MemoryRouter>
        );

        // Expected Result
        const badge = screen.getByText('2');
        expect(badge).toHaveClass('badge', 'bg-danger', 'aa-menu-badge-pulse');
    });

    it('should render static danger badge when has_errors is false', () => {
        // Test Data
        const testData = [
            { name: 'Settings', link: '/settings/', badge: 3, has_errors: false },
        ];

        // Test Action
        render(
            <MemoryRouter initialEntries={[`/${ProjectName}/`]}>
                <AuthLeftMenu data={testData} isLoading={false} error={false} />
            </MemoryRouter>
        );

        // Expected Result
        const badge = screen.getByText('3');
        expect(badge).toHaveClass('badge', 'bg-danger');
        expect(badge).not.toHaveClass('aa-menu-badge-pulse');
    });
});
