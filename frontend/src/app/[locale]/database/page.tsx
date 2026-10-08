import { Suspense } from 'react';
import { setRequestLocale, getTranslations } from 'next-intl/server';
import GearGrid from './GearGrid';
import { gears } from '@/lib/gear-data';

export default async function DatabasePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const tn = await getTranslations('Navigation');

  return (
    <main className="mx-auto max-w-[var(--page-max)] px-[var(--page-gutter)] pt-[var(--space-xl)] pb-[var(--space-3xl)]">
      <h1 className="mb-[var(--space-xl)] text-[length:var(--text-display)] font-bold leading-[1.05] tracking-[var(--tracking-display)]">
        {tn('database')}
      </h1>
      <Suspense>
        <GearGrid gears={gears} />
      </Suspense>
    </main>
  );
}
