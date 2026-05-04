package com.lenshistory.backend.controller;

import com.lenshistory.backend.model.Gear;
import com.lenshistory.backend.repository.GearRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/gear")
@CrossOrigin(origins = "*")
public class GearController {

    private final GearRepository gearRepository;

    public GearController(GearRepository gearRepository) {
        this.gearRepository = gearRepository;
    }

    @GetMapping
    public ResponseEntity<List<Gear>> getAllGears() {
        return ResponseEntity.ok(gearRepository.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Gear> getGearById(@PathVariable Long id) {
        return gearRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/search")
    public ResponseEntity<List<Gear>> searchGears(
            @RequestParam(required = false) Long brandId,
            @RequestParam(required = false) String type,
            @RequestParam(required = false) String q) {
        List<Gear> results;
        if (brandId != null && type != null) {
            results = gearRepository.findByBrandIdAndGearType(brandId, type);
        } else if (brandId != null) {
            results = gearRepository.findByBrandId(brandId);
        } else if (type != null) {
            results = gearRepository.findByGearType(type);
        } else {
            results = gearRepository.findAll();
        }
        
        if (q != null && !q.isEmpty()) {
            results = results.stream()
                    .filter(gear -> {
                        String nameEn = gear.getModelNameI18n().getEnUs().toLowerCase();
                        String nameZh = gear.getModelNameI18n().getZhTw().toLowerCase();
                        String query = q.toLowerCase();
                        return nameEn.contains(query) || nameZh.contains(query);
                    })
                    .toList();
        }
        
        return ResponseEntity.ok(results);
    }

    @GetMapping("/compare")
    public ResponseEntity<List<Gear>> compareGears(@RequestParam List<Long> ids) {
        return ResponseEntity.ok(gearRepository.findAllById(ids));
    }
}
