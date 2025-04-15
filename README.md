# Changes

### 1. **Language Cookie Management**

A functionality has been added to check if the `lang` cookie is set in the user's browser. If the `lang` cookie is not set, it defaults to `lang=en`, ensuring that the language preference is saved for future visits.

- **Event Listener**: 
  - An event listener is triggered on `DOMContentLoaded` to check for the presence of the `lang` cookie.
  - If the cookie doesn't exist, it automatically sets `lang=en` as the default language.

### 2. **Translation Function**

A translation function was created to handle multiple languages (English, French, and Italian). This function dynamically loads the correct translation based on the selected language from a dictionary object. The dictionary contains the translations for key phrases, such as "welcome," in each supported language.

- **Supported Languages**:
  - English (`en`)
  - French (`fr`)
  - Italian (`it`)

The main dictionary (example) is structured as follows:

```python
{
    'en': {'welcome': 'Welcome'},
    'fr': {'welcome': 'Bienvenue'},
    'it': {'welcome': 'Benvenuto'}
}
```

### 3. **Removal of i18n, bottle_i18n and all regarding features**

### 4. **First installer test**

# Work to do

### Dynamically generated site

For now the site, after it's first load, it's static and does not change even when the language is set.

## Possible Solutions

1. **Dynamic Translation Implementation**  
   Implement dynamic translation (see how `{{ current_lang }}` works in the HTML).

2. **Creation of Separate Pages**  
   Create separate pages for different languages. When errors and informational messages need to be translated, the rest of the content can remain static.