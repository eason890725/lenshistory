package com.lenshistory.backend.repository;

import com.lenshistory.backend.model.PriceTracking;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PriceTrackingRepository extends JpaRepository<PriceTracking, Long> {
    List<PriceTracking> findByGearIdOrderByRecordedDateDesc(Long gearId);
}
