package com.lenshistory.backend.controller;

import com.lenshistory.backend.model.Brand;
import com.lenshistory.backend.repository.BrandRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/brand")
@CrossOrigin(origins = "*")
public class BrandController {

    private final BrandRepository brandRepository;

    public BrandController(BrandRepository brandRepository) {
        this.brandRepository = brandRepository;
    }

    @GetMapping
    public ResponseEntity<List<Brand>> getAllBrands() {
        return ResponseEntity.ok(brandRepository.findAll());
    }
}
