import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  // Base URL for backend API; empty = same origin
  private baseUrl = '';

  constructor(private http: HttpClient) {}

  // make request public and default generic to any
  public async request<T = any>(path: string, options: { method?: string; body?: any; headers?: HttpHeaders } = {}): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const method = (options.method || 'GET').toUpperCase();
    const headers = options.headers || undefined;

    if (method === 'GET') {
      return await firstValueFrom(this.http.get<T>(url, { headers }));
    }
    if (method === 'POST') {
      return await firstValueFrom(this.http.post<T>(url, options.body, { headers }));
    }
    if (method === 'PUT') {
      return await firstValueFrom(this.http.put<T>(url, options.body, { headers }));
    }
    if (method === 'DELETE') {
      return await firstValueFrom(this.http.delete<T>(url, { headers }));
    }

    // fallback
    return await firstValueFrom(this.http.request<T>(method, url, { body: options.body, headers }));
  }

  async getEvents() {
    return await this.request<any>('/api/events/');
  }

  async getEvent(id: number) {
    return await this.request<any>(`/api/events/${id}`);
  }

  async postScrape(opts: { refresh?: boolean; maxDepth?: number } = {}) {
    return await this.request<any>('/api/scrape', { method: 'POST', body: opts });
  }

  async postVectorCreate(opts: { storeName?: string } = {}) {
    return await this.request<any>('/api/vectordb/create', { method: 'POST', body: opts });
  }

  async postEvent(payload: any) {
    return await this.request<any>('/api/events', { method: 'POST', body: payload });
  }

  // Providers
  async getProviders() {
    return await this.request<any>('/api/providers/');
  }

  async createProvider(payload: any) {
    return await this.request<any>('/api/providers/', { method: 'POST', body: payload });
  }

  async deleteProvider(id: number) {
    return await this.request<any>(`/api/providers/${id}`, { method: 'DELETE' });
  }

  // Event providers
  async listEventProviders(eventId: number) {
    return await this.request<any>(`/api/events/${eventId}/providers`);
  }

  async addProviderToEvent(eventId: number, payload: any) {
    return await this.request<any>(`/api/events/${eventId}/providers`, { method: 'POST', body: payload });
  }

  async removeEventProvider(eventId: number, epId: number) {
    return await this.request<any>(`/api/events/${eventId}/providers/${epId}`, { method: 'DELETE' });
  }

  async publishEvent(eventId: number) {
    return await this.request<any>(`/api/events/${eventId}/publish`, { method: 'POST' });
  }
}
