# De parameterlijst van een recipe moet precies de `{{ }}`-variabelen in de template dekken, en bij het renderen is een onbekende variabele een fout

Probleem: een herbruikbare agent-opdracht met gaten erin breekt stil. Een parameter die niemand gebruikt blijft staan, een variabele zonder definitie wordt een lege string in de prompt.

Oplossing:
- Een recipe is een YAML- of JSON-bestand met `title`, `description` en minstens één niet-lege `instructions` of `prompt`. Verder `parameters`, `extensions`, `sub_recipes`, `response` (JSON-schema) en `retry`.
- Een parameter heeft `key`, `input_type` (`string`, `number`, `boolean`, `date`, `file`, `select`), `requirement` (`required`, `optional`, `user_prompt`), `description`, `default` en `options`.
- De sleutels van de parameters moeten gelijk zijn aan de variabelen in de template, op `recipe_dir` na. Een ontbrekende definitie en een overbodige definitie zijn allebei een fout, net als een dubbele sleutel. Een `{{ }}` die niet als template te lezen is, wordt als gewone tekst bewaard en telt niet mee. Een meegegeven waarde met een onbekende sleutel wordt in deze functies niet geweigerd.
- `optional` zonder `default` is een fout. Een `file`-parameter met `default` ook, volgens de foutmelding om geen gevoelige gebruikersbestanden te importeren. De aanroeper kan nog steeds elk leesbaar pad opgeven, dat beperkt deze code niet.
- Grenzen: 32 parameters, 200 selectopties in totaal, 128 KiB geserialiseerd.
- Waarde per parameter: opgegeven waarde, dan `default`, dan pas een vraag aan de gebruiker (alleen bij `user_prompt` en alleen als er een vraagfunctie is), anders ontbreekt hij. Ontbrekende sleutels geven één fout met de hele lijst, vóór het renderen. Een `required` met `default` krijgt dus gewoon die default.
- Renderen gebeurt met minijinja in `Strict` modus en het resultaat wordt opnieuw ingelezen en gevalideerd. Een `include` mag niet buiten de recipemap (`..`, root en prefix worden geweigerd, en het echte pad na symlinks moet erbinnen liggen). Een subrecipe-pad heeft die grens niet, dat moet alleen bestaan.
- Ik vond in de crate geen controle van een waarde tegen `options` of `input_type`. Doe die zelf aan de rand.

```ts
type Param = { key: string; requirement: 'required' | 'optional' | 'user_prompt'; default?: string };
function resolve(params: Param[], given: Record<string, string>, ask?: (k: string) => string) {
  const values = { ...given };
  const missing: string[] = [];
  for (const p of params) {
    const v = given[p.key] ?? p.default ?? (p.requirement === 'user_prompt' ? ask?.(p.key) : undefined);
    if (v === undefined) missing.push(p.key); else values[p.key] = v;
  }
  return { values, missing }; // render only when missing is empty
}
```

Waarom het werkt: de fouten komen bij het laden en bij het aanroepen met de sleutelnaam erbij, niet pas als het model een rare prompt krijgt.

Niet doen als: je een recipe eenmalig en alleen voor jezelf schrijft; de strengheid kost dan meer dan ze oplevert.

Toetsvraag: faalt het laden van een recipe als een parameter nergens in de template voorkomt?

Bronnen:
- aaif-goose/goose@059fee25f13fa92be561a7d42cdd04ececef5a98 crates/goose/src/recipe/validate_recipe.rs:564 "fn validate_parameters_in_template"
- aaif-goose/goose@059fee25f13fa92be561a7d42cdd04ececef5a98 crates/goose/src/recipe/build_recipe/mod.rs:131 "(Some(default), _)"
- aaif-goose/goose@059fee25f13fa92be561a7d42cdd04ececef5a98 crates/goose/src/recipe/template_recipe.rs:39 "UndefinedBehavior::Strict"
