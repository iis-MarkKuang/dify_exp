const translation = {
  title: 'Інструменти',
  createCustomTool: 'Створити власний інструмент',
  type: {
    all: 'Усі',
    builtIn: 'Вбудовані',
    custom: 'Користувацькі',
  },
  contribute: {
    line1: 'Мені цікаво зробити свій внесок',
    line2: 'створення інструментів для Microcraft.',
    viewGuide: 'Переглянути інструкцію',
  },
  author: 'Автор',
  auth: {
    unauthorized: 'Авторизуватися',
    authorized: 'Авторизовано',
    setup: 'Налаштувати авторизацію, щоб використовувати',
    setupModalTitle: 'Налаштування авторизації',
    setupModalTitleDescription: 'Після налаштування облікових даних усі члени робочого простору можуть використовувати цей інструмент під час оркестрування програм.',
  },
  includeToolNum: '{{num}} інструмент(ів) включено',
  addTool: 'Додати інструмент ',
  createTool: {
    title: 'Створити власний інструмент',
    editAction: 'Налаштування',
    editTitle: 'Редагувати настроюваний інструмент',
    name: 'Назва',
    toolNamePlaceHolder: 'Введіть назву інструменту',
    schema: 'Схема',
    schemaPlaceHolder: 'Введіть свою схему OpenAPI тут',
    viewSchemaSpec: 'Переглянути специфікацію OpenAPI-Swagger',
    importFromUrl: 'Імпортувати з URL-адреси',
    importFromUrlPlaceHolder: 'https://...',
    urlError: 'Введіть дійсну URL-адресу',
    examples: 'Приклади',
    exampleOptions: {
      json: 'Погода (JSON)',
      yaml: 'Зоотоварів (YAML)',
      blankTemplate: 'Чистий шаблон',
    },
    availableTools: {
      title: 'Доступні інструменти',
      name: 'Назва',
      description: 'Опис',
      method: 'Метод',
      path: 'Шлях',
      action: 'Дія',
      test: 'Перевірка',
    },
    authMethod: {
      title: 'Метод авторизації',
      type: 'Тип авторизації',
      keyTooltip: 'Ключ HTTP-заголовка. Якщо ви не знаєте, залиште його як "Authorization" або встановіть власне значення',
      types: {
        none: 'Відсутня',
        api_key: 'API-ключ',
        apiKeyPlaceholder: 'Назва HTTP-заголовка для API-ключа',
        apiValuePlaceholder: 'Введіть API-ключ',
      },
      key: 'Ключ',
      value: 'Значення',
    },
    authHeaderPrefix: {
      types: {
        basic: 'Basic',
        bearer: 'Bearer',
        custom: 'Custom',
      },
    },
    privacyPolicy: 'Політика конфіденційності',
    privacyPolicyPlaceholder: 'Введіть політику конфіденційності',
  },

  test: {
    title: 'Тест',
    parametersValue: 'Параметри та значення',
    parameters: 'Параметри',
    value: 'Значення',
    testResult: 'Результати тесту',
    testResultPlaceholder: 'Результат тесту буде відображатися тут',
  },
  thought: {
    using: 'Використання',
    used: 'Використано',
    requestTitle: 'Запит до',
    responseTitle: 'Відповідь від',
  },
  setBuiltInTools: {
    info: 'Інформація',
    setting: 'Налаштування',
    toolDescription: 'Опис інструменту',
    parameters: 'Параметри',
    string: 'Рядок',
    number: 'Число',
    required: 'Обов’язково',
    infoAndSetting: 'Інформація та налаштування',
  },
  noCustomTool: {
    title: 'Немає користувацьких інструментів!',
    content: 'Додавайте та керуйте своїми власними інструментами тут для створення програм зі штучним інтелектом.',
    createTool: 'Створити інструмент',
  },
  noSearchRes: {
    title: 'Вибачте, немає результатів!',
    content: 'Ми не знайшли жодних інструментів, які б відповідали вашому пошуку.',
    reset: 'Скинути пошук',
  },
  builtInPromptTitle: 'Підказка',
  toolRemoved: 'Інструмент видалено',
  notAuthorized: 'Інструмент не авторизовано',
  howToGet: 'Як отримати',
}

export default translation
