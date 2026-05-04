package com.lenshistory.backend.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "brands")
@Data
@NoArgsConstructor
public class Brand {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "name_i18n_id", referencedColumnName = "id")
    private I18nString nameI18n;

    @Column(unique = true, nullable = false, length = 100)
    private String slug;

    @Column(name = "founded_year")
    private Integer foundedYear;

    @Column(length = 100)
    private String country;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
