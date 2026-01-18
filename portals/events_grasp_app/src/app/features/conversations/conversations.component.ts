import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-conversations',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4>Conversations</h4>
        <a class="btn btn-sm btn-primary" routerLink="/conversations/new">+ New Conversation</a>
      </div>

      <div class="list-group">
        <a class="list-group-item list-group-item-action" [routerLink]="['/conversations', 1]">AWS re:Invent 2025 - Q&A</a>
        <a class="list-group-item list-group-item-action" [routerLink]="['/conversations', 2]">Product Launch Discussion</a>
        <a class="list-group-item list-group-item-action" [routerLink]="['/conversations', 3]">Research Notes</a>
      </div>

    </div>
  `
})
export class ConversationsComponent {}
