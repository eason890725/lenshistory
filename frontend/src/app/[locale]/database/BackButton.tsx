'use client';

import { useRouter } from 'next/navigation';

// router.back() keeps the database filters and scroll position the user came from
export default function BackButton({ label }: { label: string }) {
  const router = useRouter();
  return (
    <button
      type="button"
      onClick={() => router.back()}
      className="link-type mb-[var(--space-lg)] inline-flex min-h-11 items-center text-sm text-ink-2"
    >
      ← {label}
    </button>
  );
}
