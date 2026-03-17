# Architecture EPIC-3: Séparation Research & Implémentation

**Date**: 2026-03-17  
**Status**: Décision structurale prise

---

## Résumé

**EPIC-003** (Module IA + MCP) a été **restructuré en 2 phases dans 2 repos séparés**:

### 📊 Phase 2: Research (Repo separate)

**Repo**: [`antibioprophylaxie-LLM-benchmark`](../../../antibioprophylaxie-LLM-benchmark)  
**Story**: S-019 — Jeu de questions + évaluation comparative  
**Objectif**: Déterminer quel approche IA est meilleure (RAG, MCP, LLM, etc.)  
**Livrables**:
- Dataset de test (25 questions)
- Scripts d'évaluation comparative
- Findings report avec recommandations

---

### 🚀 Phase 3: Implémentation Future (v2)

**Repo**: `recos-antibioprophylaxie-SFAR` (ce repo)  
**Stories**: S-015 à S-018 (redéfinies après Phase 2)  
**Dépend de**: Findings report de Phase 2  
**Planning**: Après complètion de Phase 2 + EPIC-1 + EPIC-2

---

## Rationale

### Pourquoi séparer?

1. **Découplage conceptuel**: Research ≠ Production
2. **CI/CD indépendante**: Phase 2 n'affecte pas l'app en production
3. **Reproducibilité scientifique**: Benchmark repo est citable + reproducible
4. **Dépendances isolées**: LLM clients, embedding models, VectorDB seulement dans research
5. **Timeline flexible**: App v1 peut se déployer tandis que research progresse

### Structure

```
01-Projets/
├── recos-antibioprophylaxie-SFAR/          (App production)
│   └── (EPIC-1: Data, EPIC-2: Webapp)
│   └── EPIC-3 Phase 3: Implémentation (future)
│
└── antibioprophylaxie-LLM-benchmark/      (Research)
    └── EPIC-3 Phase 2: S-019 (benchmark)
```

---

## Status des Stories

| Story | Phase | Status | Repo |
|-------|-------|--------|------|
| S-001 à S-014 | v1 Production | 9/14 done | recos-antibioprophylaxie-SFAR |
| **S-019** | **Phase 2 Research** | **In Progress** | **antibioprophylaxie-LLM-benchmark** |
| S-015 à S-018 | Phase 3 (v2) | Pending Research | recos-antibioprophylaxie-SFAR |

---

## Prochaines étapes

1. **Phase 2 (Research)**: S-019 benchmark → findings report (semaines 2-3)
2. **Phase 1 + 2 parallel**: Finir EPIC-2 webapp (S-013, S-014) tandis que research progresse
3. **Phase 3 (Après findings)**: Redéfinir S-015-S-018 basé sur recommandations benchmark
4. **v2**: Intégrer chatbot avec le stack IA optimal

---

## Accès repos

- 📱 **App Main**: https://github.com/tomboulier/recos-antibioprophylaxie-SFAR
- 🔬 **Research Benchmark**: `/home/thomas-boulier/Documents/01-Projets/antibioprophylaxie-LLM-benchmark/`
- 🌐 **App Deployed**: https://recos-antibioprophylaxie-sfar.onrender.com

---

## Documentation

Voir:
- [`docs/sprint-status.yaml`](sprint-status.yaml) — État actuel des stories
- [`antibioprophylaxie-LLM-benchmark/docs/s-019.md`](../../../antibioprophylaxie-LLM-benchmark/docs/s-019.md) — Spec complète Phase 2
- [`antibioprophylaxie-LLM-benchmark/README.md`](../../../antibioprophylaxie-LLM-benchmark/README.md) — Usage du benchmark
