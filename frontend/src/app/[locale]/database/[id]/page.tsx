import { getTranslations, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import BackButton from '../BackButton';
import CompareButton from '../CompareButton';
import { NONE, focalLength, releaseLabel, weightLabel, weightValue } from '@/lib/gear';
import { findGear } from '@/lib/gear-data';
import { shortName } from '@/components/gear/ProductCard';

type Row = [label: string, value: string | number | undefined];

function SpecGroup({ title, rows, none }: { title: string; rows: Row[]; none: string }) {
  const present = rows.filter(([, v]) => v !== undefined && v !== '').map(([l, v]): Row => [l, v === NONE ? none : v]);
  if (!present.length) return null;
  return (
    <section className="min-w-0">
      <h2 className="label mb-[var(--space-xs)]">{title}</h2>
      <dl className="border-t border-ink">
        {present.map(([label, value]) => (
          <div key={label} className="grid grid-cols-[minmax(0,2fr)_minmax(0,3fr)] gap-[var(--space-md)] border-b border-rule py-[var(--space-sm)]">
            <dt className="text-sm text-muted">{label}</dt>
            <dd className="text-sm text-ink tnum">{value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}

export default async function GearDetailPage({ params }: { params: Promise<{ id: string, locale: string }> }) {
  const { id, locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('GearSpecs');
  const tc = await getTranslations('Common');

  const gear = findGear(decodeURIComponent(id));
  if (!gear) notFound();

  const isLens = gear.gearType === 'LENS';
  const yesNo = (v?: boolean) => (v === undefined ? undefined : v ? tc('yes') : tc('no'));
  // Launch price, else the street price with the month it was checked
  const price = gear.launchPrice
    ? `NT$${gear.launchPrice.toLocaleString()}`
    : gear.retailPrice ? `NT$${gear.retailPrice.toLocaleString()} (${gear.retailPriceDate?.replace('-', '.')})` : undefined;
  const priceLabel = !gear.launchPrice && gear.retailPrice ? t('retailPrice') : t('launchPrice');
  const mounts = gear.mounts?.map(m => m.mount.name).join(', ');
  const kind = isLens
    ? gear.focalLengthMinMm === gear.focalLengthMaxMm ? t('prime') : t('zoom')
    : t('body');

  const groups: { title: string; rows: Row[] }[] = isLens
    ? [
        { title: t('optical'), rows: [
          [t('focalLength'), focalLength(gear)],
          [t('maxAperture'), gear.apertureMax ? `f/${gear.apertureMax}` : undefined],
          [t('minAperture'), gear.minAperture ? `f/${gear.minAperture}` : undefined],
          [t('closeFocus'), gear.closeFocus],
          [t('maxMagnification'), gear.maxMagnification],
          [t('opticalDesign'), gear.opticalDesign],
          [t('specialElements'), gear.specialElements],
          [t('coatings'), gear.coatings],
          [t('filterSize'), gear.filterSizeMm === 0 ? '—' : gear.filterSizeMm ? `${gear.filterSizeMm}mm` : undefined],
        ] },
        { title: t('features'), rows: [
          [t('motorType'), gear.motorType],
          [t('ois'), yesNo(gear.hasOIS)],
          [t('apertureRing'), yesNo(gear.hasApertureRing)],
          [t('customButton'), yesNo(gear.hasCustomButton)],
          [t('weatherSeal'), yesNo(gear.hasWeatherSeal)],
        ] },
        { title: t('physical'), rows: [
          [t('mount'), mounts],
          [t('sensorFormat'), gear.sensorFormat],
          [t('weight'), weightLabel(gear)],
          [t('dimensions'), gear.dimensions],
          [t('series'), gear.series],
          [t('releaseYear'), releaseLabel(gear)],
          [priceLabel, price],
        ] },
      ]
    : [
        { title: t('imaging'), rows: [
          [t('fixedLens'), gear.fixedLens],
          [t('megapixels'), gear.megapixels],
          [t('sensorType'), gear.sensorType],
          [t('sensorFormat'), gear.sensorFormat],
          [t('processor'), gear.processor],
          [t('isoRange'), gear.isoRange],
          [t('video'), gear.videoResolution],
          [t('videoColorDepth'), gear.videoColorDepth],
          [t('logSupport'), gear.logSupport],
        ] },
        { title: t('performance'), rows: [
          [t('afPoints'), gear.afPoints],
          [t('afTargets'), gear.afTargets],
          [t('afRange'), gear.afRange],
          [t('continuousShooting'), gear.burstSpeed],
          [t('ibis'), yesNo(gear.hasIBIS)],
          [t('ibisRating'), gear.ibisRating],
        ] },
        { title: t('hardware'), rows: [
          [t('evfResolution'), gear.evfResolution],
          [t('evfMagnification'), gear.evfMagnification],
          [t('lcdSpec'), gear.lcdSpec],
          [t('cardSlots'), gear.cardSlots],
          [t('batterySpec'), gear.batterySpec],
          [t('ports'), gear.ports],
          [t('weatherSeal'), yesNo(gear.hasWeatherSeal)],
          [t('mount'), mounts],
          [t('weight'), weightLabel(gear)],
          [t('dimensions'), gear.dimensions],
          [t('releaseYear'), releaseLabel(gear)],
          [priceLabel, price],
        ] },
      ];

  return (
    <main className="mx-auto max-w-[var(--page-max)] px-[var(--page-gutter)] pt-[var(--space-lg)] pb-[var(--space-3xl)]">
      <BackButton label={tc('backToDatabase')} />

      <div className="grid gap-[var(--space-xl)] lg:grid-cols-[minmax(0,7fr)_minmax(0,5fr)] lg:items-start">
        <div className="plate flex aspect-[4/3] items-center justify-center p-[var(--space-xl)]">
          {gear.image_url ? (
            <img
              src={gear.image_url}
              alt={gear.modelName}
              width={1200}
              height={900}
              fetchPriority="high"
              className="max-h-full max-w-full object-contain"
            />
          ) : (
            <span className="label">{t('noImage')}</span>
          )}
        </div>

        <div className="min-w-0">
          <p className="label">{[gear.brand, gear.series].filter(Boolean).join(' · ')}</p>
          <h1 className="mt-[var(--space-xs)] text-[length:var(--text-display)] font-bold leading-[1.05] tracking-[var(--tracking-display)]">
            {shortName(gear)}
          </h1>
          <p className="mt-[var(--space-sm)] text-md text-ink-2">
            {[kind, gear.sensorFormat, releaseLabel(gear)].filter(Boolean).join(' · ')}
          </p>

          <dl className="mt-[var(--space-lg)] grid grid-cols-[repeat(3,minmax(0,1fr))] border-y border-rule py-[var(--space-md)]">
            {([
              [priceLabel, price ?? '—'],
              [t('weight'), weightValue(gear) ? `${weightValue(gear)}g` : '—'],
              [isLens ? t('focalLength') : t('megapixels'), (isLens ? focalLength(gear) : gear.megapixels) ?? '—'],
            ] as const).map(([label, value]) => (
              <div key={label} className="min-w-0 pr-[var(--space-sm)]">
                <dt className="label">{label}</dt>
                <dd className="mt-[var(--space-2xs)] break-words font-mono text-sm text-ink tnum sm:text-md">{value}</dd>
              </div>
            ))}
          </dl>

          <div className="mt-[var(--space-lg)]">
            <CompareButton gearId={gear.id} />
          </div>

          {gear.officialUrl && (
            <a href={gear.officialUrl} target="_blank" rel="noopener noreferrer" className="link-type mt-[var(--space-md)] inline-flex min-h-11 items-center text-sm text-ink-2">
              {t('officialPage')} ↗
            </a>
          )}
        </div>
      </div>

      <div className="mt-[var(--space-2xl)] grid gap-[var(--space-xl)] md:grid-cols-[repeat(2,minmax(0,1fr))] xl:grid-cols-[repeat(3,minmax(0,1fr))]">
        {groups.map(g => <SpecGroup key={g.title} {...g} none={tc('none')} />)}
      </div>
    </main>
  );
}
