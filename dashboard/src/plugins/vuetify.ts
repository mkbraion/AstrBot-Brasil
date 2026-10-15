import { createVuetify } from 'vuetify';
import { pt, en } from 'vuetify/locale';
import '@/assets/mdi-subset/materialdesignicons-subset.css';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { PurpleTheme } from '@/theme/LightTheme';
import { PurpleThemeDark } from "@/theme/DarkTheme";

export default createVuetify({
  components,
  directives,
  locale: {
    locale: 'pt-BR',
    fallback: 'en',
    messages: { 'pt-BR': pt, en }
  },
  date: { locale: { 'pt-BR': 'pt-BR' } },

  theme: {
    defaultTheme: 'PurpleTheme',
    themes: {
      PurpleTheme,
      PurpleThemeDark
    }
  },
  defaults: {
    VBtn: {},
    VCard: {
      rounded: 'lg'
    },
    VSnackbar: {
      elevation: 6,
      rounded: 'lg'
    },
    VTextField: {
      rounded: 'lg'
    },
    VTooltip: {
      // set v-tooltip default location to top
      location: 'top'
    }
  }
});
