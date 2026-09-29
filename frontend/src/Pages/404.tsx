// Third Party
import { useTranslation } from 'react-i18next';

// Voices of War
import { ErrorLoader } from '@/Components/Loader';
export function ErrorPage() {
    const { t } = useTranslation();
    return (
        <main className="m-4 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 p-3 border-zinc-800 bg-[#202433] rounded-md shadow-sm backdrop-blur-md">
            <ErrorLoader title={t("Error 404")} message={t("The page you are looking for does not exist.")} />
        </main>
    );
}