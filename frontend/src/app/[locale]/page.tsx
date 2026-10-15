import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import ProductCard from '@/components/gear/ProductCard';
import { gears } from '@/lib/gear-data';
import { releaseKey } from '@/lib/gear';

export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Landing');
  const ts = await getTranslations('GearSpecs');

  const brands = Object.values(
    gears.reduce<Record<string, { brand: string; bodies: number; lenses: number }>>((acc, g) => {
      const row = (acc[g.brand] ??= { brand: g.brand, bodies: 0, lenses: 0 });
      if (g.gearType === 'LENS') row.lenses++;
      else row.bodies++;
      return acc;
    }, {})
  ).sort((a, b) => b.bodies + b.lenses - (a.bodies + a.lenses));

  const latest = [...gears]
    .filter(g => g.image_url)
    .sort((a, b) => releaseKey(b) - releaseKey(a) || a.modelName.localeCompare(b.modelName))
    .slice(0, 8);

  return (
    <main className="mx-auto max-w-[var(--page-max)] px-[var(--page-gutter)] pt-[var(--space-2xl)] pb-[var(--space-2xl)]">
      <section className="max-w-[46rem]">
        <h1 className="text-[length:var(--text-display)] font-bold leading-[1.05] tracking-[var(--tracking-display)]">{t('title')}</h1>
        <p className="mt-[var(--space-md)] max-w-[34em] text-md text-ink-2">{t('lede')}</p>
        <Link href="/database" className="link-type mt-[var(--space-lg)] inline-flex min-h-11 items-center text-md font-bold tnum">
          {t('browse', { count: gears.length })} →
        </Link>
      </section>

      <section className="mt-[var(--space-3xl)]" aria-labelledby="by-brand">
        <h2 id="by-brand" className="text-xl font-bold">{t('byBrand')}</h2>
        <ul className="mt-[var(--space-md)] grid border-t border-ink sm:grid-cols-[repeat(2,minmax(0,1fr))] lg:grid-cols-[repeat(3,minmax(0,1fr))] sm:gap-x-[var(--space-xl)]">
          {brands.map(b => (
            <li key={b.brand} className="border-b border-rule">
              <Link href={`/database?brands=${encodeURIComponent(b.brand)}`} className="group flex min-h-14 items-baseline justify-between gap-[var(--space-md)] py-[var(--space-sm)]">
                <span className="font-display text-lg font-bold text-ink group-hover:text-accent">{b.brand}</span>
                <span className="font-mono text-xs text-muted tnum">
                  {[b.bodies && `${b.bodies} ${t('bodies')}`, b.lenses && `${b.lenses} ${t('lenses')}`].filter(Boolean).join(' · ')}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-[var(--space-3xl)]" aria-labelledby="latest">
        <h2 id="latest" className="text-xl font-bold">{t('latest')}</h2>
        <div className="mt-[var(--space-md)] grid grid-cols-[repeat(2,minmax(0,1fr))] gap-x-[var(--space-lg)] gap-y-[var(--space-xl)] border-t border-ink pt-[var(--space-lg)] md:grid-cols-[repeat(4,minmax(0,1fr))]">
          {latest.map((g, i) => (
            <ProductCard key={g.id} gear={g} noImageLabel={ts('noImage')} streetLabel={ts('street')} priority={i < 4} />
          ))}
        </div>
      </section>
    </main>
  );
}
