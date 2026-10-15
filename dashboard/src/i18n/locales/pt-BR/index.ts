// Catálogo completo de português do Brasil. O fallback protege atualizações futuras.
import ptBRCommon from './core/common.json';
import ptBRActions from './core/actions.json';
import ptBRStatus from './core/status.json';
import ptBRNavigation from './core/navigation.json';
import ptBRHeader from './core/header.json';
import ptBRShared from './core/shared.json';
import ptBRChat from './features/chat.json';
import ptBRExtension from './features/extension.json';
import ptBRConversation from './features/conversation.json';
import ptBRSessionManagement from './features/session-management.json';
import ptBRToolUse from './features/tool-use.json';
import ptBRProvider from './features/provider.json';
import ptBRPlatform from './features/platform.json';
import ptBRConfig from './features/config.json';
import ptBRConfigMetadata from './features/config-metadata.json';
import ptBRConsole from './features/console.json';
import ptBRTrace from './features/trace.json';
import ptBRAbout from './features/about.json';
import ptBRSettings from './features/settings.json';
import ptBRAuth from './features/auth.json';
import ptBRChart from './features/chart.json';
import ptBRDashboard from './features/dashboard.json';
import ptBRCron from './features/cron.json';
import ptBRStats from './features/stats.json';
import ptBRAlkaidIndex from './features/alkaid/index.json';
import ptBRAlkaidKnowledgeBase from './features/alkaid/knowledge-base.json';
import ptBRAlkaidMemory from './features/alkaid/memory.json';
import ptBRKnowledgeBaseIndex from './features/knowledge-base/index.json';
import ptBRKnowledgeBaseDetail from './features/knowledge-base/detail.json';
import ptBRKnowledgeBaseDocument from './features/knowledge-base/document.json';
import ptBRPersona from './features/persona.json';
import ptBRCommand from './features/command.json';
import ptBRSubagent from './features/subagent.json';
import ptBRWelcome from './features/welcome.json';
import ptBRErrors from './messages/errors.json';
import ptBRSuccess from './messages/success.json';
import ptBRValidation from './messages/validation.json';

import enUS from '../en-US';

function mergeDeep(base: any, patch: any): any {
  if (Array.isArray(patch)) return [...patch];
  if (patch === null || typeof patch !== 'object') return patch;
  const result: any = base && typeof base === 'object' && !Array.isArray(base) ? { ...base } : {};
  for (const [key, value] of Object.entries(patch)) {
    result[key] = value && typeof value === 'object' && !Array.isArray(value)
      ? mergeDeep(result[key], value)
      : Array.isArray(value) ? [...value] : value;
  }
  return result;
}

const ptBR = {
    core: {
      common: ptBRCommon,
      actions: ptBRActions,
      status: ptBRStatus,
      navigation: ptBRNavigation,
      header: ptBRHeader,
      shared: ptBRShared
    },
    features: {
      chat: ptBRChat,
      extension: ptBRExtension,
      conversation: ptBRConversation,
      'session-management': ptBRSessionManagement,
      tooluse: ptBRToolUse,
      provider: ptBRProvider,
      platform: ptBRPlatform,
      config: ptBRConfig,
      'config-metadata': ptBRConfigMetadata,
      console: ptBRConsole,
      trace: ptBRTrace,
      about: ptBRAbout,
      settings: ptBRSettings,
      auth: ptBRAuth,
      chart: ptBRChart,
      dashboard: ptBRDashboard,
      cron: ptBRCron,
      stats: ptBRStats,
      alkaid: {
        index: ptBRAlkaidIndex,
        'knowledge-base': ptBRAlkaidKnowledgeBase,
        memory: ptBRAlkaidMemory
      },
      'knowledge-base': {
        index: ptBRKnowledgeBaseIndex,
        detail: ptBRKnowledgeBaseDetail,
        document: ptBRKnowledgeBaseDocument
      },
      persona: ptBRPersona,
      command: ptBRCommand,
      subagent: ptBRSubagent,
      welcome: ptBRWelcome
    },
    messages: {
      errors: ptBRErrors,
      success: ptBRSuccess,
      validation: ptBRValidation
    }
  };

export default mergeDeep(enUS, ptBR) as typeof enUS;
