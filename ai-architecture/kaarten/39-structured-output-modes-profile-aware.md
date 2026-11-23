# NativeOutput valt per modelprofiel terug op een prompt-schema, en een niet-object outputtype wordt onder water in een object gewrapt

Probleem: wie "native structured output" als één uniform mechanisme behandelt, loopt vast zodra een model claimt JSON-schema te ondersteunen maar in de praktijk alleen werkt als het schema in de prompt staat, of zodra het gevraagde outputtype geen JSON-object is (een lijst, een los getal).

Oplossing:
- pydantic-ai's `NativeOutput` gebruikt het native structured-output-mechanisme van het model, maar als het modelprofiel aangeeft dat het schema alsnog als prompt-tekst verstuurd moet worden, wordt automatisch het default template op dat profiel gebruikt: "native" is dus geen harde garantie, het degradeert per model naar een prompt-gebaseerde aanpak.
- openai-agents-python wrapt elk outputtype dat geen `BaseModel` of `dict` is (zoals `list[str]` of een los `int`; platte tekst `str` of `None` blijft ongewrapt) in een verborgen `TypedDict` met één wrapper-key (`"response"`), omdat de meeste providers voor structured output een top-level JSON-object-schema eisen. Na het parsen wordt die wrapper er weer afgepeld.

Waarom het werkt: de aanroeper kiest een outputtype en een modus, en de bibliotheek vangt twee modelverschillen zelf op: een profiel dat het schema als prompt wil, en een outputtype dat geen JSON-object is.

Niet doen als: het outputtype is altijd een `BaseModel` en het model ondersteunt gegarandeerd native JSON-schema; dan is de eenvoudigste modus voldoende.

Toetsvraag: werkt structured output nog steeds correct op een model dat claimt JSON-schema te ondersteunen maar het schema alleen als prompt-tekst accepteert?

Bronnen:
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/output.py:216 "default template specified on"
- openai/openai-agents-python@6c4e4a29cd08eef454db6980d74da6afc8939d24 src/agents/agent_output.py:103 "_is_subclass_of_base_model_or_dict"
