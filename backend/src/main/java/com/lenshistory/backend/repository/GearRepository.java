package com.lenshistory.backend.repository;

import com.lenshistory.backend.model.Gear;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface GearRepository extends JpaRepository<Gear, Long> {
    List<Gear> findByBrandId(Long brandId);
    
    // For simple search across model name (we'll do a basic fetch and filter for now, 
    // or we can just return all and filter in frontend for simplicity in this MVP)
    List<Gear> findByGearType(String gearType);
    List<Gear> findByBrandIdAndGearType(Long brandId, String gearType);
    
    java.util.Optional<Gear> findByModelNameI18n(com.lenshistory.backend.model.I18nString modelNameI18n);
}
