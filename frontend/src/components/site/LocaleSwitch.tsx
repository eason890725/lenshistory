'use client';

import { useLocale } from 'next-intl';
import { useSearchParams } from 'next/navigation';
import { Link, usePathname } from '@/i18n/routing';

// Switches language on the current page, keeping filters and compare ids in the query string.
export default function LocaleSwitch({ label }: { label: string }) {
  const locale = useLocale();
  const pathname = usePathname();
  const query = useSearchParams().toString();
  return (
    <Link href={query ? `${pathname}?${query}` : pathname} locale={locale === 'zh' ? 'en' : 'zh'} className="nav-link">
      {label}
    </Link>
  );
}
