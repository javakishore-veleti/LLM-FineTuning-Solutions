import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToastService, ToastMessage } from '../core/toast.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-toast-container',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 1200">
      <div *ngFor="let t of toasts" class="toast show mb-2" [ngClass]="toastClass(t.level)" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-body">{{ t.message }}</div>
      </div>
    </div>
  `
})
export class ToastComponent implements OnInit, OnDestroy {
  toasts: ToastMessage[] = [];
  sub!: Subscription;

  constructor(private toastService: ToastService) {}

  ngOnInit() {
    this.sub = this.toastService.messages$.subscribe((m) => {
      this.toasts = [m, ...this.toasts].slice(0, 5);
      if (m.timeout && m.timeout > 0) {
        setTimeout(() => this.remove(m.id), m.timeout);
      }
    });
  }

  ngOnDestroy() {
    this.sub?.unsubscribe();
  }

  remove(id: string) {
    this.toasts = this.toasts.filter(t => t.id !== id);
  }

  toastClass(level: string) {
    if (level === 'success') return 'bg-success text-white';
    if (level === 'info') return 'bg-info text-white';
    if (level === 'warn') return 'bg-warning text-dark';
    if (level === 'error') return 'bg-danger text-white';
    return '';
  }
}
