import { getTranslations } from 'next-intl/server';

// Ft4 dense colophon: one block of small mono text that says where the data comes from.
export default async function SiteFooter() {
  const ts = await getTranslations('Site');
  return (
    <footer className="mt-[var(--space-3xl)] px-[var(--page-gutter)] pb-[var(--space-xl)]">
      <div className="mx-auto max-w-[var(--page-max)] border-t border-rule-2 pt-[var(--space-md)]">
        <p className="max-w-[72ch] font-mono text-xs leading-relaxed text-muted">{ts('colophon')}</p>
      </div>
    </footer>
  );
}
