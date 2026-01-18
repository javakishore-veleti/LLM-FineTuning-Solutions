import { TestBed } from '@angular/core/testing';
import { ToastService } from './toast.service';

describe('ToastService', () => {
  let service: ToastService;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [ToastService] });
    service = TestBed.inject(ToastService);
  });

  it('should emit toast messages', (done) => {
    service.messages$.subscribe((m) => {
      expect(m.message).toBe('hello');
      expect(m.level).toBe('info');
      done();
    });
    service.info('hello');
  });
});
