'use client';

import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { useCompareIds } from '@/lib/compare';

export default function CompareButton({ gearId }: { gearId: string }) {
  const [selectedIds, setSelectedIds] = useCompareIds();
  const tc = useTranslations('Common');
  const isSelected = selectedIds.includes(gearId);

  return (
    <div className="flex flex-wrap items-center gap-x-[var(--space-lg)] gap-y-[var(--space-xs)]">
      <button
        type="button"
        aria-pressed={isSelected}
        onClick={() => setSelectedIds(isSelected ? selectedIds.filter(id => id !== gearId) : [...selectedIds, gearId])}
        className={`h-11 whitespace-nowrap border px-[var(--space-lg)] text-sm font-bold transition-colors duration-[var(--dur-short)] ease-out ${
          isSelected ? 'border-ink bg-ink text-paper' : 'border-ink text-ink hover:bg-ink hover:text-paper'
        }`}
      >
        {isSelected ? tc('inCompare') : tc('addCompare')}
      </button>

      {selectedIds.length > 0 && (
        <Link href={`/compare?ids=${selectedIds.join(',')}`} className="link-type inline-flex min-h-11 items-center text-sm tnum">
          {tc('compareNow', { count: selectedIds.length })} →
        </Link>
      )}
    </div>
  );
}
