import { Fragment } from 'react';
import { Link } from '@/i18n/routing';
import { setRequestLocale, getTranslations } from 'next-intl/server';
import { focalLength, weightLabel, type Gear } from '@/lib/gear';
import { gears as allGears } from '@/lib/gear-data';
import { shortName } from '@/components/gear/ProductCard';

function getCompareGears(ids: string) {
  if (!ids) return [];
  const idList = ids.split(',').map(id => id.trim());
  return allGears.filter(g => idList.includes(g.id) || (g.slug && idList.includes(g.slug)));
}

function zoomRatio(g: Gear) {
  if (!g.focalLengthMinMm || !g.focalLengthMaxMm || g.focalLengthMinMm === g.focalLengthMaxMm) return undefined;
  return `${(g.focalLengthMaxMm / g.focalLengthMinMm).toFixed(1)}x`;
}

type Value = string | number | undefined;
type Row = { section: string; label: string; type?: Gear['gearType']; get: (g: Gear) => Value };

export default async function ComparePage({
  searchParams,
  params
}: {
  searchParams: Promise<{ ids?: string }>;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const { ids = '' } = await searchParams;

  const t = await getTranslations('GearSpecs');
  const tc = await getTranslations('Common');
  const tn = await getTranslations('Navigation');
  const gears = getCompareGears(ids);

  const yesNo = (v?: boolean) => (v === undefined ? undefined : v ? tc('yes') : tc('no'));
  const L = 'LENS' as const;
  const B = 'CAMERA_BODY' as const;

  const rows: Row[] = [
    { section: t('releaseInfo'), label: t('releaseYear'), get: g => g.releaseYear },
    { section: t('releaseInfo'), label: t('launchPrice'), get: g => (g.launchPrice ? `NT$${g.launchPrice.toLocaleString()}` : undefined) },

    { section: t('optical'), label: t('focalLength'), type: L, get: g => focalLength(g) },
    { section: t('optical'), label: t('maxAperture'), type: L, get: g => (g.apertureMax ? `f/${g.apertureMax}` : undefined) },
    { section: t('optical'), label: t('minAperture'), type: L, get: g => (g.minAperture ? `f/${g.minAperture}` : undefined) },
    { section: t('optical'), label: t('zoomRatio'), type: L, get: zoomRatio },
    { section: t('optical'), label: t('closeFocus'), type: L, get: g => g.closeFocus },
    { section: t('optical'), label: t('maxMagnification'), type: L, get: g => g.maxMagnification },
    { section: t('optical'), label: t('opticalDesign'), type: L, get: g => g.opticalDesign },
    { section: t('optical'), label: t('filterSize'), type: L, get: g => (g.filterSizeMm ? `${g.filterSizeMm}mm` : undefined) },
    { section: t('features'), label: t('motorType'), type: L, get: g => g.motorType },
    { section: t('features'), label: t('ois'), type: L, get: g => yesNo(g.hasOIS) },
    { section: t('features'), label: t('apertureRing'), type: L, get: g => yesNo(g.hasApertureRing) },

    { section: t('imaging'), label: t('megapixels'), type: B, get: g => g.megapixels },
    { section: t('imaging'), label: t('sensorType'), type: B, get: g => g.sensorType },
    { section: t('imaging'), label: t('processor'), type: B, get: g => g.processor },
    { section: t('imaging'), label: t('isoRange'), type: B, get: g => g.isoRange },
    { section: t('imaging'), label: t('video'), type: B, get: g => g.videoResolution },
    { section: t('performance'), label: t('continuousShooting'), type: B, get: g => g.burstSpeed },
    { section: t('performance'), label: t('afTargets'), type: B, get: g => g.afTargets },
    { section: t('performance'), label: t('ibis'), type: B, get: g => yesNo(g.hasIBIS) },
    { section: t('hardware'), label: t('evfResolution'), type: B, get: g => g.evfResolution },
    { section: t('hardware'), label: t('lcdSpec'), type: B, get: g => g.lcdSpec },
    { section: t('hardware'), label: t('cardSlots'), type: B, get: g => g.cardSlots },
    { section: t('hardware'), label: t('batterySpec'), type: B, get: g => g.batterySpec },

    { section: t('physical'), label: t('mount'), get: g => g.mounts?.map(m => m.mount.name).join(', ') },
    { section: t('physical'), label: t('sensorFormat'), get: g => g.sensorFormat },
    { section: t('physical'), label: t('weatherSeal'), get: g => yesNo(g.hasWeatherSeal) },
    { section: t('physical'), label: t('weight'), get: g => weightLabel(g) },
    { section: t('physical'), label: t('dimensions'), get: g => g.dimensions },
  ];
  // A row shows when it applies to at least one selected item and at least one of them has a value
  const visibleRows = rows.filter(r => gears.some(g => (!r.type || r.type === g.gearType) && r.get(g) !== undefined));
  const sections = [...new Set(visibleRows.map(r => r.section))];

  return (
    <main className="mx-auto max-w-[var(--page-max)] px-[var(--page-gutter)] pt-[var(--space-xl)] pb-[var(--space-3xl)]">
      <h1 className="text-[length:var(--text-display)] font-bold leading-[1.05] tracking-[var(--tracking-display)]">{tn('compare')}</h1>

      {gears.length === 0 ? (
        <div className="mt-[var(--space-xl)] border-t border-rule pt-[var(--space-lg)]">
          <p className="max-w-[60ch] text-md text-ink-2">{tc('compareEmpty')}</p>
          <Link href="/database" className="link-type mt-[var(--space-md)] inline-flex min-h-11 items-center text-sm">
            {tn('database')} →
          </Link>
        </div>
      ) : (
        <div className="mt-[var(--space-xl)] overflow-x-auto">
          <table className="w-full min-w-[40rem] border-collapse text-left text-sm tnum">
            <thead>
              <tr>
                <th className="sticky left-0 z-10 w-40 bg-paper" />
                {gears.map(g => (
                  <th key={g.id} scope="col" className="min-w-[12rem] px-[var(--space-sm)] pb-[var(--space-md)] align-top font-normal">
                    <Link href={`/database/${g.slug || g.id}`} className="group block">
                      <div className="plate flex aspect-square items-center justify-center p-[var(--space-md)]">
                        {g.image_url ? (
                          <img src={g.image_url} alt={g.modelName} width={400} height={400} className="max-h-full max-w-full object-contain" />
                        ) : (
                          <span className="label">{t('noImage')}</span>
                        )}
                      </div>
                      <p className="label mt-[var(--space-sm)]">{g.brand}</p>
                      <p className="mt-[var(--space-2xs)] font-display text-md font-bold leading-snug text-ink group-hover:text-accent">{shortName(g)}</p>
                    </Link>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sections.map(section => (
                <Fragment key={section}>
                  <tr>
                    <th colSpan={gears.length + 1} scope="colgroup" className="label border-b border-ink pt-[var(--space-lg)] pb-[var(--space-xs)] text-left font-normal">
                      {section}
                    </th>
                  </tr>
                  {visibleRows.filter(r => r.section === section).map(r => (
                    <tr key={r.label} className="border-b border-rule">
                      <th scope="row" className="sticky left-0 z-10 bg-paper py-[var(--space-sm)] pr-[var(--space-md)] font-normal text-muted">{r.label}</th>
                      {gears.map(g => (
                        <td key={g.id} className="px-[var(--space-sm)] py-[var(--space-sm)] text-ink">
                          {(!r.type || r.type === g.gearType) ? (r.get(g) ?? '—') : ''}
                        </td>
                      ))}
                    </tr>
                  ))}
                </Fragment>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}
