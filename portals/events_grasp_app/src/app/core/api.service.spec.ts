import { TestBed } from '@angular/core/testing';
import { ApiService } from './api.service';
import { AuthService } from './auth.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptor } from './auth.interceptor';

class FakeAuth {
  token: string | null = null;
  getToken() { return this.token; }
}

describe('ApiService', () => {
  let service: ApiService;
  let auth: FakeAuth;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    auth = new FakeAuth();
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ApiService, { provide: AuthService, useValue: auth }, { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }]
    });
    service = TestBed.inject(ApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should attach Authorization header when token available', async () => {
    auth.token = 't-123';
    service.getEvents();
    const req = httpMock.expectOne('/api/events/');
    expect(req.request.headers.get('Authorization')).toBe('Bearer t-123');
    req.flush([]);
  });
});
