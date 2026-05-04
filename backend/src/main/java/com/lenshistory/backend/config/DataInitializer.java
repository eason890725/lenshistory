package com.lenshistory.backend.config;

import com.lenshistory.backend.model.*;
import com.lenshistory.backend.repository.*;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.ClassPathResource;
import java.io.InputStream;

@Component
public class DataInitializer implements CommandLineRunner {

    private final BrandRepository brandRepo;
    private final MountRepository mountRepo;
    private final GearRepository gearRepo;
    private final GearMountRepository gearMountRepo;
    private final I18nStringRepository i18nRepo;
    private final PriceTrackingRepository priceRepo;

    public DataInitializer(
            BrandRepository brandRepo,
            MountRepository mountRepo,
            GearRepository gearRepo,
            GearMountRepository gearMountRepo,
            I18nStringRepository i18nRepo,
            PriceTrackingRepository priceRepo) {
        this.brandRepo = brandRepo;
        this.mountRepo = mountRepo;
        this.gearRepo = gearRepo;
        this.gearMountRepo = gearMountRepo;
        this.i18nRepo = i18nRepo;
        this.priceRepo = priceRepo;
    }

    @Override
    @Transactional
    public void run(String... args) throws Exception {
        System.out.println("DataInitializer RUN STARTING...");
        try {
            // Clear existing data for fresh start - Correct Order for FK constraints
            priceRepo.deleteAll();
            gearMountRepo.deleteAll();
            gearRepo.deleteAll();
            mountRepo.deleteAll();
            brandRepo.deleteAll();
            i18nRepo.deleteAll();
            Brand sony = getOrCreateBrand("sony", "Sony", "Sony", 1946, "Japan");
            Brand canon = getOrCreateBrand("canon", "Canon", "佳能", 1937, "Japan");
            Brand nikon = getOrCreateBrand("nikon", "Nikon", "尼康", 1917, "Japan");
            Brand fujifilm = getOrCreateBrand("fujifilm", "Fujifilm", "富士", 1934, "Japan");
            Brand sigma = getOrCreateBrand("sigma", "Sigma", "?�馬", 1961, "Japan");
            Brand tamron = getOrCreateBrand("tamron", "Tamron", "騰�?", 1950, "Japan");

            Mount sonyE = getOrCreateMount("Sony E", new BigDecimal("18.00"), sony);
            Mount canonRF = getOrCreateMount("Canon RF", new BigDecimal("20.00"), canon);
            Mount nikonZ = getOrCreateMount("Nikon Z", new BigDecimal("16.00"), nikon);
            Mount fujiX = getOrCreateMount("Fujifilm X", new BigDecimal("17.70"), fujifilm);
            Mount fujiG = getOrCreateMount("Fujifilm G", new BigDecimal("26.70"), fujifilm);

            ObjectMapper mapper = new ObjectMapper();
            TypeReference<List<Map<String, Object>>> typeRef = new TypeReference<>() {};
            
            // Load Lenses
            InputStream lensIs = new ClassPathResource("lenses.json").getInputStream();
            List<Map<String, Object>> lensList = mapper.readValue(lensIs, typeRef);
            
            // Load Bodies
            InputStream bodyIs = new ClassPathResource("bodies.json").getInputStream();
            List<Map<String, Object>> bodyList = mapper.readValue(bodyIs, typeRef);

            List<Map<String, Object>> allGears = new java.util.ArrayList<>();
            allGears.addAll(lensList);
            allGears.addAll(bodyList);

            for (Map<String, Object> l : allGears) {
                String brandName = str(l, "brand");
                if (brandName == null) continue;
                String brandSlug = brandName.toLowerCase();
                Brand b = getOrCreateBrand(brandSlug, brandName, brandName, 2000, "Unknown");

                String modelName = str(l, "modelName");
                if (modelName == null) continue;
                String key = "gear." + brandSlug + "." + modelName.replaceAll("[^a-zA-Z0-9]", "").toLowerCase() + ".name";

                I18nString name = getOrCreateI18n(key, modelName, modelName);
                Optional<Gear> existingGear = gearRepo.findByModelNameI18n(name);
                
                Gear g = existingGear.orElse(new Gear());
                g.setBrand(b);
                g.setModelNameI18n(name);
                
                String gearType = str(l, "gearType");
                g.setGearType(gearType != null ? gearType : "LENS");
                
                g.setSeries(str(l, "series"));
                g.setLensType(str(l, "lensType"));
                g.setFocalLengthMinMm(intVal(l, "focalLengthMinMm"));
                g.setFocalLengthMaxMm(intVal(l, "focalLengthMaxMm"));
                g.setZoomRatio(dblVal(l, "zoomRatio"));
                g.setApertureMax(decVal(l, "apertureMax"));
                g.setApertureMin(decVal(l, "apertureMin"));
                g.setLengthMm(dblVal(l, "lengthMm"));
                g.setDiameterMm(dblVal(l, "diameterMm"));
                g.setWeightGrams(intVal(l, "weightGrams"));
                g.setDimensions(str(l, "dimensions"));
                g.setFilterSizeMm(dblVal(l, "filterSizeMm"));
                g.setCloseFocusCm(dblVal(l, "closeFocusCm"));
                g.setMaxMagnification(dblVal(l, "maxMagnification"));
                g.setHasOIS(boolVal(l, "hasOIS"));
                g.setHasWeatherSeal(boolVal(l, "hasWeatherSeal"));
                g.setHasApertureRing(boolVal(l, "hasApertureRing"));
                g.setHasCustomButton(boolVal(l, "hasCustomButton"));
                g.setReleaseYear(intVal(l, "releaseYear"));
                
                // Body specific
                g.setMegapixels(dblVal(l, "megapixels"));
                g.setSensorType(str(l, "sensorType"));
                g.setProcessor(str(l, "processor"));
                g.setMaxIso(intVal(l, "maxIso"));
                g.setVideoResolution(str(l, "videoResolution"));
                g.setContinuousShootingFps(dblVal(l, "continuousShootingFps"));
                g.setHasIBIS(boolVal(l, "hasIBIS"));
                g.setShutterSpeedRange(str(l, "shutterSpeedRange"));
                g.setAutofocusPoints(intVal(l, "autofocusPoints"));
                g.setScreenType(str(l, "screenType"));
                g.setBatteryLifeShots(intVal(l, "batteryLifeShots"));
                g.setCardSlots(str(l, "cardSlots"));

                String dateStr = str(l, "launchDate");
                if (dateStr != null) {
                    try { g.setLaunchDate(LocalDate.parse(dateStr)); } catch (Exception ignored) {}
                }
                g.setLaunchSince(str(l, "launchSince"));
                g.setLaunchPrice(decVal(l, "launchPrice"));
                g.setSensorFormat(str(l, "sensorFormat"));
                g.setImageUrl(str(l, "imageUrl"));

                g = gearRepo.save(g);

                // Mount association - Dynamic based on brand or explicit 'mounts' field
                List<String> mountNames = (List<String>) l.get("mounts");
                if (mountNames != null) {
                    for (String mName : mountNames) {
                        Mount m = mountRepo.findByName(mName).orElseGet(() -> {
                            // If mount doesn't exist, we might need to create it 
                            // But usually we pre-create the major ones
                            Mount newM = new Mount();
                            newM.setName(mName);
                            newM.setFlangeDistanceMm(new BigDecimal("20.00")); // Default
                            return mountRepo.save(newM);
                        });
                        if (gearMountRepo.findByGearAndMount(g, m).isEmpty()) {
                            GearMount gm = new GearMount();
                            gm.setGear(g);
                            gm.setMount(m);
                            gm.setIsNative(false); // Usually third party if explicitly listed
                            g.getMounts().add(gm);
                            gearMountRepo.save(gm);
                        }
                    }
                } else {
                    // Default logic based on brand
                    Mount targetMount = sonyE;
                    boolean isNative = true;
                    if (brandSlug.equals("canon")) targetMount = canonRF;
                    else if (brandSlug.equals("nikon")) targetMount = nikonZ;
                    else if (brandSlug.equals("fujifilm")) {
                        String fmt = str(l, "sensorFormat");
                        targetMount = (fmt != null && fmt.contains("Medium")) ? fujiG : fujiX;
                    } else if (brandSlug.equals("sigma") || brandSlug.equals("tamron")) {
                        targetMount = sonyE; // Default for 3rd party if not specified
                        isNative = false;
                    }

                    if (gearMountRepo.findByGearAndMount(g, targetMount).isEmpty()) {
                        GearMount gm = new GearMount();
                        gm.setGear(g);
                        gm.setMount(targetMount);
                        gm.setIsNative(isNative);
                        g.getMounts().add(gm);
                        gearMountRepo.save(gm);
                    }
                }
            }

            System.out.println("Database expanded with " + allGears.size() + " gear items (Lenses & Bodies)!");
        } catch (Exception e) {
            System.err.println("SEEDED ERROR: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private String str(Map<String, Object> m, String k) {
        Object v = m.get(k);
        if (v == null) return null;
        String s = v.toString().trim();
        return s.isEmpty() ? null : s;
    }

    private Integer intVal(Map<String, Object> m, String k) {
        Object v = m.get(k);
        if (v == null) return null;
        return ((Number) v).intValue();
    }

    private Double dblVal(Map<String, Object> m, String k) {
        Object v = m.get(k);
        if (v == null) return null;
        return ((Number) v).doubleValue();
    }

    private BigDecimal decVal(Map<String, Object> m, String k) {
        Object v = m.get(k);
        if (v == null) return null;
        return new BigDecimal(v.toString());
    }

    private Boolean boolVal(Map<String, Object> m, String k) {
        Object v = m.get(k);
        if (v == null) return null;
        return (Boolean) v;
    }

    private Brand getOrCreateBrand(String slug, String en, String zh, int year, String country) {
        return brandRepo.findBySlug(slug).orElseGet(() -> {
            I18nString name = getOrCreateI18n("brand." + slug + ".name", en, zh);
            Brand b = new Brand();
            b.setSlug(slug);
            b.setNameI18n(name);
            b.setFoundedYear(year);
            b.setCountry(country);
            return brandRepo.save(b);
        });
    }

    private Mount getOrCreateMount(String name, BigDecimal flange, Brand brand) {
        return mountRepo.findByName(name).orElseGet(() -> {
            Mount m = new Mount();
            m.setName(name);
            m.setFlangeDistanceMm(flange);
            m.setBrand(brand);
            return mountRepo.save(m);
        });
    }

    private I18nString getOrCreateI18n(String key, String en, String zh) {
        return i18nRepo.findByKeyName(key).orElseGet(() -> {
            I18nString i18n = new I18nString();
            i18n.setKeyName(key);
            i18n.setEnUs(en);
            i18n.setZhTw(zh);
            return i18nRepo.save(i18n);
        });
    }
}
