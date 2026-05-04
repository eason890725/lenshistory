package com.lenshistory.backend.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "gear_mounts", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"gear_id", "mount_id"})
})
@Data
@NoArgsConstructor
public class GearMount {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "gear_id", referencedColumnName = "id", nullable = false)
    @com.fasterxml.jackson.annotation.JsonIgnore
    private Gear gear;

    @ManyToOne
    @JoinColumn(name = "mount_id", referencedColumnName = "id", nullable = false)
    private Mount mount;

    @Column(name = "is_native")
    private Boolean isNative = true;

    @Column(name = "discontinued_year")
    private Integer discontinuedYear;
}
