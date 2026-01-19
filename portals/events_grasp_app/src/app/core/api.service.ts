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

  // Dashboard
  async getDashboardData(customerId: number = 1, limit: number = 5): Promise<DashboardDataResponse> {
    return await this.request<DashboardDataResponse>(`/api/dashboard/?customer_id=${customerId}&limit=${limit}`);
  }

  async getDashboardStats(customerId: number = 1): Promise<DashboardDataResponse> {
    return await this.request<DashboardDataResponse>(`/api/dashboard/stats?customer_id=${customerId}`);
  }

  // Scraping Logs
  async getEventsWithScrapingSummary(customerId: number = 1): Promise<ScrapingLogsResponse> {
    return await this.request<ScrapingLogsResponse>(`/api/scraping-logs/events?customer_id=${customerId}`);
  }

  async getScrapingLogsForEvent(eventId: number, limit: number = 50): Promise<ScrapingLogsResponse> {
    return await this.request<ScrapingLogsResponse>(`/api/scraping-logs/events/${eventId}/logs?limit=${limit}`);
  }

  async getScrapedFilesForEvent(eventId: number, limit: number = 100): Promise<ScrapingLogsResponse> {
    return await this.request<ScrapingLogsResponse>(`/api/scraping-logs/events/${eventId}/files?limit=${limit}`);
  }

  // Vector Stores
  async getVectorStores(eventId?: number, customerId?: number, limit: number = 100): Promise<VectorStoresResponse> {
    const params = new URLSearchParams();
    if (eventId) params.append('event_id', eventId.toString());
    if (customerId) params.append('customer_id', customerId.toString());
    params.append('limit', limit.toString());
    return await this.request<VectorStoresResponse>(`/api/vector-stores/?${params.toString()}`);
  }

  async getVectorStore(vectorStoreId: number): Promise<VectorStoresResponse> {
    return await this.request<VectorStoresResponse>(`/api/vector-stores/${vectorStoreId}`);
  }

  async createVectorStore(payload: VectorStoreCreatePayload): Promise<VectorStoresResponse> {
    return await this.request<VectorStoresResponse>('/api/vector-stores/', { method: 'POST', body: payload });
  }

  async updateVectorStore(vectorStoreId: number, payload: VectorStoreUpdatePayload): Promise<VectorStoresResponse> {
    return await this.request<VectorStoresResponse>(`/api/vector-stores/${vectorStoreId}`, { method: 'PUT', body: payload });
  }

  async deleteVectorStore(vectorStoreId: number): Promise<VectorStoresResponse> {
    return await this.request<VectorStoresResponse>(`/api/vector-stores/${vectorStoreId}`, { method: 'DELETE' });
  }

  // Vector Store Providers
  async getVectorStoreProviders(): Promise<ProvidersResponse> {
    return await this.request<ProvidersResponse>('/api/vector-stores/providers/list');
  }

  async getProviderCategories(): Promise<ProviderCategoriesResponse> {
    return await this.request<ProviderCategoriesResponse>('/api/vector-stores/providers/categories');
  }

  async getProviderSchema(providerType: string): Promise<ProviderSchemaResponse> {
    return await this.request<ProviderSchemaResponse>(`/api/vector-stores/providers/${providerType}/schema`);
  }

  async validateProviderConfig(payload: ProviderConfigPayload): Promise<ValidationResponse> {
    return await this.request<ValidationResponse>('/api/vector-stores/providers/validate', { method: 'POST', body: payload });
  }

  async testProviderConnection(providerType: string, config: any): Promise<ConnectionTestResponse> {
    return await this.request<ConnectionTestResponse>('/api/vector-stores/providers/test-connection', {
      method: 'POST',
      body: { provider_type: providerType, config }
    });
  }

  async createVectorStoreWithConfig(payload: ProviderConfigPayload): Promise<VectorStoresResponse> {
    return await this.request<VectorStoresResponse>('/api/vector-stores/providers/create', { method: 'POST', body: payload });
  }

  async createVectorStoreWithoutEvent(payload: VectorStoreCreateWithoutEventPayload): Promise<VectorStoresResponse> {
    return await this.request<VectorStoresResponse>('/api/vector-stores/providers/create-standalone', { method: 'POST', body: payload });
  }

  // Credentials API
  async getCredentialProviders(): Promise<CredentialProvidersResponse> {
    return await this.request<CredentialProvidersResponse>('/api/credentials/providers');
  }

  async getCredentialAuthTypes(providerType: string): Promise<AuthTypesResponse> {
    return await this.request<AuthTypesResponse>(`/api/credentials/providers/${providerType}/auth-types`);
  }

  async getCredentialSchema(providerType: string, authType: string): Promise<CredentialSchemaResponse> {
    return await this.request<CredentialSchemaResponse>(`/api/credentials/providers/${providerType}/schema/${authType}`);
  }

  async getCredentials(providerType?: string): Promise<CredentialsListResponse> {
    const params = providerType ? `?provider_type=${providerType}` : '';
    return await this.request<CredentialsListResponse>(`/api/credentials/${params}`);
  }

  async getCredential(credentialId: number): Promise<CredentialResponse> {
    return await this.request<CredentialResponse>(`/api/credentials/${credentialId}`);
  }

  async createCredential(payload: CredentialCreatePayload): Promise<CredentialCreateResponse> {
    return await this.request<CredentialCreateResponse>('/api/credentials/', { method: 'POST', body: payload });
  }

  async updateCredential(credentialId: number, payload: CredentialUpdatePayload): Promise<BaseResponse> {
    return await this.request<BaseResponse>(`/api/credentials/${credentialId}`, { method: 'PUT', body: payload });
  }

  async deleteCredential(credentialId: number): Promise<BaseResponse> {
    return await this.request<BaseResponse>(`/api/credentials/${credentialId}`, { method: 'DELETE' });
  }

  async getCredentialsForVectorStore(vectorStoreProvider: string): Promise<CredentialsListResponse> {
    return await this.request<CredentialsListResponse>(`/api/credentials/for-provider/${vectorStoreProvider}`);
  }
}

// Dashboard response interfaces
export interface DashboardStats {
  events: number;
  conversations: number;
  vector_stores: number;
  providers: number;
}

export interface RecentEvent {
  event_id: number;
  name: string;
  source: string;
  indexed: boolean;
}

export interface RecentConversation {
  conversation_id: number;
  title: string;
  messages: number;
  time_ago: string;
}

export interface DashboardDataResponse {
  success: boolean;
  message?: string;
  stats?: DashboardStats;
  recent_events?: RecentEvent[];
  recent_conversations?: RecentConversation[];
}

// Scraping Logs interfaces
export interface EventSummary {
  event_id: number;
  event_name: string;
  source_url: string;
  total_scrapes: number;
  total_files: number;
  last_scrape_date?: string;
}

export interface ScrapingLog {
  scraping_log_id: number;
  event_id: number;
  source_location: string;
  source_location_type: string;
  start_time?: string;
  end_time?: string;
  status: string;
  output_location?: string;
  output_location_type?: string;
  files_scraped: number;
  error_message?: string;
  created_at?: string;
  duration?: string;
}

export interface ScrapedFile {
  file_id: number;
  file_name: string;
  file_display_name?: string;
  source_file_location: string;
  source_location_type: string;
  file_size_bytes?: number;
  file_size_display?: string;
  status: string;
  uploaded_flag: boolean;
  created_at?: string;
}

export interface ScrapingLogsResponse {
  success: boolean;
  message?: string;
  events?: EventSummary[];
  scraping_logs?: ScrapingLog[];
  scraped_files?: ScrapedFile[];
}

// Vector Stores interfaces
export interface VectorStore {
  vector_store_id: number;
  event_id: number;
  event_name?: string;
  vector_store_provider: string;
  vector_store_db_name: string;
  vector_store_db_link?: string;
  status: string;
  files_count: number;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface VectorStoreCreatePayload {
  event_id: number;
  vector_store_provider: string;
  vector_store_db_name: string;
  vector_store_db_link?: string;
  vector_config_json?: string;
}

export interface VectorStoreUpdatePayload {
  vector_store_provider?: string;
  vector_store_db_name?: string;
  vector_store_db_link?: string;
  status?: string;
  is_active?: boolean;
}

export interface VectorStoresResponse {
  success: boolean;
  message?: string;
  vector_stores?: VectorStore[];
  vector_store?: VectorStore;
  total_count?: number;
}

// Vector Store Provider interfaces
export interface VectorStoreProvider {
  provider_type: string;
  name: string;
  category: string;
  status: 'available' | 'coming_soon' | 'beta';
  description: string;
  icon: string;
}

export interface ProvidersResponse {
  success: boolean;
  providers: VectorStoreProvider[];
}

export interface ProviderCategoriesResponse {
  success: boolean;
  categories: { [category: string]: VectorStoreProvider[] };
}

export interface ProviderSchemaField {
  name: string;
  label: string;
  type: 'text' | 'password' | 'number' | 'select' | 'checkbox' | 'textarea';
  required: boolean;
  placeholder?: string;
  description?: string;
  default?: any;
  min?: number;
  max?: number;
  options?: { value: string; label: string }[];
  showIf?: { [key: string]: any };
}

export interface ProviderSchema {
  provider_type: string;
  provider_name: string;
  provider_description: string;
  provider_status: string;
  provider_category: string;
  coming_soon?: boolean;
  message?: string;
  fields: ProviderSchemaField[];
}

export interface ProviderSchemaResponse {
  success: boolean;
  schema: ProviderSchema;
}

export interface ProviderConfigPayload {
  event_id: number;
  display_name: string;
  provider_type: string;
  config: { [key: string]: any };
}

export interface VectorStoreCreateWithoutEventPayload {
  display_name: string;
  provider_type: string;
  credential_id: number;
  config: { [key: string]: any };
}

export interface ValidationResponse {
  success: boolean;
  valid: boolean;
  error?: string;
}

export interface ConnectionTestResponse {
  success: boolean;
  message: string;
}

// Credential interfaces
export interface CredentialProvider {
  provider_type: string;
  name: string;
  icon: string;
  status: 'available' | 'coming_soon';
  description: string;
  auth_types: AuthType[];
}

export interface AuthType {
  value: string;
  label: string;
  description: string;
}

export interface Credential {
  credential_id: number;
  customer_id: number;
  credential_name: string;
  provider_type: string;
  provider_name: string;
  provider_icon: string;
  auth_type: string;
  description?: string;
  config?: { [key: string]: any };
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface CredentialProvidersResponse {
  success: boolean;
  providers: CredentialProvider[];
}

export interface AuthTypesResponse {
  success: boolean;
  auth_types: AuthType[];
}

export interface CredentialSchemaResponse {
  success: boolean;
  schema: {
    fields: ProviderSchemaField[];
  };
}

export interface CredentialsListResponse {
  success: boolean;
  credentials: Credential[];
  total_count: number;
}

export interface CredentialResponse {
  success: boolean;
  credential: Credential;
}

export interface CredentialCreatePayload {
  credential_name: string;
  provider_type: string;
  auth_type: string;
  config: { [key: string]: any };
  description?: string;
}

export interface CredentialUpdatePayload {
  credential_name?: string;
  config?: { [key: string]: any };
  description?: string;
  is_active?: boolean;
}

export interface CredentialCreateResponse {
  success: boolean;
  message: string;
  credential_id: number;
}

export interface BaseResponse {
  success: boolean;
  message?: string;
}

