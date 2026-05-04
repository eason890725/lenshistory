package com.lenshistory.backend.repository;

import com.lenshistory.backend.model.I18nString;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface I18nStringRepository extends JpaRepository<I18nString, Long> {
    Optional<I18nString> findByKeyName(String keyName);
}
