package com.example.csvdemo.web;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/csv")
@CrossOrigin(origins = {"http://localhost:4200"})
public class CsvController {

	private final Path exportDirectory;

	public CsvController(@Value("${csv.export-dir:./exports}") String exportDir) throws Exception {
		this.exportDirectory = Paths.get(exportDir).toAbsolutePath().normalize();
		Files.createDirectories(this.exportDirectory);
	}

	/**
	 * Downloads an empty CSV file to the browser.
	 */
	@GetMapping("/empty")
	public ResponseEntity<byte[]> downloadEmptyCsv(
			@RequestParam(defaultValue = "empty.csv") String fileName) {
		String safeName = sanitizeFileName(fileName);
		byte[] content = new byte[0];

		return ResponseEntity.ok()
				.header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + safeName + "\"")
				.contentType(MediaType.parseMediaType("text/csv"))
				.contentLength(content.length)
				.body(content);
	}

	/**
	 * Creates an empty CSV file on the server and returns its metadata.
	 */
	@PostMapping("/empty")
	public ResponseEntity<Map<String, Object>> createEmptyCsvOnServer(
			@RequestParam(required = false) String fileName) throws Exception {
		String safeName = fileName == null || fileName.isBlank()
				? "empty-" + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss")) + ".csv"
				: sanitizeFileName(fileName);

		if (!safeName.toLowerCase().endsWith(".csv")) {
			safeName = safeName + ".csv";
		}

		Path target = exportDirectory.resolve(safeName).normalize();
		if (!target.startsWith(exportDirectory)) {
			return ResponseEntity.badRequest().body(Map.of(
					"error", "Invalid file name"));
		}

		Files.writeString(target, "", StandardCharsets.UTF_8);

		return ResponseEntity.ok(Map.of(
				"message", "Empty CSV file created",
				"fileName", safeName,
				"path", target.toString(),
				"size", 0));
	}

	private static String sanitizeFileName(String fileName) {
		String cleaned = Paths.get(fileName).getFileName().toString().replaceAll("[^a-zA-Z0-9._-]", "_");
		if (cleaned.isBlank()) {
			return "empty.csv";
		}
		if (!cleaned.toLowerCase().endsWith(".csv")) {
			cleaned = cleaned + ".csv";
		}
		return cleaned;
	}
}
