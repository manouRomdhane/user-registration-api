package com.example.csvapp;

import com.example.csvapp.dto.CsvCreateResponse;
import com.example.csvapp.service.CsvService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CsvServiceTest {

    @TempDir
    Path tempDir;

    @Test
    void createEmptyCsv_createsBlankFileNamedWithDateAndTime() throws Exception {
        CsvService service = new CsvService(tempDir.toString());

        CsvCreateResponse response = service.createEmptyCsv();

        assertTrue(response.getFileName().matches("\\d{4}-\\d{2}-\\d{2}_\\d{2}-\\d{2}\\.csv"));
        Path created = Path.of(response.getPath());
        assertTrue(Files.exists(created));
        assertEquals(0, Files.size(created));
        assertEquals("Fichier CSV vide créé avec succès", response.getMessage());
    }
}
