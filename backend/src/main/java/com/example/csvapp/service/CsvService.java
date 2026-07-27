package com.example.csvapp.service;

import com.example.csvapp.dto.CsvCreateResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Service
public class CsvService {

    private static final DateTimeFormatter FILE_NAME_FORMAT =
            DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm");

    private final Path exportDirectory;

    public CsvService(@Value("${csv.export-dir:exports}") String exportDir) throws IOException {
        this.exportDirectory = Paths.get(exportDir).toAbsolutePath().normalize();
        Files.createDirectories(this.exportDirectory);
    }

    public CsvCreateResponse createEmptyCsv() throws IOException {
        String fileName = LocalDateTime.now().format(FILE_NAME_FORMAT) + ".csv";
        Path filePath = exportDirectory.resolve(fileName);

        // Fichier CSV blanc (vide), pas un fichier vidéo
        Files.writeString(filePath, "");

        return new CsvCreateResponse(
                fileName,
                filePath.toString(),
                "Fichier CSV vide créé avec succès"
        );
    }
}
