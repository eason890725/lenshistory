'use client';

import { ChevronLeft } from 'lucide-react';
import { useRouter } from 'next/navigation';

// router.back() keeps the database filters and scroll position the user came from
export default function BackButton({ label }: { label: string }) {
  const router = useRouter();
  return (
    <button
      onClick={() => router.back()}
      className="group flex items-center gap-2 text-gray-400 hover:text-white transition-colors mb-8"
    >
      <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
      <span className="text-xs uppercase tracking-[0.2em] font-medium">{label}</span>
    </button>
  );
}
