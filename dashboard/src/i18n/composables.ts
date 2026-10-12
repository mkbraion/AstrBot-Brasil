import { ref, computed } from 'vue';
import { localeLoaders } from './translations';
import type { Locale } from './types';

const currentLocale = ref<Locale>('pt-BR');
const translations = ref<Record<string, any>>({});

export async function initI18n(locale: Locale = 'pt-BR') {
  currentLocale.value = locale;
  if (typeof document !== 'undefined') document.documentElement.lang = locale;
  await loadTranslations(locale);
}

async function loadTranslations(locale: Locale) {
  try {
    const loader = localeLoaders[locale] ?? localeLoaders['pt-BR'];
    translations.value = await loader();
  } catch (error) {
    console.error(`Falha ao carregar as traduções de ${locale}:`, error);
    if (locale !== 'pt-BR') {
      console.log('Usando pt-BR como idioma de fallback');
      translations.value = await localeLoaders['pt-BR']();
    }
  }
}

export function useI18n() {
  const t = (key: string, params?: Record<string, string | number>): string => {
    const keys = key.split('.');
    let value: any = translations.value;
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) value = value[k];
      else {
        console.warn(`Chave de tradução não encontrada: ${key}`);
        return `[MISSING: ${key}]`;
      }
    }
    if (typeof value !== 'string') {
      console.warn(`Valor de tradução inválido: ${key}`, value);
      return `[INVALID: ${key}]`;
    }
    let result: string = value;
    if (params) {
      result = result.replace(/\{(\w+)\}/g, (match: string, paramKey: string) => params[paramKey]?.toString() || match);
    }
    return result;
  };

  const setLocale = async (newLocale: Locale) => {
    if (newLocale !== currentLocale.value) {
      currentLocale.value = newLocale;
      if (typeof document !== 'undefined') document.documentElement.lang = newLocale;
      await loadTranslations(newLocale);
      localStorage.setItem('astrbot-locale', newLocale);
      window.dispatchEvent(new CustomEvent('astrbot-locale-changed', { detail: { locale: newLocale } }));
    }
  };

  const locale = computed(() => currentLocale.value);
  const availableLocales: Locale[] = ['pt-BR', 'zh-CN', 'en-US', 'ru-RU', 'ja-JP'];
  const isLoaded = computed(() => Object.keys(translations.value).length > 0);
  return { t, locale, setLocale, availableLocales, isLoaded };
}

export function useModuleI18n(moduleName: string) {
  const { t } = useI18n();
  const tm = (key: string, params?: Record<string, string | number>): string => {
    const normalizedModuleName = moduleName.replace(/\//g, '.');
    return t(`${normalizedModuleName}.${key}`, params);
  };
  const getRaw = (key: string): any => {
    const normalizedModuleName = moduleName.replace(/\//g, '.');
    const fullKey = `${normalizedModuleName}.${key}`;
    const keys = fullKey.split('.');
    let value: any = translations.value;
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) value = value[k];
      else return null;
    }
    return value;
  };
  return { tm, getRaw };
}

export function useLanguageSwitcher() {
  const { locale, setLocale, availableLocales } = useI18n();
  const languageOptions = computed(() => [
    { value: 'pt-BR', label: 'Português (Brasil)', flag: '🇧🇷' },
    { value: 'zh-CN', label: '简体中文', flag: '🇨🇳' },
    { value: 'en-US', label: 'English', flag: '🇺🇸' },
    { value: 'ru-RU', label: 'Русский', flag: '🇷🇺' },
    { value: 'ja-JP', label: '日本語', flag: '🇯🇵' }
  ]);
  const currentLanguage = computed(() => languageOptions.value.find(lang => lang.value === locale.value));
  const switchLanguage = async (newLocale: Locale) => await setLocale(newLocale);
  return { locale, languageOptions, currentLanguage, switchLanguage, availableLocales };
}

export function mergeDynamicTranslations(modulePath: string, allLocaleData: Record<string, any>) {
  const locale = currentLocale.value;
  const localeData = allLocaleData[locale] ?? allLocaleData['pt-BR'] ?? allLocaleData['en-US'];
  if (!localeData || typeof localeData !== 'object') return;
  const pathParts = modulePath.split('.');
  let target: any = translations.value;
  for (const part of pathParts) {
    if (!(part in target) || typeof target[part] !== 'object') target[part] = {};
    target = target[part];
  }
  deepMerge(target, localeData);
  translations.value = { ...translations.value };
}

function deepMerge(target: Record<string, any>, source: Record<string, any>) {
  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      if (!(key in target) || typeof target[key] !== 'object') target[key] = {};
      deepMerge(target[key], source[key]);
    } else target[key] = source[key];
  }
}

export async function setupI18n() {
  const savedLocale = localStorage.getItem('astrbot-locale') as Locale;
  const supported: Locale[] = ['pt-BR', 'zh-CN', 'en-US', 'ru-RU', 'ja-JP'];
  const initialLocale = savedLocale && supported.includes(savedLocale) ? savedLocale : 'pt-BR';
  await initI18n(initialLocale);
}
