export const KEYWORD_CATEGORIES = {

    "Literatur": "literatur_1",
    "Sophie von La Roches Werke": "literatur_2",
    "Schaffensprozess": "literatur_3",
    "Inhalt eigener Werke": "literatur_3",
    "Rezeption eigener Werke": "literatur_3",
    "Schriftstellerische Tätigkeit als Frau": "literatur_3",
    "Johann Isaak von Gernings Werke": "literatur_2",
    "Johann Isaak von Gernings Dichtung": "literatur_3",
    "Rezeption anderer Werke": "literatur_2",
    "Kulturgeschichtliches Buch": "literatur_3",
    "Dichtung": "literatur_3",
    "Biographisches Werk": "literatur_3",
    "Brief": "literatur_3",
    "Philosophischer Text": "literatur_3",
    "Kunst": "literatur_3",

    "Geselligkeit/Beziehungen": "beziehungen_1",
    "Freundschaft": "beziehungen_2",
    "Freundschaft mit Wieland": "beziehungen_3",
    "Familie": "beziehungen_2",
    "Sophie von La Roches Kinder": "beziehungen_3",
    "Sophie von La Roches Enkel*innen": "beziehungen_3",
    "Johann Isaak von Gernings Mutter": "beziehungen_3",
    "Schriftsteller-/Dichterkreis": "beziehungen_2",
    "Weimarer Viergestirn (Goethe, Schiller, Herder, Wieland)": "beziehungen_3",
    "Liebesbeziehung": "beziehungen_2",
    "Verliebtheit Gernings": "beziehungen_3",
    "Bekanntschaften": "beziehungen_2",

    "Persönliches": "persoenliches_1",
    "Alter": "persoenliches_2",
    "Krankheit": "persoenliches_2",
    "Haus und Garten": "persoenliches_2",
    "Personal/Dienstleister": "persoenliches_2",
    "Geschäfte/Verkauf": "persoenliches_2",

    "Reisen": "reisen_1",
    "Deutschland (Reisen)": "reisen_2",
    "Taunus": "reisen_3",
    "Italien (Reisen)": "reisen_2",
    "Natur": "reisen_2",
    "Ausflug": "reisen_2",

    "Politik": "politik_1",
    "Deutschland (Politik)": "politik_2",
    "Innenpolitische Unruhe": "politik_3",
    "Revolution": "politik_2",
    "Frankreich (Politik)": "politik_2",
    "Italien (Politik)": "politik_2",
    "Deutschland - Frankreich": "politik_2",
    "Koalitionskriege": "politik_3",

    "Sprechakt": "sprechakt_1",
    "Wunsch": "sprechakt_2",
    "Appell": "sprechakt_2",
    "Dank": "sprechakt_2",
    "Lob": "sprechakt_2",
    "Warnung": "sprechakt_2",
    "Kondolenz": "sprechakt_2",
    "Ratschlag": "sprechakt_2",
    "Empfehlung": "sprechakt_2",
    "Bitte": "sprechakt_2",
    "Bitte um Besorgung": "sprechakt_3",
    "Bitte um Besorgung von Büchern": "sprechakt_4",
    "Bitte um Weitersendung von Büchern": "sprechakt_3",
    "Bitte um Weitersendung von Briefen": "sprechakt_3",

    "Emotion": "emotion_1",
    "Freude": "emotion_2",
    "Trauer": "emotion_2",
    "Trübsinnigkeit": "emotion_2",
    "Missbilligung": "emotion_2",
    "Streit": "emotion_2",

    "Warensendung": "warensendung_1",
    "Warensendung Literatur": "warensendung_2",
    "Rückgabe geliehener Literatur": "warensendung_2",
    "Sendung Brief": "warensendung_2",
    "Rücksendung Brief": "warensendung_2",

    "Zitat": "zitat_1",
    "Zitat Gedicht": "zitat_2",
    "Zitat philosophischer Text": "zitat_2",

    "Ästhetischer Sprachgebrauch": "andere_1",
    "Antike griechische Schriftsteller": "andere_1",
    "Erziehung": "andere_1",
    "Religion": "andere_1"

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
    label: "Geselligkeit/Beziehungen",
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

