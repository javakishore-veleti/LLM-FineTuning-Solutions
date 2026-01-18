import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-conversation-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="container py-4">
      <a class="btn btn-sm btn-link mb-3" routerLink="/conversations">← Back to Conversations</a>
      <h4>Conversation #{{ id }}</h4>
      <p class="text-muted">This is a placeholder for the conversation UI.</p>

      <div class="card mt-3">
        <div class="card-body">
          <p><strong>Sample message:</strong> Hello, can you summarize the re:Invent announcements?</p>
        </div>
      </div>
    </div>
  `
})
export class ConversationDetailComponent {
  id: string | null = null;
  constructor(route: ActivatedRoute) {
    this.id = route.snapshot.paramMap.get('id');
  }
}
