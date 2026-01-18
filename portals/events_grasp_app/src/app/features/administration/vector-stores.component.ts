import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-admin-vector-stores',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div>
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4>Vector Stores</h4>
        <button class="btn btn-sm btn-primary">+ Add Store</button>
      </div>

      <table class="table table-sm">
        <thead>
          <tr>
            <th>Name</th>
            <th>Provider</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>LLM-FineTuning-Solutions</td>
            <td>OpenAI</td>
            <td><span class="badge bg-success">Active</span></td>
            <td><button class="btn btn-sm btn-outline-secondary">Manage</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  `
})
export class AdminVectorStoresComponent {}
