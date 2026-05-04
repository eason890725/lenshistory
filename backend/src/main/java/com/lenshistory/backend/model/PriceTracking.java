package com.lenshistory.backend.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "price_trackings")
@Data
@NoArgsConstructor
public class PriceTracking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "gear_id", referencedColumnName = "id", nullable = false)
    private Gear gear;

    @Column(length = 3)
    private String currency = "USD";

    @Column(precision = 10, scale = 2)
    private BigDecimal msrp;

    @Column(name = "current_used_avg", precision = 10, scale = 2)
    private BigDecimal currentUsedAvg;

    @Column(name = "highest_recorded", precision = 10, scale = 2)
    private BigDecimal highestRecorded;

    @Column(name = "lowest_recorded", precision = 10, scale = 2)
    private BigDecimal lowestRecorded;

    @Column(name = "recorded_date", nullable = false)
    private LocalDate recordedDate;

    @Column(name = "condition_grade", length = 50)
    private String conditionGrade;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
