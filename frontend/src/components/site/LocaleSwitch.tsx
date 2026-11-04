'use client';

import { Suspense } from 'react';
import { useLocale } from 'next-intl';
import { useSearchParams } from 'next/navigation';
import { Link, usePathname } from '@/i18n/routing';

function LocaleLink({ label, query }: { label: string; query: string }) {
  const locale = useLocale();
  const pathname = usePathname();
  return (
    <Link href={query ? `${pathname}?${query}` : pathname} locale={locale === 'zh' ? 'en' : 'zh'} className="nav-link">
      {label}
    </Link>
  );
}

function LocaleLinkWithQuery({ label }: { label: string }) {
  return <LocaleLink label={label} query={useSearchParams().toString()} />;
}

// Switches language on the current page, keeping filters and compare ids in the query string.
// The query is only known in the browser, so static pages render the plain link until it loads.
export default function LocaleSwitch({ label }: { label: string }) {
  return (
    <Suspense fallback={<LocaleLink label={label} query="" />}>
      <LocaleLinkWithQuery label={label} />
    </Suspense>
  );
}
