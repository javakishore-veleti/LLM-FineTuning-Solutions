import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToastService, ToastMessage } from '../core/toast.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-toast-container',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="toast-wrapper position-fixed top-0 end-0 p-3" style="z-index:1200">
      <div *ngFor="let t of toasts" class="eg-toast mb-2" [ngClass]="[toastClass(t.level),'showing']" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-body d-flex align-items-start gap-2">
          <div class="flex-grow-1">{{ t.message }}</div>
          <button class="btn btn-sm btn-light ms-2" (click)="remove(t.id)">×</button>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
    .eg-toast { min-width: 240px; border-radius: 6px; padding: 8px; box-shadow: 0 6px 18px rgba(15,23,42,0.08); opacity: 0; transform: translateY(-8px); transition: opacity .25s ease, transform .25s ease; }
    .eg-toast.showing { opacity: 1; transform: translateY(0); }
    .bg-success { background:#198754; color:#fff }
    .bg-info { background:#0dcaf0; color:#072a3b }
    .bg-warning { background:#ffc107; color:#111 }
    .bg-danger { background:#dc3545; color:#fff }
    `
  ]
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
