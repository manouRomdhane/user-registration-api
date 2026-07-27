import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CsvService } from './csv.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  fileName = 'empty.csv';
  statusMessage = '';
  isLoading = false;

  constructor(private readonly csvService: CsvService) {}

  downloadEmptyCsv(): void {
    this.isLoading = true;
    this.statusMessage = '';

    this.csvService.downloadEmptyCsv(this.fileName || 'empty.csv').subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const anchor = document.createElement('a');
        const name = this.fileName?.endsWith('.csv')
          ? this.fileName
          : `${this.fileName || 'empty'}.csv`;
        anchor.href = url;
        anchor.download = name;
        anchor.click();
        window.URL.revokeObjectURL(url);
        this.statusMessage = `Fichier « ${name} » téléchargé.`;
        this.isLoading = false;
      },
      error: () => {
        this.statusMessage = 'Erreur lors du téléchargement du CSV.';
        this.isLoading = false;
      },
    });
  }

  createEmptyCsvOnServer(): void {
    this.isLoading = true;
    this.statusMessage = '';

    this.csvService.createEmptyCsvOnServer(this.fileName || undefined).subscribe({
      next: (response) => {
        this.statusMessage = `${response.message} → ${response.fileName}`;
        this.isLoading = false;
      },
      error: () => {
        this.statusMessage = 'Erreur lors de la création du CSV sur le serveur.';
        this.isLoading = false;
      },
    });
  }
}
