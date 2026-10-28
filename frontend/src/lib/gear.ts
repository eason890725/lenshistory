// Types and helpers only. The data itself lives in gear-data.ts so client components
// that import from here don't pull products.json into the browser bundle.

// Shape of one record in products.json. scripts/validate-products.mjs keeps the data in line with it.
export type Gear = {
  id: string;
  slug?: string;
  brand: string;
  modelName: string;
  gearType: 'LENS' | 'CAMERA_BODY';
  aliases?: string[];
  image_url?: string;
  officialUrl?: string;
  mounts?: { mount: { name: string } }[];
  sensorFormat?: string;
  series?: string;
  category?: string;
  releaseYear?: number;   // year it was announced (kept separate so the year filter stays simple)
  releaseMonth?: number;  // 1-12, month it was announced, when known
  launchPrice?: number;     // Taiwan launch suggested price (NT$)
  retailPrice?: number;     // current Taiwan street price for new stock; cards and sorting use it only when there is no launch price
  retailPriceDate?: string; // "2026-10", when retailPrice was checked
  weightGrams?: number | string;
  dimensions?: string;
  hasWeatherSeal?: boolean;

  // lens
  lensType?: string;
  focalLengthMinMm?: number;
  focalLengthMaxMm?: number;
  apertureMax?: number | string;
  minAperture?: string;
  maxMagnification?: number | string;
  closeFocus?: string;
  filterSizeMm?: number;
  motorType?: string;
  opticalDesign?: string;
  specialElements?: string;
  coatings?: string;
  hasOIS?: boolean;
  hasApertureRing?: boolean;
  hasCustomButton?: boolean;

  // camera body
  fixedLens?: string;       // built-in lens of a fixed-lens camera (a body with no mounts), e.g. "23mm F2 (35mm equiv.)"
  megapixels?: number | string;
  sensorType?: string;
  processor?: string;
  isoRange?: string;
  burstSpeed?: string;
  afPoints?: string;
  afTargets?: string;
  afRange?: string;
  hasIBIS?: boolean;
  ibisRating?: string;
  videoResolution?: string;
  videoColorDepth?: string;
  logSupport?: string;
  evfResolution?: string;
  evfMagnification?: string;
  lcdSpec?: string;
  cardSlots?: string;
  batterySpec?: string;
  ports?: string;
};

// weightGrams is a number, or free text like "Approx. 630 g (including battery and card)"
export function weightLabel(g: Gear) {
  return typeof g.weightGrams === 'number' ? `${g.weightGrams}g` : g.weightGrams;
}

export function weightValue(g: Gear) {
  return Number(String(g.weightGrams ?? '').replace(/,/g, '').match(/\d+(\.\d+)?/)?.[0]) || undefined;
}

// Filter category: a body with no mount is a fixed-lens camera (action cams often publish no lens spec, so fixedLens can be empty)
export function gearKind(g: Gear) {
  return g.gearType === 'LENS' ? 'LENS' : g.mounts?.length ? 'CAMERA_BODY' : 'FIXED_LENS';
}

// Launch price when known, else the street price
export function priceValue(g: Gear) {
  return g.launchPrice ?? g.retailPrice;
}

// "NT$39,990", or "Street NT$32,990" when only the street price is known
export function priceText(g: Gear, streetLabel: string) {
  if (g.launchPrice) return `NT$${g.launchPrice.toLocaleString()}`;
  if (g.retailPrice) return `${streetLabel} NT$${g.retailPrice.toLocaleString()}`;
}

// Stored in a spec field when the official spec confirms the feature doesn't exist (no EVF, no Log); shown as 無 / None
export const NONE = 'None';

// "2026.09", or just "2026" when the month isn't known
export function releaseLabel(g: Gear) {
  if (!g.releaseYear) return undefined;
  return g.releaseMonth ? `${g.releaseYear}.${String(g.releaseMonth).padStart(2, '0')}` : String(g.releaseYear);
}

// Sort key: a known month sorts after "month unknown" within the same year
export function releaseKey(g: Gear) {
  return (g.releaseYear || 0) * 100 + (g.releaseMonth || 0);
}

export function focalLength(g: Gear) {
  if (!g.focalLengthMinMm) return undefined;
  return g.focalLengthMinMm === g.focalLengthMaxMm
    ? `${g.focalLengthMinMm}mm`
    : `${g.focalLengthMinMm}-${g.focalLengthMaxMm}mm`;
}
