package com.example.csvapp.controller;

import com.example.csvapp.dto.CsvCreateResponse;
import com.example.csvapp.service.CsvService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.util.Map;

@RestController
@RequestMapping("/api/csv")
@CrossOrigin(origins = {"http://localhost:4200"})
public class CsvController {

    private final CsvService csvService;

    public CsvController(CsvService csvService) {
        this.csvService = csvService;
    }

    @PostMapping("/create")
    public ResponseEntity<?> createEmptyCsv() {
        try {
            CsvCreateResponse response = csvService.createEmptyCsv();
            return ResponseEntity.status(HttpStatus.CREATED).body(response);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("message", "Impossible de créer le fichier CSV: " + e.getMessage()));
        }
    }
}
