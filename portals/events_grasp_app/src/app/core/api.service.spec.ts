import { TestBed } from '@angular/core/testing';
import { ApiService } from './api.service';
import { AuthService } from './auth.service';

class FakeAuth {
  token: string | null = null;
  getToken() { return this.token; }
}

describe('ApiService', () => {
  let service: ApiService;
  let auth: FakeAuth;

  beforeEach(() => {
    auth = new FakeAuth();
    TestBed.configureTestingModule({ providers: [ApiService, { provide: AuthService, useValue: auth }] });
    service = TestBed.inject(ApiService);
  });

  it('should attach Authorization header when token available', async () => {
    // spy on global fetch
    const origFetch = (window as any).fetch;
    auth.token = 't-123';
    (window as any).fetch = async (url: string, opts: any) => {
      expect(opts.headers['Authorization']).toBe('Bearer t-123');
      return new Response('{}', { status: 200 });
    };
    await service.getEvents();
    (window as any).fetch = origFetch;
  });
});
