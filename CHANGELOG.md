# CHANGELOG

<!-- version list -->

## v1.1.0 (2026-03-15)

### Bug Fixes

- **lint**: Retirer la variable count inutilisée (F841)
  ([#47](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/pull/47),
  [`d200533`](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/commit/d200533223e7b019741de0a6c771601dbaf31887))

- **search**: Corriger has_more (limit=4, results[:3]) et navigation ↑ depuis le champ
  ([#47](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/pull/47),
  [`d200533`](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/commit/d200533223e7b019741de0a6c771601dbaf31887))

- **search**: Style focus clavier identique au hover + accent gauche
  ([#49](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/pull/49),
  [`0071f64`](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/commit/0071f646424a0e8551bc49755ea656538bc23d7d))

- **search**: Utiliser e.target au lieu de document.activeElement pour la navigation clavier
  ([#48](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/pull/48),
  [`680b7e3`](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/commit/680b7e31a2eb3d624a870000b6bfd698b8b7d33d))

- **test**: Remplacer la requête fragile 'a' par 'proth' dans test_has_more
  ([#47](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/pull/47),
  [`d200533`](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/commit/d200533223e7b019741de0a6c771601dbaf31887))

### Chores

- **ci**: Retrigger release workflow avec GH_TOKEN
  ([`6b47cdf`](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/commit/6b47cdfa84b31783cea32a1d7c0bdb77ee41b5e2))

### Features

- **search**: Navigation clavier circulaire + limite à 3 suggestions
  ([#47](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/pull/47),
  [`d200533`](https://github.com/tomboulier/recos-antibioprophylaxie-SFAR/commit/d200533223e7b019741de0a6c771601dbaf31887))


## v1.0.0 (2026-03-15)

- Initial Release
