import type { Metadata } from "next";
import { Geist, Geist_Mono, Chiron_Sung_HK } from "next/font/google";
import "../globals.css";
import {NextIntlClientProvider, hasLocale} from 'next-intl';
import {getMessages, setRequestLocale} from 'next-intl/server';
import {notFound} from 'next/navigation';
import {routing} from '@/i18n/routing';
import SiteHeader from '@/components/site/SiteHeader';
import SiteFooter from '@/components/site/SiteFooter';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// CJK + Latin serif for headings. Google serves it in unicode-range slices, so pages only fetch the glyphs they use.
const chironSung = Chiron_Sung_HK({
  variable: "--font-chiron-sung",
  weight: ["400", "700"],
  subsets: ["latin"],
  preload: false,
  adjustFontFallback: false,
});

export const metadata: Metadata = {
  title: "LensHistory 鏡頭歷史",
  description: "無反光鏡時代的相機與鏡頭規格總目",
};

type Props = {
  children: React.ReactNode;
  params: Promise<{locale: string}>;
};

export default async function LocaleLayout({children, params}: Props) {
  const {locale} = await params;

  if (!hasLocale(routing.locales, locale)) {
    notFound();
  }

  setRequestLocale(locale);
  const messages = await getMessages();

  return (
    <html
      lang={locale === 'zh' ? 'zh-Hant-TW' : 'en'}
      className={`${geistSans.variable} ${geistMono.variable} ${chironSung.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <NextIntlClientProvider messages={messages}>
          <SiteHeader />
          <div className="flex-1">{children}</div>
          <SiteFooter />
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
