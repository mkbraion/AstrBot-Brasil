/**
 * Definições de tipos TypeScript para i18n — geradas automaticamente a partir de JSON
 * Tipos de internacionalização inferidos dos arquivos JSON, com segurança de tipos e sincronização automática
 */

// Infere a estrutura completa a partir dos dados reais de tradução
import type { Locale, Translations } from './translations';

export type TranslationSchema = Translations;

// Auxiliar TypeScript: extrai recursivamente caminhos de chaves aninhadas
type NestedKeyOf<T> = T extends object 
  ? {
      [K in keyof T & string]: T[K] extends object
        ? `${K}` | `${K}.${NestedKeyOf<T[K]>}`
        : `${K}`
    }[keyof T & string]
  : never;

// União de chaves de tradução inferida automaticamente, incluindo caminhos válidos separados por pontos
export type TranslationKey = NestedKeyOf<TranslationSchema>;

// Tipo de localidade inferido dos carregadores de idiomas disponíveis
export type { Locale } from './translations';

// Tipo da função de tradução
export type TranslationFunction = {
  (key: TranslationKey): string;
  (key: TranslationKey, params: Record<string, string | number>): string;
};

// Tipos auxiliares mantidos, independentes da estrutura específica das traduções

// Estado de carregamento do módulo
export interface ModuleLoadingState {
  core: boolean;
  features: boolean;
  messages: boolean;
}

// Configuração de tradução
export interface I18nConfig {
  locale: Locale;
  fallbackLocale: Locale;
  lazy: boolean;
  preload: string[];
  caching: boolean;
  devMode: boolean;
}

// Resultado da validação
export interface ValidationResult {
  isValid: boolean;
  missingKeys: string[];
  extraKeys: string[];
  errors: ValidationError[];
}

export interface ValidationError {
  type: 'missing' | 'extra' | 'type_mismatch' | 'empty_value';
  key: string;
  message: string;
  severity: 'error' | 'warning';
}

// Relatório de utilização
export interface UsageReport {
  unusedKeys: string[];
  undefinedKeys: string[];
  coverage: number;
  totalKeys: number;
  usedKeys: number;
}

// Estatísticas de tradução
export interface TranslationStats {
  modules: {
    [moduleName: string]: {
      keys: number;
      coverage: number;
      lastUpdated: string;
    };
  };
  locales: {
    [locale: string]: {
      totalKeys: number;
      translatedKeys: number;
      coverage: number;
    };
  };
  overall: {
    totalKeys: number;
    averageCoverage: number;
    lastSync: string;
  };
}

// Tipos das ferramentas de desenvolvimento
export interface DevToolsData {
  currentLocale: Locale;
  loadedModules: string[];
  cacheStats: {
    size: number;
    hits: number;
    misses: number;
  };
  performance: {
    loadTime: number;
    renderTime: number;
  };
}

// Extensão do módulo Vue I18n comentada temporariamente para evitar problemas de resolução durante a compilação
// Essas definições continuam válidas em execução, sem provocar erros de compilação
/*
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $t: (key: TranslationKey, params?: Record<string, string | number>) => string;
  }
}

declare module 'vue-i18n' {
  export interface DefineLocaleMessage extends TranslationSchema {}
}
*/ 
