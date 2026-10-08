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
  releaseYear?: number;
  launchPrice?: number;
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

export function focalLength(g: Gear) {
  if (!g.focalLengthMinMm) return undefined;
  return g.focalLengthMinMm === g.focalLengthMaxMm
    ? `${g.focalLengthMinMm}mm`
    : `${g.focalLengthMinMm}-${g.focalLengthMaxMm}mm`;
}
