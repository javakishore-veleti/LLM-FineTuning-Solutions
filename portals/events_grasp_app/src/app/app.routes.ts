import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'signup',
    loadComponent: () => import('./features/auth/signup.component').then(m => m.SignupComponent)
  },
  {
    path: '',
    loadComponent: () => import('./features/home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard]
  },
  {
    path: 'conversations',
    children: [
      {
        path: '',
        loadComponent: () => import('./features/conversations/conversations.component').then(m => m.ConversationsComponent)
      },
      {
        path: ':id',
        loadComponent: () => import('./features/conversations/conversation-detail.component').then(m => m.ConversationDetailComponent)
      }
    ]
  },
  {
    path: 'settings',
    loadComponent: () => import('./features/settings/settings.component').then(m => m.SettingsComponent)
  },
  {
    path: 'administration',
    loadComponent: () => import('./features/administration/admin-layout.component').then(m => m.AdminLayoutComponent),
    canActivate: [authGuard],
    children: [
      {
        path: 'events',
        children: [
          {
            path: '',
            loadComponent: () => import('./features/administration/events.component').then(m => m.AdminEventsComponent)
          },
          {
            path: 'new',
            loadComponent: () => import('./features/administration/event-create.component').then(m => m.EventCreateComponent)
          },
          {
            path: ':id',
            loadComponent: () => import('./features/administration/event-detail.component').then(m => m.EventDetailComponent)
          }
        ]
      },
      {
        path: 'vector-stores',
        children: [
          {
            path: '',
            loadComponent: () => import('./features/administration/vector-stores.component').then(m => m.AdminVectorStoresComponent)
          },
          {
            path: 'new',
            loadComponent: () => import('./features/administration/vector-store-create.component').then(m => m.VectorStoreCreateComponent)
          }
        ]
      },
      {
        path: 'credentials',
        children: [
          {
            path: '',
            loadComponent: () => import('./features/administration/credentials.component').then(m => m.AdminCredentialsComponent)
          },
          {
            path: 'new',
            loadComponent: () => import('./features/administration/credential-create.component').then(m => m.CredentialCreateComponent)
          }
        ]
      },
      {
        path: 'scraping-logs',
        loadComponent: () => import('./features/administration/scraping-logs.component').then(m => m.AdminScrapingLogsComponent)
      },
      {
        path: '',
        redirectTo: 'events',
        pathMatch: 'full'
      }
    ]
  }
];
