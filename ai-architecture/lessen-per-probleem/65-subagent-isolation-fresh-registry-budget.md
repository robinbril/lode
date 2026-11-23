# Elke delegatie bouwt een verse agent met eigen tool-registry, maar het token-budget van het kind komt niet automatisch van de ouder

Probleem: een sub-agent die de tool-registry of conversatie van zijn ouder deelt, kan per ongeluk tools of state zien die niet voor hem bedoeld waren; een sub-agent zonder enige dieptegrens kan zichzelf eindeloos blijven delegeren.

Oplossing:
- Delegatie bouwt een nieuwe `Agent` met een eigen `ToolRegistry`. De ingebouwde tools worden daarin geregistreerd, maar een agent zonder toekenning krijgt er geen: wat hij mag, komt uit zijn eigen config.
- Het kind erft geen gesprek en geen credentials van de ouder. Het teamgeheugen is wel gedeeld als dat aan staat: de uitkomst van het kind wordt daar ook in weggeschreven. Dit is dus geen volledige isolatie.
- De delegatie-tool weigert zichzelf aanroepen, een onbekend doel, een cyclus (met de keten in de melding), diepte 3 of meer (standaard) en een pool zonder vrij run-slot, dat anders zou vastlopen.
- Het budget van de ouder wordt pas na terugkeer van het kind getoetst; het kind draait onder zijn eigen `maxTokenBudget`. Meerdere delegaties in één beurt worden samen achteraf opgeteld. De documentatie noemt dit een plafond waar een kind niet buiten kan; de code laat een overschrijding toe van alles wat in die beurt liep.
- Wil je een echt plafond: geef het kind bij de start het resterende budget van de ouder mee.

```ts
// eigen schets: resterend budget verdelen vóór de start
const rest = ouder.budget - ouder.verbruikt;
const perKind = Math.floor(rest / aantalKinderenDezeBeurt);
if (perKind <= 0) return fout("geen budget voor delegatie");
```

Waarom het werkt: een verse registry maakt "welke tools heeft dit kind" een keuze in de config in plaats van een erfenis, en de grenzen in de tool gelden voor elke aanroep.

Niet doen als: delegatie nooit dieper dan één niveau gaat; dan is een cyclus- en dieptecheck overbodige complexiteit.

Toetsvraag: kan geen enkel kind meer uitgeven dan wat de ouder bij de start nog over had, ook als er vijf tegelijk starten?

Bronnen:
- open-multi-agent/open-multi-agent@e1059babc907663444a2a475e2548c61b85cea9b packages/core/src/orchestrator/task-execution.ts:79 "Agent instance"
- open-multi-agent/open-multi-agent@e1059babc907663444a2a475e2548c61b85cea9b packages/core/src/tool/built-in/delegate.ts:70 "maxDelegationDepth"
- open-multi-agent/open-multi-agent@e1059babc907663444a2a475e2548c61b85cea9b packages/core/src/agent/runner.ts:1469 "delegationTurnUsage"
- open-multi-agent/open-multi-agent@e1059babc907663444a2a475e2548c61b85cea9b docs/budgets-and-limits.md:260 "cannot spend outside"
