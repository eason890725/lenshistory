package com.lenshistory.backend.repository;

import com.lenshistory.backend.model.Gear;
import com.lenshistory.backend.model.GearMount;
import com.lenshistory.backend.model.Mount;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface GearMountRepository extends JpaRepository<GearMount, Long> {
    List<GearMount> findByGearId(Long gearId);
    List<GearMount> findByMountId(Long mountId);
    Optional<GearMount> findByGearAndMount(Gear gear, Mount mount);
}
