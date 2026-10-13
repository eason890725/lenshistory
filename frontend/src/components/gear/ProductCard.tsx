import { Link } from '@/i18n/routing';
import { focalLength, releaseLabel, type Gear } from '@/lib/gear';

export function shortName(g: Gear) {
  return g.modelName.startsWith(g.brand + ' ') ? g.modelName.slice(g.brand.length + 1) : g.modelName;
}

export function keySpec(g: Gear) {
  if (g.gearType === 'LENS') {
    const f = focalLength(g);
    return [f, g.apertureMax ? `f/${g.apertureMax}` : undefined].filter(Boolean).join(' ');
  }
  return [g.megapixels, g.sensorFormat].filter(Boolean).join(' · ');
}

type CompareProps = {
  selected: boolean;
  disabled: boolean;
  onToggle: (g: Gear) => void;
  labels: { add: string; remove: string; mixed: string };
};

// F6 product card: plate · brand · name · one mono line of facts. The optional compare toggle is the only micro-action.
export default function ProductCard({
  gear,
  noImageLabel,
  compare,
  priority = false,
}: {
  gear: Gear;
  noImageLabel: string;
  compare?: CompareProps;
  priority?: boolean;
}) {
  const name = shortName(gear);
  const facts = [releaseLabel(gear), keySpec(gear), gear.launchPrice ? `NT$${gear.launchPrice.toLocaleString()}` : undefined]
    .filter(Boolean)
    .join(' · ');

  return (
    <article className={`group relative min-w-0 ${compare?.disabled ? 'opacity-45' : ''}`}>
      <Link href={`/database/${gear.slug || gear.id}`} className="block focus-visible:outline-offset-4">
        <div className="plate flex aspect-square items-center justify-center p-[var(--space-lg)]">
          {gear.image_url ? (
            <img
              src={gear.image_url}
              alt={gear.modelName}
              width={600}
              height={600}
              loading={priority ? 'eager' : 'lazy'}
              decoding="async"
              className="max-h-full max-w-full object-contain transition-transform duration-[var(--dur-med)] ease-out group-hover:scale-[1.02]"
            />
          ) : (
            <span className="label">{noImageLabel}</span>
          )}
        </div>
        <div className="pt-[var(--space-sm)]">
          <p className="label">{gear.brand}</p>
          <h3 className="mt-[var(--space-2xs)] text-md font-bold leading-snug text-ink">{name}</h3>
          {facts && <p className="mt-[var(--space-2xs)] font-mono text-xs text-muted tnum">{facts}</p>}
        </div>
      </Link>

      {compare && (
        <button
          type="button"
          onClick={() => compare.onToggle(gear)}
          aria-pressed={compare.selected}
          aria-disabled={compare.disabled}
          title={compare.disabled ? compare.labels.mixed : undefined}
          aria-label={`${compare.selected ? compare.labels.remove : compare.labels.add}: ${gear.modelName}`}
          className="absolute left-0 top-0 grid size-11 place-items-center"
        >
          <span
            className={`block size-4 border transition-colors duration-[var(--dur-short)] ease-out ${
              compare.selected ? 'border-accent bg-accent' : 'border-rule-2 bg-paper group-hover:border-ink'
            }`}
          >
            {compare.selected && (
              <svg viewBox="0 0 16 16" className="size-full" aria-hidden="true">
                <path d="M4 8.5l2.5 2.5L12 5.5" fill="none" stroke="currentColor" strokeWidth="1.75" className="text-accent-ink" />
              </svg>
            )}
          </span>
        </button>
      )}
    </article>
  );
}
