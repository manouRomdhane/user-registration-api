package com.example.csvapp.dto;

public class CsvCreateResponse {

    private final String fileName;
    private final String path;
    private final String message;

    public CsvCreateResponse(String fileName, String path, String message) {
        this.fileName = fileName;
        this.path = path;
        this.message = message;
    }

    public String getFileName() {
        return fileName;
    }

    public String getPath() {
        return path;
    }

    public String getMessage() {
        return message;
    }
}
