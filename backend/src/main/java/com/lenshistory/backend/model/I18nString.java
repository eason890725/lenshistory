package com.lenshistory.backend.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "i18n_strings")
@Data
@NoArgsConstructor
public class I18nString {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "key_name", unique = true, nullable = false)
    private String keyName;

    @Column(name = "zh_tw", columnDefinition = "TEXT", nullable = false)
    private String zhTw;

    @Column(name = "en_us", columnDefinition = "TEXT", nullable = false)
    private String enUs;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
