import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class ApiService {
  // Base URL for backend API; empty = same origin
  private baseUrl = '';

  constructor(private auth: AuthService) {}

  private async request(path: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${path}`;

    const headers: Record<string, string> = {};
    // copy existing headers passed in
    if (options.headers) {
      const h = options.headers as Record<string, string>;
      Object.assign(headers, h);
    }

    // Attach Authorization header from AuthService if token exists
    const token = this.auth?.getToken?.();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const res = await fetch(url, { ...options, headers, credentials: 'same-origin' });
    const text = await res.text();
    let json: any = null;
    try {
      json = text ? JSON.parse(text) : null;
    } catch (e) {
      // not JSON
    }
    if (!res.ok) {
      const err = new Error(json?.error || res.statusText || 'Request failed');
      (err as any).status = res.status;
      (err as any).body = json || text;
      throw err;
    }
    return json || text;
  }

  async getEvents() {
    return await this.request('/api/events/');
  }

  async getEvent(id: number) {
    return await this.request(`/api/events/${id}`);
  }

  async postScrape(opts: { refresh?: boolean; maxDepth?: number } = {}) {
    const body = JSON.stringify(opts);
    return await this.request('/api/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body
    });
  }

  async postVectorCreate(opts: { storeName?: string } = {}) {
    const body = JSON.stringify(opts);
    return await this.request('/api/vectordb/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body
    });
  }

  async postEvent(payload: any) {
    const body = JSON.stringify(payload);
    return await this.request('/api/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body
    });
  }

  // Providers
  async getProviders() {
    return await this.request('/api/providers/');
  }

  async createProvider(payload: any) {
    return await this.request('/api/providers/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }

  async deleteProvider(id: number) {
    return await this.request(`/api/providers/${id}`, { method: 'DELETE' });
  }

  // Event providers
  async listEventProviders(eventId: number) {
    return await this.request(`/api/events/${eventId}/providers`);
  }

  async addProviderToEvent(eventId: number, payload: any) {
    return await this.request(`/api/events/${eventId}/providers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }

  async removeEventProvider(eventId: number, epId: number) {
    return await this.request(`/api/events/${eventId}/providers/${epId}`, { method: 'DELETE' });
  }

  async publishEvent(eventId: number) {
    return await this.request(`/api/events/${eventId}/publish`, { method: 'POST' });
  }
}
