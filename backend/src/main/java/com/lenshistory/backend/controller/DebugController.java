package com.lenshistory.backend.controller;

import com.lenshistory.backend.config.DataInitializer;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/debug")
public class DebugController {

    private final DataInitializer dataInitializer;

    public DebugController(DataInitializer dataInitializer) {
        this.dataInitializer = dataInitializer;
    }

    @GetMapping("/seed")
    public String seed() {
        try {
            dataInitializer.run();
            return "Seed successful!";
        } catch (Exception e) {
            return "Seed failed: " + e.getMessage();
        }
    }
}
