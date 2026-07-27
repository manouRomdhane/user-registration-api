import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { AppComponent } from './app.component';

describe('AppComponent', () => {
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [provideHttpClient(), provideHttpClientTesting()]
    }).compileComponents();

    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    expect(fixture.componentInstance).toBeTruthy();
  });

  it('should call the API when the create button is clicked', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const component = fixture.componentInstance;
    fixture.detectChanges();

    component.createCsv();

    const req = httpMock.expectOne('http://localhost:8080/api/csv/create');
    expect(req.request.method).toBe('POST');
    req.flush({
      fileName: '2026-07-27_12-06.csv',
      path: '/tmp/2026-07-27_12-06.csv',
      message: 'Fichier CSV vide créé avec succès'
    });

    expect(component.result?.fileName).toBe('2026-07-27_12-06.csv');
  });
});
