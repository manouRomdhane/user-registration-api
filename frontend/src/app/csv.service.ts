import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CsvCreateResponse {
  fileName: string;
  path: string;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class CsvService {
  private readonly apiUrl = 'http://localhost:8080/api/csv';

  constructor(private readonly http: HttpClient) {}

  createEmptyCsv(): Observable<CsvCreateResponse> {
    return this.http.post<CsvCreateResponse>(`${this.apiUrl}/create`, {});
  }
}
