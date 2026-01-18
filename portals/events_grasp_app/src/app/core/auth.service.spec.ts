import { TestBed } from '@angular/core/testing';
import { AuthService } from './auth.service';
import { ApiService } from './api.service';

describe('AuthService', () => {
  let service: AuthService;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [AuthService, ApiService] });
    service = TestBed.inject(AuthService);
    localStorage.clear();
  });

  it('should store and retrieve token', () => {
    service.setToken('abc123');
    expect(service.getToken()).toBe('abc123');
    expect(service.isAuthenticated()).toBeTrue();
    service.clearToken();
    expect(service.getToken()).toBeNull();
    expect(service.isAuthenticated()).toBeFalse();
  });

  it('login should set token for non-empty credentials', async () => {
    const ok = await service.login('u', 'p');
    expect(ok).toBeTrue();
    expect(service.getToken()).toBeTruthy();
  });
});
