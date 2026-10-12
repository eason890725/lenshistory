'use client';

import { Fragment, useState } from 'react';
import { Link } from '@/i18n/routing';

export type CompareColumn = { id: string; href: string; brand: string; name: string; image?: string };
// A cell is null when the row doesn't apply to that item (e.g. a lens row for a camera body)
export type CompareRow = { label: string; values: (string | null)[] };
export type CompareSection = { title: string; rows: CompareRow[] };

function isSame(row: CompareRow) {
  const applicable = row.values.filter((v): v is string => v !== null);
  return applicable.length > 1 && applicable.every(v => v === applicable[0]);
}

export default function CompareTable({
  columns,
  sections,
  labels,
}: {
  columns: CompareColumn[];
  sections: CompareSection[];
  labels: { diffOnly: string; noImage: string };
}) {
  const [diffOnly, setDiffOnly] = useState(false);
  const visible = sections
    .map(s => ({ ...s, rows: diffOnly ? s.rows.filter(r => !isSame(r)) : s.rows }))
    .filter(s => s.rows.length > 0);

  return (
    <>
      {columns.length > 1 && (
        <label className="mt-[var(--space-lg)] inline-flex min-h-11 cursor-pointer items-center gap-[var(--space-sm)] text-sm text-ink-2">
          <input
            type="checkbox"
            checked={diffOnly}
            onChange={e => setDiffOnly(e.target.checked)}
            className="size-4 accent-[var(--color-accent)]"
          />
          {labels.diffOnly}
        </label>
      )}

      <div className="mt-[var(--space-md)] overflow-x-auto">
        <table className="w-full min-w-[40rem] border-collapse text-left text-sm tnum">
          <thead>
            <tr>
              <th className="sticky left-0 z-10 w-40 bg-paper" />
              {columns.map(c => (
                <th key={c.id} scope="col" className="min-w-[12rem] px-[var(--space-sm)] pb-[var(--space-md)] align-top font-normal">
                  <Link href={c.href} className="group block">
                    <div className="plate flex aspect-square items-center justify-center p-[var(--space-md)]">
                      {c.image ? (
                        <img src={c.image} alt={c.name} width={400} height={400} className="max-h-full max-w-full object-contain" />
                      ) : (
                        <span className="label">{labels.noImage}</span>
                      )}
                    </div>
                    <p className="label mt-[var(--space-sm)]">{c.brand}</p>
                    <p className="mt-[var(--space-2xs)] font-display text-md font-bold leading-snug text-ink group-hover:text-accent">{c.name}</p>
                  </Link>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {visible.map(s => (
              <Fragment key={s.title}>
                <tr>
                  <th colSpan={columns.length + 1} scope="colgroup" className="label border-b border-ink pt-[var(--space-lg)] pb-[var(--space-xs)] text-left font-normal">
                    {s.title}
                  </th>
                </tr>
                {s.rows.map(r => (
                  <tr key={r.label} className="border-b border-rule">
                    <th scope="row" className="sticky left-0 z-10 bg-paper py-[var(--space-sm)] pr-[var(--space-md)] font-normal text-muted">{r.label}</th>
                    {r.values.map((v, i) => (
                      <td key={columns[i].id} className="px-[var(--space-sm)] py-[var(--space-sm)] text-ink">{v ?? ''}</td>
                    ))}
                  </tr>
                ))}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
