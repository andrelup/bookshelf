# BookShelf Frontend — Bulletproof React Architecture

SPA para tienda de libros. Este CLAUDE.md complementa el CLAUDE.md raíz del monorepo.

## Stack

- React 18
- TypeScript (strict mode)
- Vite (build + dev server)
- TailwindCSS (estilos)
- React Router v6 (routing)
- Vitest + React Testing Library (testing)
- Playwright (E2E)
- ESLint + Prettier (linting + formatting)

## Arquitectura Bulletproof React

```
frontend/
├── src/
│   ├── app/                       # Entrypoint, providers globales, router
│   │   ├── App.tsx                # Componente raíz
│   │   ├── providers.tsx          # AuthProvider, QueryProvider, etc.
│   │   └── router.tsx             # Definición de rutas con React Router v6
│   │
│   ├── features/                  # MÓDULOS DE DOMINIO — cada feature es autónomo
│   │   ├── auth/
│   │   │   ├── api/               # Llamadas al backend (login, register, logout)
│   │   │   │   └── auth-api.ts
│   │   │   ├── components/        # Componentes exclusivos de auth
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── RegisterForm.tsx
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   ├── hooks/             # Hooks de auth
│   │   │   │   ├── useAuth.ts
│   │   │   │   └── useLogin.ts
│   │   │   ├── types/             # Tipos TypeScript de auth
│   │   │   │   └── index.ts
│   │   │   └── index.ts           # Public API del feature (re-exports)
│   │   │
│   │   ├── books/
│   │   │   ├── api/
│   │   │   │   └── books-api.ts
│   │   │   ├── components/
│   │   │   │   ├── BookCard.tsx
│   │   │   │   ├── BookList.tsx
│   │   │   │   ├── BookDetail.tsx
│   │   │   │   └── BookSearch.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useBooks.ts
│   │   │   │   └── useBookSearch.ts
│   │   │   ├── types/
│   │   │   │   └── index.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── wishlist/
│   │   │   ├── api/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── types/
│   │   │   └── index.ts
│   │   │
│   │   └── seller/
│   │       ├── api/
│   │       ├── components/
│   │       │   ├── SellerDashboard.tsx
│   │       │   ├── BookForm.tsx
│   │       │   └── SellerBookList.tsx
│   │       ├── hooks/
│   │       ├── types/
│   │       └── index.ts
│   │
│   ├── components/                # Componentes COMPARTIDOS (UI genérica reutilizable)
│   │   ├── ui/                    # Primitivos: Button, Input, Modal, Card, Spinner
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Card.tsx
│   │   │   └── Spinner.tsx
│   │   └── layout/                # Layout: Header, Footer, Sidebar, PageContainer
│   │       ├── Header.tsx
│   │       ├── Footer.tsx
│   │       └── PageContainer.tsx
│   │
│   ├── hooks/                     # Hooks COMPARTIDOS (genéricos, no de un feature)
│   │   ├── useApi.ts              # Wrapper de fetch con auth header y error handling
│   │   ├── useDebounce.ts
│   │   └── useLocalStorage.ts
│   │
│   ├── lib/                       # Configuración de librerías externas
│   │   └── api-client.ts          # Instancia base de fetch/axios con baseURL y interceptors
│   │
│   ├── types/                     # Tipos globales compartidos
│   │   └── api.ts                 # ApiResponse<T>, PaginatedResponse<T>, etc.
│   │
│   └── utils/                     # Funciones helper puras (sin side effects)
│       ├── format-price.ts
│       └── validate-isbn.ts
│
├── e2e/                           # Tests E2E con Playwright
│   ├── tests/
│   │   ├── auth.spec.ts
│   │   ├── books.spec.ts
│   │   └── wishlist.spec.ts
│   └── page-objects/              # Page Object Model
│       ├── LoginPage.ts
│       └── CatalogPage.ts
│
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.ts
├── eslint.config.js
├── prettier.config.js
├── playwright.config.ts
└── Dockerfile
```

## Reglas de Arquitectura Bulletproof React

1. **Cada feature es un módulo autónomo.** Tiene su propia carpeta con api/, components/, hooks/, types/ y un `index.ts` que actúa como public API.

2. **Un feature NO importa directamente de otro feature.** Si `wishlist` necesita el tipo `Book`, ese tipo debe estar en `types/` global o el feature `books` debe exportarlo en su `index.ts` y `wishlist` importa desde `@/features/books`.

3. **El `index.ts` de cada feature es su contrato público.** Solo lo que se exporta ahí es accesible desde fuera:
   ```typescript
   // features/auth/index.ts
   export { LoginForm } from './components/LoginForm';
   export { RegisterForm } from './components/RegisterForm';
   export { ProtectedRoute } from './components/ProtectedRoute';
   export { useAuth } from './hooks/useAuth';
   export type { User, LoginCredentials } from './types';
   ```

4. **Los componentes de `components/` raíz son UI genérica** sin lógica de negocio: Button, Input, Modal, Card, Spinner. No importan de ningún feature.

5. **Los hooks de `hooks/` raíz son genéricos** y reutilizables en cualquier feature: useApi, useDebounce, useLocalStorage. No contienen lógica de negocio.

6. **`app/` solo contiene wiring:** providers, router, y el componente raíz. No contiene componentes de UI ni lógica de negocio.

## Convenciones de código

- Functional components con hooks. No class components.
- PascalCase para componentes: `BookCard.tsx`, `LoginForm.tsx`
- camelCase para hooks: `useAuth.ts`, `useBooks.ts`
- kebab-case para archivos de utilidades y API: `books-api.ts`, `format-price.ts`
- TypeScript strict mode obligatorio. No usar `any` — usar `unknown` y narrowing.
- Named exports siempre. No default exports (excepto páginas para lazy loading).
- Props definidas con `interface`, no `type`:
  ```typescript
  interface BookCardProps {
    book: Book;
    onAddToWishlist: (bookId: number) => void;
  }

  export const BookCard = ({ book, onAddToWishlist }: BookCardProps) => {
    // ...
  };
  ```

## Estado

- **React Context** para auth (usuario logueado, token). Provider en `app/providers.tsx`.
- **Estado local** (`useState`, `useReducer`) para todo lo demás. No meter Redux ni Zustand.
- **Datos del servidor** gestionados con el hook `useApi` (fetch + estado de loading/error/data).
- Si un estado es necesario en más de un feature → elevarlo a Context o moverlo a un hook compartido.

## Estilos

- TailwindCSS para todos los estilos. No CSS modules, no styled-components, no CSS en línea.
- Clases de Tailwind directamente en el JSX.
- Para variantes de componentes, usar lógica condicional con template literals:
  ```typescript
  const buttonClass = `px-4 py-2 rounded ${variant === 'primary' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'}`;
  ```
- No crear archivos `.css` salvo `index.css` con las directivas de Tailwind.

## API Client

- Un único `api-client.ts` en `lib/` con la configuración base:
  ```typescript
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  ```
- Todas las llamadas al backend pasan por este client.
- El token JWT se inyecta automáticamente desde el AuthContext.
- Respuestas tipadas con generics: `ApiResponse<Book>`, `ApiResponse<Book[]>`.

## Testing

- **Unit tests:** Vitest + React Testing Library
- **E2E tests:** Playwright con Page Object Model
- Colocación: tests unitarios junto al componente (`BookCard.test.tsx` junto a `BookCard.tsx`)
- Testear comportamiento, no implementación. Usar `getByRole`, `getByText`, no `getByTestId`.
- Ejecutar: `npx vitest run --coverage`

## Routing

- React Router v6 con rutas definidas en `app/router.tsx`
- Lazy loading para páginas principales:
  ```typescript
  const BookDetail = lazy(() => import('@/features/books/components/BookDetail'));
  ```
- Rutas protegidas con `ProtectedRoute` component de `features/auth`
- Rutas de seller separadas con su propio layout

## Path Aliases

- `@/` apunta a `src/`:
  ```typescript
  import { BookCard } from '@/features/books';
  import { Button } from '@/components/ui/Button';
  import { useApi } from '@/hooks/useApi';
  ```
- Configurado en `tsconfig.json` y `vite.config.ts`

## Qué NO hacer

- No importar componentes internos de un feature desde fuera — solo lo que exporta `index.ts`
- No poner lógica de negocio en `components/` raíz — esos son UI puros
- No usar `any` — usar `unknown` con type guards
- No crear archivos CSS individuales — usar Tailwind
- No usar `useEffect` para fetch de datos — usar el hook `useApi` que ya maneja loading/error
- No meter estado global (Context) para datos que solo usa un feature
- No hacer fetch directo con `window.fetch` — siempre a través de `lib/api-client.ts`