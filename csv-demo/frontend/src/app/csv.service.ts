import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CreateCsvResponse {
  message: string;
  fileName: string;
  path: string;
  size: number;
}

@Injectable({ providedIn: 'root' })
export class CsvService {
  private readonly apiUrl = 'http://localhost:8080/api/csv';

  constructor(private readonly http: HttpClient) {}

  /** Downloads an empty CSV file in the browser. */
  downloadEmptyCsv(fileName = 'empty.csv'): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/empty`, {
      params: { fileName },
      responseType: 'blob',
    });
  }

  /** Creates an empty CSV file on the Spring Boot server. */
  createEmptyCsvOnServer(fileName?: string): Observable<CreateCsvResponse> {
    const params: Record<string, string> = {};
    if (fileName) {
      params['fileName'] = fileName;
    }
    return this.http.post<CreateCsvResponse>(`${this.apiUrl}/empty`, null, { params });
  }
}
