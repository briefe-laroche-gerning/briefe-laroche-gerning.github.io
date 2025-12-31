export const KEYWORD_CATEGORIES = {

    "Literatur": "literatur_oberkategorie",
    "Sophie von La Roches Werke": "literatur",
    "Schaffensprozess": "literatur",
    "Inhalt eigener Werke": "literatur",
    "Rezeption eigener Werke": "literatur",
    "Schriftstellerische Tätigkeit als Frau": "literatur",
    "Johann Isaak von Gernings Werke": "literatur",
    "Johann Isaak von Gernings Dichtung": "literatur",
    "Rezeption anderer Werke": "literatur",
    "Kulturgeschichtliches Buch": "literatur",
    "Dichtung": "literatur",
    "Biographisches Werk": "literatur",
    "Brief": "literatur",
    "Philosophischer Text": "literatur",
    "Kunst": "literatur",

    "Geselligkeit/Beziehungen": "beziehungen_oberkategorie",
    "Freundschaft": "beziehungen",
    "Freundschaft mit Wieland": "beziehungen",
    "Familie": "beziehungen",
    "Sophie von La Roches Kinder": "beziehungen",
    "Sophie von La Roches Enkel*innen": "beziehungen",
    "Johann Isaak von Gernings Mutter": "beziehungen",
    "Schriftsteller-/Dichterkreis": "beziehungen",
    "Weimarer Viergestirn (Goethe, Schiller, Herder, Wieland)": "beziehungen",
    "Liebesbeziehung": "beziehungen",
    "Verliebtheit Gernings": "beziehungen",
    "Bekanntschaften": "beziehungen",

    "Persönliches": "persoenliches_oberkategorie",
    "Alter": "persoenliches",
    "Krankheit": "persoenliches",
    "Haus und Garten": "persoenliches",
    "Personal/Dienstleister": "persoenliches",
    "Geschäfte/Verkauf": "persoenliches",

    "Politik": "politik_oberkategorie",
    "Deutschland (Politik)": "politik",
    "Innenpolitische Unruhe": "politik",
    "Revolution": "politik",
    "Frankreich (Politik)": "politik",
    "Italien (Politik)": "politik",
    "Deutschland - Frankreich": "politik",
    "Koalitionskriege": "politik",
 
    "Reisen": "reisen_oberkategorie",
    "Deutschland (Reisen)": "reisen",
    "Taunus": "reisen",
    "Italien (Reisen)": "reisen",
    "Natur": "reisen",
    "Ausflug": "reisen",

    "Emotion": "emotion_oberkategorie",
    "Freude": "emotion",
    "Trauer": "emotion",
    "Trübsinnigkeit": "emotion",
    "Missbilligung": "emotion",
    "Streit": "emotion",

    "Sprechakt": "sprechakt_oberkategorie",
    "Wunsch": "sprechakt",
    "Appell": "sprechakt",
    "Dank": "sprechakt",
    "Lob": "sprechakt",
    "Warnung": "sprechakt",
    "Kondolenz": "sprechakt",
    "Ratschlag": "sprechakt",
    "Empfehlung": "sprechakt",
    "Bitte": "sprechakt",
    "Bitte um Besorgung": "sprechakt",
    "Bitte um Besorgung von Büchern": "sprechakt",
    "Bitte um Weitersendung von Büchern": "sprechakt",
    "Bitte um Weitersendung von Briefen": "sprechakt",

    "Ästhetischer Sprachgebrauch": "andere",
    "Antike griechische Schriftsteller": "andere",
    "Erziehung": "andere",
    "Religion": "andere",

    "Warensendung": "warensendung_oberkategorie",
    "Warensendung Literatur": "warensendung",
    "Rückgabe geliehener Literatur": "warensendung",
    "Sendung Brief": "warensendung",
    "Rücksendung Brief": "warensendung",

    "Zitat": "zitat_oberkategorie",
    "Zitat Gedicht": "zitat",
    "Zitat philosophischer Text": "zitat"

};


export const ALL_KEYWORDS = Object.keys(KEYWORD_CATEGORIES);


export const KEYWORD_TREE = {
  literatur: {
    label: "Literatur",
    color: "literatur",
    children: {
      la_roche: {
        label: "Sophie von La Roches Werke",
        children: {
          schaffensprozess: { label: "Schaffensprozess" },
          inhalt: { label: "Inhalt eigener Werke" },
          rezeption: { label: "Rezeption eigener Werke" },
          frau: { label: "Schriftstellerische Tätigkeit als Frau" }
        }
      },

      gerning: {
        label: "Johann Isaak von Gernings Werke",
        children: {
          dichtung: { label: "Johann Isaak von Gernings Dichtung" }
        }
      },

      rezeption_andere: {
        label: "Rezeption anderer Werke",
        children: {
          kultur: { label: "Kulturgeschichtliches Buch" },
          dichtung: { label: "Dichtung" },
          bio: { label: "Biographisches Werk" },
          brief: { label: "Brief" },
          philosophie: { label: "Philosophischer Text" },
          kunst: { label: "Kunst" }
        }
      }
    }
  },

  beziehungen: {
    label: "Geselligkeit / Beziehungen",
    color: "beziehungen",
    children: {
      freundschaft: {
        label: "Freundschaft",
        children: {
          wieland: { label: "Freundschaft mit Wieland" }
        }
      },
      familie: {
        label: "Familie",
        children: {
          kinder: { label: "Sophie von La Roches Kinder" },
          enkel: { label: "Sophie von La Roches Enkel*innen" },
          mutter: { label: "Johann Isaak von Gernings Mutter" }
        }
      },
      dichterkreis: {
        label: "Schriftsteller-/Dichterkreis",
        children: {
          viergestirn: {
            label: "Weimarer Viergestirn (Goethe, Schiller, Herder, Wieland)"
          }
        }
      },
      liebe: {
        label: "Liebesbeziehung",
        children: {
          verliebtheit: { label: "Verliebtheit Gernings" }
        }
      },
      bekanntschaften: { label: "Bekanntschaften" }
    }
  },

  persoenliches: {
    label: "Persönliches",
    color: "persoenliches",
    children: {
      alter: { label: "Alter" },
      krankheit: { label: "Krankheit" },
      haus: { label: "Haus und Garten" },
      personal: { label: "Personal/Dienstleister" },
      geschaefte: { label: "Geschäfte/Verkauf" }
    }
  },

  politik: {
    label: "Politik",
    color: "politik",
    children: {
      deutschland: {
        label: "Deutschland (Politik)",
        children: {
          innenpolitik: { label: "Innenpolitische Unruhe" }
        }
      },
      revolution: { label: "Revolution" },
      frankreich: { label: "Frankreich (Politik)" },
      italien: { label: "Italien (Politik)" },
      df: {
        label: "Deutschland - Frankreich",
        children: {
          kriege: { label: "Koalitionskriege" }
        }
      }
    }
  },

  reisen: {
    label: "Reisen",
    color: "reisen",
    children: {
      deutschland: {
        label: "Deutschland (Reisen)",
        children: {
          taunus: { label: "Taunus" }
        }
      },
      italien: { label: "Italien (Reisen)" },
      natur: { label: "Natur" },
      ausflug: { label: "Ausflug" }
    }
  },

  emotion: {
    label: "Emotion",
    color: "emotion",
    children: {
      freude: { label: "Freude" },
      trauer: { label: "Trauer" },
      truebsinn: { label: "Trübsinnigkeit" },
      missbilligung: { label: "Missbilligung" },
      streit: { label: "Streit" }
    }
  },

  sprechakt: {
    label: "Sprechakt",
    color: "sprechakt",
    children: {
      wunsch: { label: "Wunsch" },
      appell: { label: "Appell" },
      dank: { label: "Dank" },
      lob: { label: "Lob" },
      warnung: { label: "Warnung" },
      kondolenz: { label: "Kondolenz" },
      ratschlag: { label: "Ratschlag" },
      empfehlung: { label: "Empfehlung" },
      bitte: {
        label: "Bitte",
        children: {
          besorgung: {
            label: "Bitte um Besorgung",
            children: {
              buecher: { label: "Bitte um Besorgung von Büchern" }
            }
          },
          weitersendung_buecher: {
            label: "Bitte um Weitersendung von Büchern"
          },
          weitersendung_briefe: {
            label: "Bitte um Weitersendung von Briefen"
          }
        }
      }
    }
    },


  warensendung: {
    label: "Warensendung",
    color: "warensendung",
    children: {
      literatur: { label: "Warensendung Literatur" },
      rueckgabe_lit: { label: "Rückgabe geliehener Literatur" },
      brief: { label: "Sendung Brief" },
      ruecksendung: { label: "Rücksendung Brief" }
    }
  },

  zitat: {
    label: "Zitat",
    color: "zitat",
    children: {
      gedicht: { label: "Zitat Gedicht" },
      philosophie: { label: "Zitat philosophischer Text" }
    }
  },

      aesthetik: {
        label: "Ästhetischer Sprachgebrauch"
    },
    antikeGriechen: {
        label: "Antike griechische Schriftsteller"
    },
    erziehung: {
        label: "Erziehung"
    },
    religion: {
        label: "Religion"
    }

};

