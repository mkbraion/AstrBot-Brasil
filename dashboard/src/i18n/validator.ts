/**
 * Validador de i18n
 * Validador de internacionalização: verifica cobertura, utilização e erros nas traduções
 */

import type { ValidationResult, ValidationError, UsageReport, TranslationStats } from './types';

export class I18nValidator {
  private baseLocale: string = 'zh-CN';
  private supportedLocales: string[] = ['zh-CN', 'en-US', 'ru-RU', 'ja-JP'];

  /**
   * Verifica a completude das traduções
   */
  validateCompleteness(localeData: Record<string, any>): ValidationResult {
    const errors: ValidationError[] = [];
    const missingKeys: string[] = [];
    const extraKeys: string[] = [];

    // Obtém os dados do idioma de referência
    const baseData = localeData[this.baseLocale];
    if (!baseData) {
      errors.push({
        type: 'missing',
        key: this.baseLocale,
        message: `Dados ausentes para o idioma de referência ${this.baseLocale}`,
        severity: 'error'
      });
      return { isValid: false, missingKeys, extraKeys, errors };
    }

    // Obtém todas as chaves
    const baseKeys = this.getAllKeys(baseData);

    // Valida cada idioma
    for (const locale of this.supportedLocales) {
      if (locale === this.baseLocale) continue;

      const targetData = localeData[locale];
      if (!targetData) {
        errors.push({
          type: 'missing',
          key: locale,
          message: `Dados ausentes para o idioma ${locale}`,
          severity: 'error'
        });
        continue;
      }

      const targetKeys = this.getAllKeys(targetData);
      
      // Verifica chaves ausentes
      const missing = baseKeys.filter(key => !targetKeys.includes(key));
      missingKeys.push(...missing.map(key => `${locale}.${key}`));

      // Verifica chaves excedentes
      const extra = targetKeys.filter(key => !baseKeys.includes(key));
      extraKeys.push(...extra.map(key => `${locale}.${key}`));

      // Adiciona informações detalhadas dos erros
      missing.forEach(key => {
        errors.push({
          type: 'missing',
          key: `${locale}.${key}`,
          message: `Chave ausente em ${locale}: ${key}`,
          severity: 'error'
        });
      });

      extra.forEach(key => {
        errors.push({
          type: 'extra',
          key: `${locale}.${key}`,
          message: `Chave excedente em ${locale}: ${key}`,
          severity: 'warning'
        });
      });
    }

    return {
      isValid: errors.filter(e => e.severity === 'error').length === 0,
      missingKeys,
      extraKeys,
      errors
    };
  }

  /**
   * Valida os valores das traduções
   */
  validateValues(localeData: Record<string, any>): ValidationError[] {
    const errors: ValidationError[] = [];

    for (const [locale, data] of Object.entries(localeData)) {
      this.validateNestedValues(data, locale, '', errors);
    }

    return errors;
  }

  /**
   * Valida recursivamente os valores aninhados
   */
  private validateNestedValues(
    obj: any, 
    locale: string, 
    parentKey: string, 
    errors: ValidationError[]
  ): void {
    for (const [key, value] of Object.entries(obj)) {
      const fullKey = parentKey ? `${parentKey}.${key}` : key;

      if (typeof value === 'object' && value !== null) {
        this.validateNestedValues(value, locale, fullKey, errors);
      } else if (typeof value === 'string') {
        // Verifica valores vazios
        if (!value.trim()) {
          errors.push({
            type: 'empty_value',
            key: `${locale}.${fullKey}`,
            message: `Valor de tradução vazio: ${locale}.${fullKey}`,
            severity: 'warning'
          });
        }

        // Verifica placeholders de interpolação
        const placeholders = value.match(/\{[^}]+\}/g) || [];
        for (const placeholder of placeholders) {
          if (!/^{[a-zA-Z_][a-zA-Z0-9_]*}$/.test(placeholder)) {
            errors.push({
              type: 'type_mismatch',
              key: `${locale}.${fullKey}`,
              message: `Placeholder de interpolação inválido: ${placeholder} em ${locale}.${fullKey}`,
              severity: 'warning'
            });
          }
        }
      } else {
        errors.push({
          type: 'type_mismatch',
          key: `${locale}.${fullKey}`,
          message: `O valor da tradução deve ser uma string; tipo encontrado: ${typeof value}`,
          severity: 'error'
        });
      }
    }
  }

  /**
   * Analisa a utilização das traduções
   */
  validateUsage(translationKeys: string[], usedKeys: string[]): UsageReport {
    const unusedKeys = translationKeys.filter(key => !usedKeys.includes(key));
    const undefinedKeys = usedKeys.filter(key => !translationKeys.includes(key));

    return {
      unusedKeys,
      undefinedKeys,
      coverage: (usedKeys.length / translationKeys.length) * 100,
      totalKeys: translationKeys.length,
      usedKeys: usedKeys.length
    };
  }

  /**
   * Gera estatísticas das traduções
   */
  generateStats(localeData: Record<string, any>): TranslationStats {
    const stats: TranslationStats = {
      modules: {},
      locales: {},
      overall: {
        totalKeys: 0,
        averageCoverage: 0,
        lastSync: new Date().toISOString()
      }
    };

    // Analisa cada idioma
    for (const [locale, data] of Object.entries(localeData)) {
      const keys = this.getAllKeys(data);
      const translatedKeys = keys.filter(key => {
        const value = this.getValueByKey(data, key);
        return typeof value === 'string' && value.trim() !== '';
      });

      stats.locales[locale] = {
        totalKeys: keys.length,
        translatedKeys: translatedKeys.length,
        coverage: (translatedKeys.length / keys.length) * 100
      };

      // Analisa os módulos
      this.analyzeModules(data, locale, stats.modules);
    }

    // Calcula as estatísticas gerais
    const locales = Object.values(stats.locales);
    stats.overall.totalKeys = Math.max(...locales.map(l => l.totalKeys));
    stats.overall.averageCoverage = locales.reduce((sum, l) => sum + l.coverage, 0) / locales.length;

    return stats;
  }

  /**
   * Analisa as estatísticas por módulo
   */
  private analyzeModules(data: any, locale: string, modules: TranslationStats['modules']): void {
    for (const [moduleName, moduleData] of Object.entries(data)) {
      if (typeof moduleData === 'object' && moduleData !== null) {
        const moduleKey = `${locale}.${moduleName}`;
        const keys = this.getAllKeys(moduleData);
        const translatedKeys = keys.filter(key => {
          const value = this.getValueByKey(moduleData, key);
          return typeof value === 'string' && value.trim() !== '';
        });

        if (!modules[moduleKey]) {
          modules[moduleKey] = {
            keys: 0,
            coverage: 0,
            lastUpdated: new Date().toISOString()
          };
        }

        modules[moduleKey].keys = keys.length;
        modules[moduleKey].coverage = (translatedKeys.length / keys.length) * 100;
      }
    }
  }

  /**
   * Obtém todos os caminhos de chaves de um objeto
   */
  private getAllKeys(obj: any, prefix: string = ''): string[] {
    const keys: string[] = [];

    for (const [key, value] of Object.entries(obj)) {
      const fullKey = prefix ? `${prefix}.${key}` : key;

      if (typeof value === 'object' && value !== null) {
        keys.push(...this.getAllKeys(value, fullKey));
      } else {
        keys.push(fullKey);
      }
    }

    return keys;
  }

  /**
   * Obtém um valor pelo caminho da chave
   */
  private getValueByKey(obj: any, keyPath: string): any {
    return keyPath.split('.').reduce((current, key) => {
      return current && current[key];
    }, obj);
  }

  /**
   * Verifica a consistência dos placeholders de interpolação
   */
  validateInterpolation(localeData: Record<string, any>): ValidationError[] {
    const errors: ValidationError[] = [];
    const baseData = localeData[this.baseLocale];
    
    if (!baseData) return errors;

    const baseKeys = this.getAllKeys(baseData);

    for (const key of baseKeys) {
      const baseValue = this.getValueByKey(baseData, key);
      if (typeof baseValue !== 'string') continue;

      const basePlaceholders = (baseValue.match(/\{[^}]+\}/g) || []).sort();

      for (const locale of this.supportedLocales) {
        if (locale === this.baseLocale) continue;

        const targetData = localeData[locale];
        if (!targetData) continue;

        const targetValue = this.getValueByKey(targetData, key);
        if (typeof targetValue !== 'string') continue;

        const targetPlaceholders = (targetValue.match(/\{[^}]+\}/g) || []).sort();

        if (JSON.stringify(basePlaceholders) !== JSON.stringify(targetPlaceholders)) {
          errors.push({
            type: 'type_mismatch',
            key: `${locale}.${key}`,
            message: `Placeholders de interpolação diferentes em ${locale}.${key}; esperado: ${basePlaceholders.join(', ')}; encontrado: ${targetPlaceholders.join(', ')}`,
            severity: 'error'
          });
        }
      }
    }

    return errors;
  }

  /**
   * Valida a convenção de nomes das chaves
   */
  validateKeyNaming(localeData: Record<string, any>): ValidationError[] {
    const errors: ValidationError[] = [];
    const keyNamingPattern = /^[a-z][a-zA-Z0-9]*$/;

    for (const [locale, data] of Object.entries(localeData)) {
      this.validateKeyNamingRecursive(data, locale, '', keyNamingPattern, errors);
    }

    return errors;
  }

  /**
   * Valida recursivamente os nomes das chaves
   */
  private validateKeyNamingRecursive(
    obj: any,
    locale: string,
    parentKey: string,
    pattern: RegExp,
    errors: ValidationError[]
  ): void {
    for (const key of Object.keys(obj)) {
      const fullKey = parentKey ? `${parentKey}.${key}` : key;

      if (!pattern.test(key)) {
        errors.push({
          type: 'type_mismatch',
          key: `${locale}.${fullKey}`,
          message: `A chave ${key} não segue a convenção de nomes; use camelCase`,
          severity: 'warning'
        });
      }

      if (typeof obj[key] === 'object' && obj[key] !== null) {
        this.validateKeyNamingRecursive(obj[key], locale, fullKey, pattern, errors);
      }
    }
  }

  /**
   * Valida vários pacotes de idiomas
   */
  async validateLocales(locales: string[]): Promise<{
    summary: {
      totalLocales: number;
      totalKeys: number;
      missingKeys: number;
      emptyValues: number;
      invalidInterpolations: number;
      completeness: number;
    };
    details: ValidationResult[];
    recommendations: string[];
  }> {
    const results: ValidationResult[] = [];
    
    for (const locale of locales) {
      try {
        // O ideal é carregar os arquivos reais de tradução; por enquanto, cria uma estrutura básica
        const localeData = { [locale]: {} };
        const result = this.validateCompleteness(localeData);
        results.push(result);
             } catch (error) {
         console.error(`Erro ao validar o pacote de idioma ${locale}:`, error);
         // Cria o resultado de erro
         const errorResult: ValidationResult = {
           isValid: false,
           missingKeys: [],
           extraKeys: [],
           errors: [
             {
               type: 'missing',
               key: locale,
               message: error instanceof Error ? error.message : 'Erro desconhecido',
               severity: 'error'
             }
           ]
         };
         results.push(errorResult);
       }
    }
    
        // Gera o relatório resumido
    const totalKeys = results.length * 100; // Total estimado de chaves
    const missingKeys = results.reduce((sum, r) => sum + r.missingKeys.length, 0);
    
    return {
      summary: {
        totalLocales: results.length,
        totalKeys,
        missingKeys,
        emptyValues: 0, // Definido temporariamente como zero
        invalidInterpolations: 0, // Definido temporariamente como zero
        completeness: totalKeys > 0 ? ((totalKeys - missingKeys) / totalKeys) * 100 : 100
      },
      details: results,
      recommendations: [
        'Priorize a tradução das chaves ausentes nos módulos principais',
        'Verifique todos os valores vazios e forneça traduções adequadas',
        'Mantenha os placeholders de interpolação consistentes entre os idiomas'
      ]
    };
  }

  /**
   * Gera o relatório de validação
   */
  generateReport(localeData: Record<string, any>, usedKeys: string[] = []): {
    completeness: ValidationResult;
    values: ValidationError[];
    interpolation: ValidationError[];
    naming: ValidationError[];
    usage: UsageReport | null;
    stats: TranslationStats;
  } {
    const completeness = this.validateCompleteness(localeData);
    const values = this.validateValues(localeData);
    const interpolation = this.validateInterpolation(localeData);
    const naming = this.validateKeyNaming(localeData);
    const stats = this.generateStats(localeData);

    let usage: UsageReport | null = null;
    if (usedKeys.length > 0) {
      const allKeys = this.getAllKeys(localeData[this.baseLocale] || {});
      usage = this.validateUsage(allKeys, usedKeys);
    }

    return {
      completeness,
      values,
      interpolation,
      naming,
      usage,
      stats
    };
  }
} 