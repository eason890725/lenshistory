'use client';

import { Link } from '@/i18n/routing';
import { useCompareIds } from '@/lib/compare';

export default function CompareNavLink({ label }: { label: string }) {
  const [ids] = useCompareIds();
  return (
    <Link href={ids.length ? `/compare?ids=${ids.join(',')}` : '/compare'} className="nav-link tnum">
      {label}
      {ids.length > 0 && <span className="ml-1 text-accent">{ids.length}</span>}
    </Link>
  );
}
