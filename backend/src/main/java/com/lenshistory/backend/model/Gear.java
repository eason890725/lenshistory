package com.lenshistory.backend.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "gears")
@Data
@NoArgsConstructor
public class Gear {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "brand_id", referencedColumnName = "id", nullable = false)
    private Brand brand;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "model_name_i18n_id", referencedColumnName = "id")
    private I18nString modelNameI18n;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "description_i18n_id", referencedColumnName = "id")
    private I18nString descriptionI18n;

    @Column(name = "gear_type", nullable = false, length = 50)
    private String gearType; // 'LENS', 'CAMERA_BODY'

    // --- Series / Type ---
    @Column(length = 50)
    private String series;          // e.g. "GM", "G", "Art", "Contemporary"

    @Column(length = 50)
    private String lensType;        // e.g. "1.Wide", "2.Standard", "3.Tele" (zoom only)

    // --- Focal length ---
    @Column(name = "focal_length_min_mm")
    private Integer focalLengthMinMm;

    @Column(name = "focal_length_max_mm")
    private Integer focalLengthMaxMm;

    private Double zoomRatio;       // e.g. 2.0, 2.9 (zoom only)

    // --- Aperture ---
    @Column(name = "aperture_max", precision = 4, scale = 2)
    private BigDecimal apertureMax;

    @Column(name = "aperture_min", precision = 4, scale = 2)
    private BigDecimal apertureMin;

    // --- Physical specs ---
    private Double lengthMm;        // (L) in mm
    private Double diameterMm;      // (D) in mm

    @Column(name = "weight_grams")
    private Integer weightGrams;    // (W) in grams

    @Column(name = "dimensions")
    private String dimensions;      // formatted string "D x L mm"

    private Double filterSizeMm;    // filter thread diameter in mm, null if not applicable

    // --- Optical performance ---
    private Double closeFocusCm;    // close focus distance in cm
    private Double maxMagnification;// e.g. 0.24

    @Column(name = "optical_structure")
    private String opticalStructure;

    // --- Features ---
    private Boolean hasOIS;         // Optical Image Stabilisation
    private Boolean hasWeatherSeal; // IP dust/moisture resistance
    private Boolean hasApertureRing;// Physical aperture ring
    private Boolean hasCustomButton;// Customizable button on lens

    // --- Pricing & Release ---
    @Column(name = "release_year")
    private Integer releaseYear;

    private LocalDate launchDate;   // exact launch date
    private String launchSince;     // e.g. "5å¹?9?? - how long since launch

    @Column(precision = 10, scale = 2)
    private BigDecimal launchPrice; // price at launch in TWD

    // --- Format / Display ---
    @Column(name = "sensor_format", length = 100)
    private String sensorFormat;

    @Column(name = "image_url")
    private String imageUrl;

    // --- Camera Body Specific Specs ---
    @Column(name = "megapixels")
    private Double megapixels;      // Resolution in MP

    @Column(name = "sensor_type")
    private String sensorType;      // e.g. "BSI-CMOS", "Stacked CMOS"

    @Column(name = "processor")
    private String processor;       // e.g. "BIONZ XR"

    @Column(name = "max_iso")
    private Integer maxIso;

    @Column(name = "video_resolution")
    private String videoResolution; // e.g. "8K 30p, 4K 120p"

    @Column(name = "continuous_shooting_fps")
    private Double continuousShootingFps;

    @Column(name = "has_ibis")
    private Boolean hasIBIS;        // In-body Image Stabilization

    @Column(name = "shutter_speed_range")
    private String shutterSpeedRange;

    @Column(name = "autofocus_points")
    private Integer autofocusPoints;

    @Column(name = "screen_type")
    private String screenType;

    @Column(name = "battery_life_shots")
    private Integer batteryLifeShots;

    @Column(name = "card_slots")
    private String cardSlots;

    // --- Timestamps ---
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @OneToMany(mappedBy = "gear", cascade = CascadeType.ALL, fetch = FetchType.EAGER)
    private java.util.List<GearMount> mounts = new java.util.ArrayList<>();

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
