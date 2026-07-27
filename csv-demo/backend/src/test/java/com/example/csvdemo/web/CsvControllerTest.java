package com.example.csvdemo.web;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@TestPropertySource(properties = "csv.export-dir=${java.io.tmpdir}/csv-demo-exports")
class CsvControllerTest {

	@Autowired
	private MockMvc mockMvc;

	@Test
	void downloadEmptyCsvReturnsAttachment() throws Exception {
		mockMvc.perform(get("/api/csv/empty").param("fileName", "rapport.csv"))
				.andExpect(status().isOk())
				.andExpect(header().string("Content-Disposition", "attachment; filename=\"rapport.csv\""));
	}

	@Test
	void createEmptyCsvOnServer() throws Exception {
		mockMvc.perform(post("/api/csv/empty").param("fileName", "nouveau.csv"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.fileName").value("nouveau.csv"))
				.andExpect(jsonPath("$.size").value(0))
				.andExpect(jsonPath("$.message").value("Empty CSV file created"));
	}
}
