import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';

export type ToastLevel = 'success' | 'info' | 'warn' | 'error';
export interface ToastMessage {
  id: string;
  level: ToastLevel;
  message: string;
  timeout?: number; // ms
}

@Injectable({ providedIn: 'root' })
export class ToastService {
  private subject = new Subject<ToastMessage>();
  public messages$: Observable<ToastMessage> = this.subject.asObservable();

  private makeMessage(level: ToastLevel, message: string, timeout = 5000): ToastMessage {
    return { id: `${Date.now()}-${Math.random().toString(36).slice(2,8)}`, level, message, timeout };
  }

  success(message: string, timeout = 4500) {
    this.subject.next(this.makeMessage('success', message, timeout));
  }
  info(message: string, timeout = 4000) {
    this.subject.next(this.makeMessage('info', message, timeout));
  }
  warn(message: string, timeout = 6000) {
    this.subject.next(this.makeMessage('warn', message, timeout));
  }
  error(message: string, timeout = 8000) {
    this.subject.next(this.makeMessage('error', message, timeout));
  }
}
