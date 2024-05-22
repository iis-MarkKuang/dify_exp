const translation = {
  list: {
    title: 'Dokumenty',
    desc: 'Wszystkie pliki wiedzy są tutaj pokazane, a cała wiedza może być powiązana z odnośnikami Microcraft lub zindeksowana za pomocą wtyczki Chat.',
    addFile: 'dodaj plik',
    addPages: 'Dodaj strony',
    table: {
      header: {
        fileName: 'NAZWA PLIKU',
        words: 'SŁOWA',
        hitCount: 'LICZBA ZNALEZIEŃ',
        uploadTime: 'CZAS WGRANIA',
        status: 'STATUS',
        action: 'AKCJA',
      },
    },
    action: {
      uploadFile: 'Wgraj nowy plik',
      settings: 'Ustawienia segmentacji',
      addButton: 'Dodaj fragment',
      add: 'Dodaj fragment',
      batchAdd: 'Dodaj partię',
      archive: 'Archiwum',
      unarchive: 'Usuń z archiwum',
      delete: 'Usuń',
      enableWarning: 'Zarchiwizowany plik nie może zostać włączony',
      sync: 'Synchronizuj',
    },
    index: {
      enable: 'Włącz',
      disable: 'Wyłącz',
      all: 'Wszystkie',
      enableTip: 'Plik może być zindeksowany',
      disableTip: 'Plik nie może być zindeksowany',
    },
    status: {
      queuing: 'Oczekiwanie',
      indexing: 'Indeksowanie',
      paused: 'Wstrzymane',
      error: 'Błąd',
      available: 'Dostępny',
      enabled: 'Włączony',
      disabled: 'Wyłączony',
      archived: 'Zaarchiwizowany',
    },
    empty: {
      title: 'Nie ma jeszcze dokumentacji',
      upload: {
        tip: 'Możesz wgrać pliki, synchronizować z witryny lub z aplikacji internetowych takich jak Notion, GitHub, itp.',
      },
      sync: {
        tip: 'Microcraft regularnie pobiera pliki z Twojego Notion i dokonuje ich przetwarzania.',
      },
    },
    delete: {
      title: 'Czy na pewno chcesz usunąć?',
      content:
        'Jeśli będziesz musiał wznowić przetwarzanie później, będziesz kontynuować tam, gdzie przerwałeś',
    },
    batchModal: {
      title: 'Dodaj partię fragmentów',
      csvUploadTitle: 'Przeciągnij i upuść swój plik CSV tutaj, lub ',
      browse: 'wybierz',
      tip: 'Plik CSV musi być zgodny z następującą strukturą:',
      question: 'pytanie',
      answer: 'odpowiedź',
      contentTitle: 'treść fragmentu',
      content: 'treść',
      template: 'Pobierz szablon tutaj',
      cancel: 'Anuluj',
      run: 'Uruchom partię',
      runError: 'Błąd uruchomienia partii',
      processing: 'Przetwarzanie partii',
      completed: 'Import zakończony',
      error: 'Błąd importu',
      ok: 'OK',
    },
  },
  metadata: {
    title: 'Metadane',
    desc: 'Etykietowanie metadanych dla dokumentów pozwala sztucznej inteligencji na dostęp do nich w odpowiednim czasie i ujawnia źródło odniesień dla użytkowników.',
    dateTimeFormat: 'D MMMM YYYY, HH:mm',
    docTypeSelectTitle: 'Wybierz rodzaj dokumentu',
    docTypeChangeTitle: 'Zmień rodzaj dokumentu',
    docTypeSelectWarning:
      'Jeśli zmieniony zostanie rodzaj dokumentu, teraz wypełnione metadane nie zostaną zachowane',
    firstMetaAction: 'Zacznijmy',
    placeholder: {
      add: 'Dodaj ',
      select: 'Wybierz ',
    },
    source: {
      upload_file: 'Wgraj plik',
      notion: 'Synchronizuj z Notion',
      github: 'Synchronizuj z Github',
    },
    type: {
      book: 'Książka',
      webPage: 'Strona internetowa',
      paper: 'Artykuł',
      socialMediaPost: 'Post w mediach społecznościowych',
      personalDocument: 'Dokument osobisty',
      businessDocument: 'Dokument biznesowy',
      IMChat: 'Czat na komunikatorze',
      wikipediaEntry: 'Artykuł w Wikipedii',
      notion: 'Synchronizuj z Notion',
      github: 'Synchronizuj z Github',
      technicalParameters: 'Parametry techniczne',
    },
    field: {
      processRule: {
        processDoc: 'Przetwórz dokument',
        segmentRule: 'Reguła fragmentacji',
        segmentLength: 'Długość fragmentów',
        processClean: 'Oczyszczanie tekstu',
      },
      book: {
        title: 'Tytuł',
        language: 'Język',
        author: 'Autor',
        publisher: 'Wydawca',
        publicationDate: 'Data publikacji',
        ISBN: 'ISBN',
        category: 'Kategoria',
      },
      webPage: {
        title: 'Tytuł',
        url: 'URL',
        language: 'Język',
        authorPublisher: 'Autor/Wydawca',
        publishDate: 'Data publikacji',
        topicsKeywords: 'Tematy/Słowa kluczowe',
        description: 'Opis',
      },
      paper: {
        title: 'Tytuł',
        language: 'Język',
        author: 'Autor',
        publishDate: 'Data publikacji',
        journalConferenceName: 'Nazwa czasopisma/konferencji',
        volumeIssuePage: 'Tom/Wydanie/Strona',
        DOI: 'DOI',
        topicsKeywords: 'Tematy/Słowa kluczowe',
        abstract: 'Abstrakt',
      },
      socialMediaPost: {
        platform: 'Platforma',
        authorUsername: 'Autor/Nazwa użytkownika',
        publishDate: 'Data publikacji',
        postURL: 'Adres URL posta',
        topicsTags: 'Tematy/Tagi',
      },
      personalDocument: {
        title: 'Tytuł',
        author: 'Autor',
        creationDate: 'Data utworzenia',
        lastModifiedDate: 'Data ostatniej modyfikacji',
        documentType: 'Typ dokumentu',
        tagsCategory: 'Tagi/Kategoria',
      },
      businessDocument: {
        title: 'Tytuł',
        author: 'Autor',
        creationDate: 'Data utworzenia',
        lastModifiedDate: 'Data ostatniej modyfikacji',
        documentType: 'Typ dokumentu',
        departmentTeam: 'Dział/Zespół',
      },
      IMChat: {
        chatPlatform: 'Platforma czatu',
        chatPartiesGroupName: 'Podmioty czatu/Nazwa grupy',
        participants: 'Uczestnicy',
        startDate: 'Data rozpoczęcia',
        endDate: 'Data zakończenia',
        topicsKeywords: 'Tematy/Słowa kluczowe',
        fileType: 'Typ pliku',
      },
      wikipediaEntry: {
        title: 'Tytuł',
        language: 'Język',
        webpageURL: 'Adres URL strony internetowej',
        editorContributor: 'Edytor/Współtwórca',
        lastEditDate: 'Data ostatniej edycji',
        summaryIntroduction: 'Podsumowanie/Wstęp',
      },
      notion: {
        title: 'Tytuł',
        language: 'Język',
        author: 'Autor',
        createdTime: 'Czas utworzenia',
        lastModifiedTime: 'Czas ostatniej modyfikacji',
        url: 'URL',
        tag: 'Tag',
        description: 'Opis',
      },
      github: {
        repoName: 'Nazwa repozytorium',
        repoDesc: 'Opis repozytorium',
        repoOwner: 'Właściciel repozytorium',
        fileName: 'Nazwa pliku',
        filePath: 'Ścieżka pliku',
        programmingLang: 'Język programowania',
        url: 'URL',
        license: 'Licencja',
        lastCommitTime: 'Czas ostatniego zobowiązania',
        lastCommitAuthor: 'Autor ostatniego zobowiązania',
      },
      originInfo: {
        originalFilename: 'Oryginalna nazwa pliku',
        originalFileSize: 'Oryginalny rozmiar pliku',
        uploadDate: 'Data wgrywania',
        lastUpdateDate: 'Data ostatniej aktualizacji',
        source: 'Źródło',
      },
      technicalParameters: {
        segmentSpecification: 'Specyfikacja fragmentów',
        segmentLength: 'Długość fragmentów',
        avgParagraphLength: 'Średnia długość akapitu',
        paragraphs: 'Akapity',
        hitCount: 'Liczba odwołań',
        embeddingTime: 'Czas embedowania',
        embeddedSpend: 'Wydatki związane z embedowaniem',
      },
    },
    languageMap: {
      zh: 'Chiński',
      en: 'Angielski',
      es: 'Hiszpański',
      fr: 'Francuski',
      de: 'Niemiecki',
      ja: 'Japoński',
      ko: 'Koreański',
      ru: 'Rosyjski',
      ar: 'Arabski',
      pt: 'Portugalski',
      it: 'Włoski',
      nl: 'Holenderski',
      pl: 'Polski',
      sv: 'Szwedzki',
      tr: 'Turecki',
      he: 'Hebrajski',
      hi: 'Hinduski',
      da: 'Duński',
      fi: 'Fiński',
      no: 'Norweski',
      hu: 'Węgierski',
      el: 'Grecki',
      cs: 'Czeski',
      th: 'Tajski',
      id: 'Indonezyjski',
    },
    categoryMap: {
      book: {
        fiction: 'Literatura piękna',
        biography: 'Biografia',
        history: 'Historia',
        science: 'Nauka',
        technology: 'Technologia',
        education: 'Edukacja',
        philosophy: 'Filozofia',
        religion: 'Religia',
        socialSciences: 'Nauki społeczne',
        art: 'Sztuka',
        travel: 'Podróże',
        health: 'Zdrowie',
        selfHelp: 'Samorozwój',
        businessEconomics: 'Biznes/ekonomia',
        cooking: 'Gotowanie',
        childrenYoungAdults: 'Dzieci/Młodzież',
        comicsGraphicNovels: 'Komiksy/Graphic Novels',
        poetry: 'Poezja',
        drama: 'Dramat',
        other: 'Inne',
      },
      personalDoc: {
        notes: 'Notatki',
        blogDraft: 'Wersja robocza bloga',
        diary: 'Dziennik',
        researchReport: 'Raport badawczy',
        bookExcerpt: 'Fragment książki',
        schedule: 'Harmonogram',
        list: 'Lista',
        projectOverview: 'Przegląd projektu',
        photoCollection: 'Kolekcja zdjęć',
        creativeWriting: 'Twórcze pisanie',
        codeSnippet: 'Fragment kodu',
        designDraft: 'Projekt/wersja robocza',
        personalResume: 'CV',
        other: 'Inne',
      },
      businessDoc: {
        meetingMinutes: 'Protokoły zebrań',
        researchReport: 'Raport badawczy',
        proposal: 'Propozycja',
        employeeHandbook: 'Podręcznik pracownika',
        trainingMaterials: 'Materiały szkoleniowe',
        requirementsDocument: 'Dokument wymagań',
        designDocument: 'Dokument projektowy',
        productSpecification: 'Specyfikacja produktu',
        financialReport: 'Raport finansowy',
        marketAnalysis: 'Analiza rynku',
        projectPlan: 'Plan projektu',
        teamStructure: 'Struktura zespołu',
        policiesProcedures: 'Zasady i procedury',
        contractsAgreements: 'Umowy',
        emailCorrespondence: 'Korespondencja e-mailowa',
        other: 'Inne',
      },
    },
  },
  embedding: {
    processing: 'Przetwarzanie osadzania...',
    paused: 'Osadzanie wstrzymane',
    completed: 'Osadzanie zakończone',
    error: 'Błąd osadzania',
    docName: 'Przetwarzanie wstępne dokumentu',
    mode: 'Reguła segmentacji',
    segmentLength: 'Długość fragmentów',
    textCleaning: 'Predefinicja tekstu i czyszczenie',
    segments: 'Akapity',
    highQuality: 'Tryb wysokiej jakości',
    economy: 'Tryb ekonomiczny',
    estimate: 'Szacowany czas',
    stop: 'Zatrzymaj przetwarzanie',
    resume: 'Wznów przetwarzanie',
    automatic: 'Automatyczny',
    custom: 'Niestandardowy',
    previewTip: 'Podgląd akapitu będzie dostępny po zakończeniu osadzania',
  },
  segment: {
    paragraphs: 'Akapity',
    keywords: 'Słowa kluczowe',
    addKeyWord: 'Dodaj słowo kluczowe',
    keywordError: 'Maksymalna długość słowa kluczowego wynosi 20',
    characters: 'znaków',
    hitCount: 'Liczba odwołań',
    vectorHash: 'Wektor hash: ',
    questionPlaceholder: 'dodaj pytanie tutaj',
    questionEmpty: 'Pytanie nie może być puste',
    answerPlaceholder: 'dodaj odpowiedź tutaj',
    answerEmpty: 'Odpowiedź nie może być pusta',
    contentPlaceholder: 'dodaj treść tutaj',
    contentEmpty: 'Treść nie może być pusta',
    newTextSegment: 'Nowy segment tekstowy',
    newQaSegment: 'Nowy segment Q&A',
    delete: 'Usunąć ten fragment?',
  },
}

export default translation
