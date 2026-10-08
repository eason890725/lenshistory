import { getTranslations } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import { catalogueStats } from '@/lib/gear-data';
import CompareNavLink from './CompareNavLink';
import LocaleSwitch from './LocaleSwitch';

// N6 masthead: centred wordmark, issue line beneath, link row, single rule.
export default async function SiteHeader() {
  const t = await getTranslations('Navigation');
  const ts = await getTranslations('Site');
  const stats = catalogueStats();

  return (
    <header className="px-[var(--page-gutter)] pt-[var(--space-lg)] text-center">
      <Link href="/" className="inline-block font-display text-[clamp(1.75rem,4vw,2.75rem)] font-bold leading-none tracking-[var(--tracking-display)] text-ink">
        LensHistory
      </Link>
      <p className="label mt-[var(--space-xs)] tnum">
        {ts('issue', stats)}
      </p>
      <nav aria-label="Primary" className="mt-[var(--space-md)]">
        <ul className="flex items-center justify-center gap-x-[var(--space-lg)] text-sm">
          <li><Link href="/" className="nav-link">{t('home')}</Link></li>
          <li><Link href="/database" className="nav-link">{t('database')}</Link></li>
          <li><CompareNavLink label={t('compare')} /></li>
          <li aria-hidden="true" className="text-rule-2">/</li>
          <li><LocaleSwitch label={ts('switchLocale')} /></li>
        </ul>
      </nav>
      <hr className="mx-auto mt-[var(--space-md)] max-w-[var(--page-max)] border-0 border-t border-rule-2" />
    </header>
  );
}
