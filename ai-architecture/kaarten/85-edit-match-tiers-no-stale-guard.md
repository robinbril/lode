# Een edit-tool zoekt de oude tekst in de bestandsinhoud van dat moment, in lagen van streng naar soepel, en dat is de enige controle op verouderde context

Probleem: een model bewerkt een bestand op basis van een Read van drie stappen terug. Is de inhoud intussen veranderd, dan schrijft een naïeve replace op de verkeerde plek of overschrijft werk.

Oplossing:
- opencode leest het bestand op het moment van de edit en zoekt `oldString` in lagen: exact; alleen als dat niets oplevert met genormaliseerde typografie (slimme quotes, streepjes, rare spaties); alleen als dat ook niets oplevert regel voor regel zonder witruimte aan het einde (edit.ts:172-175).
- Nul treffers is een fout, soms met een hint van maximaal 12 regels uit het bestand, maar alleen als lezen van dat bestand al is toegestaan (:335-341). Meer dan een treffer is een fout tenzij `replaceAll` aanstaat (:346). Lege `oldString`, gelijke strings en een edit die niets verandert worden ook geweigerd (:288-293, :351).
- De rechtenvraag (:332) staat voor de controle op nul of meerdere treffers. Een edit die daarna faalt kan dus al een vraag hebben opgeleverd, zonder diff-voorbeeld.
- Alles loopt onder een slot per pad (:365), maar dat is process-lokaal: "external writes can still race" (file-mutation.ts:95). Het slot blijft ook vast tijdens het wachten op goedkeuring.
- codex (`apply_patch`) zoekt per blok context in lagen exact, rstrip, trim en genormaliseerd, en neemt de eerste treffer vanaf de huidige regel (seek_sequence.rs:35-108, file_update.rs:103). Een unieke treffer wordt dus niet afgedwongen. Bestanden worden na elkaar geschreven en lib.rs bevat geen rollback; een fout halverwege geeft de al toegepaste wijzigingen terug, en die lijst heet niet meer exact als een schrijfactie zelf faalde (lib.rs:454-467).
- Geen van beide vergelijkt een hash of mtime van de eerdere Read met nu. Een afwijkende inhoud valt alleen op doordat de tekst niet meer matcht.

Eigen voorbeeld met een expliciete versiecontrole onder het slot, die geen van beide bronnen heeft:

```python
def edit(path, old, new, seen_sha):
    with path_lock(path):
        data = path.read_bytes()  # bytes, so line endings survive
        if sha256(data).hexdigest() != seen_sha:
            raise Stale(path)
        if not old or data.count(old.encode()) != 1:
            raise NoUniqueMatch(path)
        tmp = path.with_name(f".{path.name}.{uuid4().hex}")  # a.py and a.ts never share one
        tmp.write_bytes(data.replace(old.encode(), new.encode(), 1))
        shutil.copymode(path, tmp)
        os.replace(tmp, path)
```

Wat dit niet garandeert: `path_lock` dekt alleen schrijvers in dit proces. Een externe schrijver tussen lezen en vervangen blijft mogelijk, alleen het venster is kleiner.

Waarom het werkt: een uniek te vinden oude tekst is zelf een kleine versiecontrole, en de laagjes vangen typografie op zonder de zoekplek te laten raden.

Niet doen als: een bestand binair of niet UTF-8 is, opencode weigert dat zelfs (file-mutation.ts:71).

Toetsvraag: faalt een edit waarvan de oude tekst tussen Read en edit is veranderd, en faalt een edit met twee treffers zonder replaceAll?

Bronnen:
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/tool/plugin/edit.ts:172 "findOccurrences(view, search)"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/file-mutation.ts:95 "external writes can still race"
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/apply-patch/src/seek_sequence.rs:35 "Exact match first"
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/apply-patch/src/file_update.rs:103 "seek_sequence::seek_sequence"
