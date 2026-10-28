/**
 * Carregador dinâmico de i18n
 * Carregador de internacionalização com carregamento sob demanda e cache
 */

export interface LoaderCache {
  [key: string]: any;
}

export interface ModuleInfo {
  name: string;
  path: string;
  loaded: boolean;
  data?: any;
}

export class I18nLoader {
  private cache: Map<string, any> = new Map();
  private moduleRegistry: Map<string, ModuleInfo> = new Map();
  
  constructor() {
    this.registerModules();
  }

  /**
   * Registra todos os módulos de tradução disponíveis
   */
  private registerModules(): void {
    const modules = [
      // Módulos principais
      { name: 'core/common', path: 'core/common.json' },
      { name: 'core/actions', path: 'core/actions.json' },
      { name: 'core/status', path: 'core/status.json' },
      { name: 'core/navigation', path: 'core/navigation.json' },
      { name: 'core/header', path: 'core/header.json' },
      { name: 'core/shared', path: 'core/shared.json' },
      
      // Módulos de funcionalidades
      { name: 'features/chat', path: 'features/chat.json' },
      { name: 'features/extension', path: 'features/extension.json' },
      { name: 'features/conversation', path: 'features/conversation.json' },
      { name: 'features/session-management', path: 'features/session-management.json' },
      { name: 'features/tooluse', path: 'features/tool-use.json' },
      { name: 'features/provider', path: 'features/provider.json' },
      { name: 'features/platform', path: 'features/platform.json' },
      { name: 'features/config', path: 'features/config.json' },
      { name: 'features/config-metadata', path: 'features/config-metadata.json' },
      { name: 'features/console', path: 'features/console.json' },
      { name: 'features/trace', path: 'features/trace.json' },
      { name: 'features/about', path: 'features/about.json' },
      { name: 'features/settings', path: 'features/settings.json' },
      { name: 'features/auth', path: 'features/auth.json' },
      { name: 'features/chart', path: 'features/chart.json' },
      { name: 'features/dashboard', path: 'features/dashboard.json' },
      { name: 'features/cron', path: 'features/cron.json' },
      { name: 'features/subagent', path: 'features/subagent.json' },
      { name: 'features/alkaid/index', path: 'features/alkaid/index.json' },
      { name: 'features/alkaid/knowledge-base', path: 'features/alkaid/knowledge-base.json' },
      { name: 'features/alkaid/memory', path: 'features/alkaid/memory.json' },
      { name: 'features/persona', path: 'features/persona.json' },
      { name: 'features/welcome', path: 'features/welcome.json' },
      
      // Módulos de mensagens
      { name: 'messages/errors', path: 'messages/errors.json' },
      { name: 'messages/success', path: 'messages/success.json' },
      { name: 'messages/validation', path: 'messages/validation.json' }
    ];

    modules.forEach(module => {
      this.moduleRegistry.set(module.name, {
        name: module.name,
        path: module.path,
        loaded: false
      });
    });
  }

  /**
   * Carrega um módulo individual
   */
  async loadModule(locale: string, moduleName: string): Promise<any> {
    const cacheKey = `${locale}:${moduleName}`;
    
    // Verifica o cache
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    const moduleInfo = this.moduleRegistry.get(moduleName);
    if (!moduleInfo) {
      console.warn(`Módulo ${moduleName} não registrado`);
      return {};
    }

    try {
      // Usa importação dinâmica para carregar JSON em produção e no desenvolvimento
      const modulePath = `../locales/${locale}/${moduleInfo.path}`;
      const module = await import(/* @vite-ignore */ modulePath);
      const data = module.default || module;

      // Armazena o resultado em cache
      this.cache.set(cacheKey, data);
      
      // Atualiza as informações do módulo
      moduleInfo.loaded = true;
      moduleInfo.data = data;

      return data;
    } catch (error) {
      console.error(`Falha ao carregar o módulo ${moduleName}:`, error);
      
      // Alternativa: tenta carregar com fetch (ambiente de desenvolvimento)
      try {
        const modulePath = `/src/i18n/locales/${locale}/${moduleInfo.path}`;
        const response = await fetch(modulePath);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();

        // Armazena o resultado em cache
        this.cache.set(cacheKey, data);
        
        // Atualiza as informações do módulo
        moduleInfo.loaded = true;
        moduleInfo.data = data;

        return data;
      } catch (fetchError) {
        console.error(`A tentativa alternativa com fetch também falhou:`, fetchError);
        return {};
      }
    }
  }

  /**
   * Carregador genérico de módulos: reduz duplicação e facilita a manutenção
   */
  private async loadModules(
    locale: string,
    prefix: string,
    overrideList: string[] = []
  ): Promise<any> {
    // Usa a lista informada ou filtra os módulos registrados pelo prefixo
    const moduleNames = overrideList.length > 0
      ? overrideList
      : Array.from(this.moduleRegistry.keys()).filter(key => key.startsWith(prefix));

    const results = await Promise.all(
      moduleNames.map(module => this.loadModule(locale, module))
    );

    return this.mergeModules(results, moduleNames);
  }

  /**
   * Carrega os módulos principais (prioridade máxima)
   */
  async loadCoreModules(locale: string): Promise<any> {
    return this.loadModules(locale, 'core');
  }

  /**
   * Carrega os módulos de funcionalidades
   */
  async loadFeatureModules(locale: string, features?: string[]): Promise<any> {
    return this.loadModules(locale, 'features', features || []);
  }

  /**
   * Carrega os módulos de mensagens
   */
  async loadMessageModules(locale: string): Promise<any> {
    return this.loadModules(locale, 'messages');
  }

  /**
   * Carrega todos os módulos
   */
  async loadAllModules(locale: string): Promise<any> {
    const [core, features, messages] = await Promise.all([
      this.loadCoreModules(locale),
      this.loadFeatureModules(locale),
      this.loadMessageModules(locale)
    ]);

    return {
      ...core,
      ...features,
      ...messages
    };
  }

  /**
   * Carrega o pacote de idioma completo (todos os módulos combinados)
   */
  async loadLocale(locale: string): Promise<any> {
    return this.loadAllModules(locale);
  }

  /**
   * Combina os dados de vários módulos
   */
  private mergeModules(modules: any[], moduleNames: string[]): any {
    const result: any = {};
    const pathRegistry = new Map<string, string>();
    
    modules.forEach((module, index) => {
      const moduleName = moduleNames[index];
      const nameParts = moduleName.split('/');
      
      // Monta a estrutura de objetos aninhados para todos os módulos
      let current = result;
      for (let i = 0; i < nameParts.length - 1; i++) {
        if (!current[nameParts[i]]) {
          current[nameParts[i]] = {};
        }
        current = current[nameParts[i]];
      }
      
      // Detecta conflitos: verifica se a chave final já existe
      const finalKey = nameParts[nameParts.length - 1];
      const fullPath = nameParts.join('.');
      
      if (current[finalKey] && pathRegistry.has(fullPath)) {
        const existingModule = pathRegistry.get(fullPath);
        console.warn(`⚠️ Conflito de caminho de módulo i18n: "${fullPath}" já está ocupado pelo módulo "${existingModule}" ; o módulo "${moduleName}" pode sobrescrever algumas chaves e valores`);
      }
      
      // Registra a associação entre caminho e nome do módulo
      pathRegistry.set(fullPath, moduleName);
      
      // Define o valor final (mantém a mesclagem superficial existente)
      current[finalKey] = { ...current[finalKey], ...module };
    });

    return result;
  }

  /**
   * Pré-carrega os módulos essenciais
   */
  async preloadEssentials(locale: string): Promise<void> {
    const essentials = [
      'core/common',
      'core/navigation',
      'features/chat'
    ];

    await Promise.all(
      essentials.map(module => this.loadModule(locale, module))
    );
  }

  /**
   * Limpa o cache
   */
  clearCache(locale?: string): void {
    if (locale) {
      // Limpa o cache de um idioma específico
      const keys = Array.from(this.cache.keys()).filter((key: string) => key.startsWith(`${locale}:`));
      keys.forEach((key: string) => this.cache.delete(key));
    } else {
      // Limpa todo o cache
      this.cache.clear();
    }
  }

  /**
   * Obtém o estado do carregamento
   */
  getLoadingStatus(): { total: number; loaded: number; modules: ModuleInfo[] } {
    const modules = Array.from(this.moduleRegistry.values());
    const loaded = modules.filter(m => m.loaded).length;
    
    return {
      total: modules.length,
      loaded,
      modules
    };
  }

  /**
   * Recarrega o módulo sem reiniciar
   */
  async reloadModule(locale: string, moduleName: string): Promise<any> {
    const cacheKey = `${locale}:${moduleName}`;
    this.cache.delete(cacheKey);
    
    const moduleInfo = this.moduleRegistry.get(moduleName);
    if (moduleInfo) {
      moduleInfo.loaded = false;
    }
    
    return this.loadModule(locale, moduleName);
  }


} 
