# Welk model een tenant krijgt is een abonnementsvraag, niet een modelkeuze-vraag

Probleem: als "welk LLM-model" en "wat mag deze klant" los van elkaar beslist worden, eindig je met een duur model dat gratis gebruikers evengoed kunnen aanroepen, of met een harde crash zodra het dure model geen capaciteit heeft.

Oplossing:
- Supabase Studio markeert elke modelentry met `requiresAdvanceModelEntitlement`: modellen zonder die vlag zijn voor iedereen beschikbaar, modellen ermee vereisen de `assistant.advance_model`-entitlement die aan het betaalplan hangt.
- De functie die het taalmodel daadwerkelijk ophaalt (`getModel`) weet niets van entitlements of throttling; de aanroeper moet die knoop al hebben doorgehakt. Een pad dat dit vergeet, levert zonder fout het dure model.
- De vlag zit in het type: de basismodellen worden eruit afgeleid en de default moet een basismodel zijn, anders compileert het niet.
- Let op: `getModel` valt bij een onbekend model-id stil terug op de default van de provider. Het vooraf gelogde model is dan niet het model dat draaide.
- Gevraagd en gebruikt model in de trace: zie de kaart over trace-labels.

Waarom het werkt: de planbeslissing ligt vóór de modelaanroep, dus een nieuw model vraagt één vlag en een planwijziging raakt de provider-code niet.

Niet doen als: je maar één model aanbiedt; dan is er geen fallback om te ontwerpen.

Toetsvraag: faalt een test waarin een tenant zonder entitlement het dure model-id rechtstreeks meestuurt?

Bronnen:
- supabase/supabase@ba7d772 apps/studio/lib/ai/model.utils.ts:30 "assistant.advance_model"
- supabase/supabase@ba7d772 apps/studio/lib/ai/model.ts:41 "throttling/entitlement"
