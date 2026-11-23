# Een feature flag bepaalt niet of de UI iets toont, maar of de agent een tool ooit ziet

Probleem: een AI-tool die altijd geregistreerd staat kan niet geleidelijk uitgerold worden, en een halve-uitrol-bug ("de tool bestaat wel maar werkt nog niet overal") is moeilijk te debuggen.

Oplossing:
- PostHog heeft per riskante of nieuwe tool-categorie een eigen naamgegeven flag-functie (`has_memory_tool_feature_flag`, `has_task_tool_feature_flag`, `has_mcp_gateway_feature_flag`, …), geëvalueerd met de gebruiker (`distinct_id`) en met de organisatie als groep. Of de uitrol per gebruiker of per organisatie gaat, staat in de flag zelf.
- De toolkit bouwt de lijst opnieuw op als hij wordt opgevraagd: eerst de vaste basistools, dan per flag een extra tool. De hulpfunctie heet `feature_enabled_or_false`: is de flagdienst stuk, dan is de tool uit.
- Een uitgezette tool bestaat voor het model dus niet. Een flag is uitrol, geen recht: de rechtencheck blijft in de tool zelf.
- Botsing met een stabiel cacheprefix: een flag die midden in een gesprek omslaat, verandert de toollijst en gooit de cache weg. Leg de flaguitslag daarom per gesprek vast en ververs bij een nieuw gesprek; alleen uitzetten om een incident mag direct.

Waarom het werkt: uitrol van een nieuwe tool is een flag-wijziging, geen deploy, en een probleem met één tool raakt alleen de organisaties die de flag aan hebben staan.

Niet doen als: de tool geen enkel risico of kostenimpact heeft; dan is een flag alleen overhead.

Toetsvraag: kun je een nieuwe tool voor enkele organisaties aanzetten zonder deploy, en blijft de toollijst binnen een lopend gesprek gelijk?

Bronnen:
- PostHog/posthog@9277b47 ee/hogai/utils/feature_flags.py:30 "has_task_tool_feature_flag"
- PostHog/posthog@9277b47 ee/hogai/chat_agent/toolkit.py:95 "has_task_tool_feature_flag"
- supabase/supabase@ba7d772 apps/studio/lib/ai/generate-assistant-response.ts:96 "already invalidates"
