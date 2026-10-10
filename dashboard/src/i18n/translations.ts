// Carregadores de tradução por idioma.
// Cada locale é carregado sob demanda para reduzir o bundle inicial.

import type zhCN from './locales/zh-CN';

export type Translations = typeof zhCN;

export const localeLoaders = {
  'pt-BR': () => import('./locales/pt-BR').then((m) => m.default),
  'zh-CN': () => import('./locales/zh-CN').then((m) => m.default),
  'en-US': () => import('./locales/en-US').then((m) => m.default),
  'ru-RU': () => import('./locales/ru-RU').then((m) => m.default),
  'ja-JP': () => import('./locales/ja-JP').then((m) => m.default)
} as const;

export type Locale = keyof typeof localeLoaders;
