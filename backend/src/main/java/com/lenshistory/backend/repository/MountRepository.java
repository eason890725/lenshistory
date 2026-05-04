package com.lenshistory.backend.repository;

import com.lenshistory.backend.model.Mount;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface MountRepository extends JpaRepository<Mount, Long> {
    Optional<Mount> findByName(String name);
}
