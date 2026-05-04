package com.lenshistory.backend.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "mounts")
@Data
@NoArgsConstructor
public class Mount {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false, length = 100)
    private String name;

    @Column(name = "flange_distance_mm", precision = 5, scale = 2, nullable = false)
    private BigDecimal flangeDistanceMm;

    @ManyToOne
    @JoinColumn(name = "brand_id", referencedColumnName = "id")
    private Brand brand;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
