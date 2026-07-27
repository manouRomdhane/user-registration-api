import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CsvCreateResponse, CsvService } from './csv.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  loading = false;
  result: CsvCreateResponse | null = null;
  error: string | null = null;

  constructor(private readonly csvService: CsvService) {}

  createCsv(): void {
    this.loading = true;
    this.result = null;
    this.error = null;

    this.csvService.createEmptyCsv().subscribe({
      next: (response) => {
        this.result = response;
        this.loading = false;
      },
      error: (err) => {
        this.error = err?.error?.message || 'Erreur lors de la création du fichier CSV';
        this.loading = false;
      }
    });
  }
}
