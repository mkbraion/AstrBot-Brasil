// AstrBot Brasil — pacote de idioma pt-BR.
// Chaves ainda não localizadas usam en-US como fallback temporário para
// preservar funcionalidade enquanto a cobertura brasileira é ampliada.
import enUS from '../en-US';
import common from './core/common.json';
import actions from './core/actions.json';
import status from './core/status.json';
import navigation from './core/navigation.json';
import auth from './features/auth.json';
import welcome from './features/welcome.json';
import dashboard from './features/dashboard.json';
import about from './features/about.json';
import consoleMessages from './features/console.json';
import errors from './messages/errors.json';
import success from './messages/success.json';
import validation from './messages/validation.json';

export default {
  ...enUS,
  core: {
    ...enUS.core,
    common: { ...enUS.core.common, ...common },
    actions: { ...enUS.core.actions, ...actions },
    status: { ...enUS.core.status, ...status },
    navigation: { ...enUS.core.navigation, ...navigation }
  },
  features: {
    ...enUS.features,
    auth: { ...enUS.features.auth, ...auth },
    welcome: { ...enUS.features.welcome, ...welcome },
    dashboard: { ...enUS.features.dashboard, ...dashboard },
    about: { ...enUS.features.about, ...about },
    console: { ...enUS.features.console, ...consoleMessages }
  },
  messages: {
    ...enUS.messages,
    errors: { ...enUS.messages.errors, ...errors },
    success: { ...enUS.messages.success, ...success },
    validation: { ...enUS.messages.validation, ...validation }
  }
};
